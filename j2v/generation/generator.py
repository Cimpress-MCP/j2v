import re
from collections import defaultdict

from j2v.str_templates import looker_templates as lt
from j2v.str_templates import sql_templates as st
from j2v.utils.config import generator_config
from j2v.utils.helpers import *

ELEMENT_ACCESS_STR = generator_config['ELEMENT_ACCESS_STR']


class Generator:
    def __init__(self, column_name, table_alias, handle_null_values_in_sql, primary_key):
        """
        Init empty lists and ops counter.
        """
        self.all_joins = []
        self.explore_joins = {}
        self.column_name = column_name
        self.table_alias = table_alias
        self.primary_key = primary_key
        self.handle_null_values_in_sql = handle_null_values_in_sql
        self.dim_definitions = defaultdict(set)
        self.dim_sql_definitions = defaultdict(defaultdict)

    def clean(self):
        self.explore_joins = {}
        self.all_joins = []

    def collect_all_paths(self, current_dict, current_path=None, current_view=None, root_view=None, parent_object_key=None):
        """
        Recursive. Explores the data in JSON and takes appropriate actions.
        :param parent_object_key: group label for dimension
        :param current_dict: Currently processed dict
        :param current_path: Path from the root dict
        :param current_view: Currently processed view
        :param root_view:
        :return:
        """
        if not current_path:
            current_path = doublequote(self.column_name)
        if not current_view:
            current_view = self.table_alias
        if not root_view:
            root_view = self.table_alias
        for key, value in current_dict.items():
            if type(key) != str:
                continue
            if is_primitive(value) or value is None:
                self.add_dimension(current_path, current_view, key, value, parent_object_key)
            elif is_dict(value):
                relative_path = current_path + ":" + doublequote(key)
                self.collect_all_paths(value, relative_path, current_view, root_view, key)
            elif is_non_empty_1D_list(value):
                new_view_name = self.get_full_path_str(current_view, current_path, key)
                sample_element = value[0]
                if is_dict(sample_element):
                    self.add_explore_join(new_view_name, current_view, key, current_path)
                    self.collect_all_paths(current_dict=sample_element,
                                           current_path=ELEMENT_ACCESS_STR,
                                           current_view=new_view_name,
                                           root_view=current_view)

                elif is_primitive(sample_element):
                    self.add_explore_join(new_view_name, current_view, key, current_path)
                    self.add_dimension("", new_view_name, ELEMENT_ACCESS_STR, sample_element, None,
                                       primitive_array=True)

    def get_full_path_str(self, current_view, current_path, key):
        """

        :param current_view:
        :param current_path:
        :param key:
        :return:
        """
        # create name based on the full access path
        # remove access string from view name, only one left most occurrence,
        # we cannot remove more, it can be in some field name
        full_path = current_view + ":" + current_path.replace(ELEMENT_ACCESS_STR, "", 1) + key
        # make the name valid Looker view name
        full_path_nice = re.sub(lt.invalid_dim_name_regex, '_', full_path)
        # make view name nicer
        full_path_nice = re.sub("_+", "_", full_path_nice)
        # remove the table-column name prefix, only 1 left most occurrence
        full_path_nice = full_path_nice.replace(
            self.table_alias + "_" + self.column_name + "_", "", 1)
        return full_path_nice

    def get_epoch_conversion(self, epoch_length):
        conversion = 1
        if epoch_length == 13:
            conversion = 10 ** 3
        elif epoch_length == 16:
            conversion = 10 ** 6
        return "/" + str(conversion) if conversion > 1 else ""

    def add_explore_join(self, new_view_name, current_view, key, current_path):
        """

        :param new_view_name:
        :param current_view:
        :param key:
        :param current_path:
        :return:
        """

        required_joins_line = lt.req_joins_str_template.format(required_join=current_view)
        join_path = current_view + ":" + current_path + ":" + doublequote(key)

        if current_view is self.table_alias:
            # root view
            required_joins_line = ""
            join_path = current_view + "." + current_path + ":" + doublequote(key)

        join_path = join_path.replace(":" + ELEMENT_ACCESS_STR, "." + ELEMENT_ACCESS_STR)
        join_statement = st.join_str_template.format(alias=new_view_name,
                                                     exploded_structure_path=join_path)
        explore_join = lt.explore_join_str_template.format(alias=new_view_name, view=new_view_name,
                                                           join_expression=join_statement,
                                                           required_joins_line=required_joins_line)

        self.explore_joins[join_path] = explore_join

        # keep the order
        if join_statement not in self.all_joins:
            self.all_joins.append(join_statement)

    def add_dimension(self, field_path_sql, current_view, dimension_name, dim_val, parent_object_key,
                      primitive_array=False):
        """
        :param primitive_array:
        :param field_path_sql:
        :param current_view:
        :param dimension_name:
        :param dim_val:
        :param parent_object_key:
        :return:
        """
        dim_type, json_type = get_dimension_types(dimension_name, dim_val)
        full_path_nice = self.get_full_path_str(current_view, field_path_sql, dimension_name)
        field_path_sql = field_path_sql + (":" if field_path_sql else "") + doublequote(dimension_name)

        name_elements = full_path_nice.split("_")
        results = list()
        for element in name_elements[1 if len(name_elements) > 1 else 0:]:
            results.extend(re.sub('(?!^)([A-Z][a-z]+)', r' \1', element).split())
        #   explode camel cased dimension names
        exploded_dim_name = re.sub('(?!^)([A-Z][a-z]+)', r' \1', dimension_name).split()

        if primitive_array:
            field_path_sql = dimension_name
            #   add parent field name for naming 1-D array
            exploded_dim_name.insert(0, name_elements[-2])

        nice_description = map(lambda _: _.capitalize(), results)
        nice_dimension_name = map(lambda _: _.lower(), exploded_dim_name)

        group_label_string = "\n    {}:\"{}\"".format("group_label", parent_object_key) if parent_object_key is not None else ""

        dimension_name_final = "_".join(nice_dimension_name)

        primary_key_field = "\n    primary_key: yes" if parent_object_key is None and self.primary_key == dimension_name else ""

        sql_select = self.build_sql_select(json_type, dim_type, field_path_sql, current_view, full_path_nice.upper())

        # check for duplicate dimension name in current view by checking the sql definitions in the same view
        if dimension_name_final in self.dim_sql_definitions[current_view] and sql_select not in self.dim_sql_definitions[current_view][dimension_name_final]:
            dimension_name_final = "_".join(["" if len(name_elements) == 1 else name_elements[-2], dimension_name_final])

        self.dim_sql_definitions[current_view][dimension_name_final] = sql_select

        if dim_type == "time" and json_type == "timestamp":
            new_dimension = lt.dimension_group_time_template.format(
                dimension_name=dimension_name_final,
                desc=" ".join(nice_description),
                data_type_field="",
                path=field_path_sql,
                looker_type=dim_type,
                json_type=json_type)

        elif dim_type == "epoch" and json_type == "number":
            new_dimension = lt.dimension_group_time_template.format(
                dimension_name=dimension_name_final,
                desc=" ".join(nice_description),
                data_type_field="\n    datatype:{}".format(dim_type),
                looker_type="time",
                path=field_path_sql,
                json_type=json_type + self.get_epoch_conversion(len(str(dim_val))))
        else:
            new_dimension = lt.dimension_str_template.format(
                dimension_name=dimension_name_final,
                desc=" ".join(nice_description),
                path=field_path_sql,
                looker_type=dim_type,
                primary_key_field=primary_key_field,
                json_type=json_type,
                group_label_string=group_label_string)

        self.dim_definitions[current_view].add(new_dimension)

    def build_sql_select(self, json_type, dim_type, field_path_sql, current_view, full_path_nice_upper):
        if self.handle_null_values_in_sql:

            if json_type.startswith('number'):
                return st.non_nullable_numeric_field_str_template.format(
                    path=field_path_sql,
                    TABLE=current_view, json_type=json_type,
                    path_alias=full_path_nice_upper)

            elif json_type == "string" and dim_type != "time":
                return st.non_nullable_text_field_str_template.format(
                    path=field_path_sql,
                    TABLE=current_view, json_type=json_type,
                    path_alias=full_path_nice_upper)
        return st.field_str_template.format(
            path=field_path_sql,
            TABLE=current_view,
            json_type=json_type,
            path_alias=full_path_nice_upper)