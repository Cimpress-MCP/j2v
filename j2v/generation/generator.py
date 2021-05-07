from collections import defaultdict
import random
from j2v.str_templates import sql_templates as st
from j2v.utils.helpers import *

class Generator:
    def __init__(self, column_name, table_alias, handle_null_values_in_sql, sql_dialect, primary_key):
        """
        Init empty lists.
        """
        self.all_joins = []
        self.explore_joins = {}
        self.column_name = column_name
        self.table_alias = table_alias
        self.sql_dialect = sql_dialect
        self.primary_key = primary_key
        self.handle_null_values_in_sql = handle_null_values_in_sql
        self.dim_definitions = defaultdict(set)
        self.dim_sql_definitions = defaultdict(defaultdict)

    def clean(self):
        self.explore_joins = {}
        self.all_joins = []

    def collect_all_paths(self, data_object, current_path=None, current_view=None, data_object_key=None,
                          parent_object_key=None):
        """
        Recursive. Explores the data and takes appropriate actions.
        :param data_object: Currently processed dict, list or primitive type
        :param current_path: Path from the root
        :param current_view: Currently processed view
        :param data_object_key: data object key (the object parent in a json tree)
        :param parent_object_key: a key of a data object key (the object grandparent in a json tree)
        :return:
        """

        templates = getattr(st, self.sql_dialect)
        if current_path is None and data_object_key is None:
            current_path = templates["path_step"].format(path_step=self.column_name)
        elif data_object_key is not None:
            new_step = templates["path_step"].format(path_step=data_object_key)
            current_path = templates["concat_steps"].format(step1=current_path, step2=new_step) if current_path else new_step
        elif current_path is not None and data_object_key is None:
            current_path = templates["ELEMENT_ACCESS_STR"]
        if current_view is None:
            current_view = self.table_alias
            self.dim_definitions[current_view] = set()

        if is_primitive(data_object) or data_object is None:
            self.add_dimension(current_path, current_view, data_object_key or templates["ELEMENT_ACCESS_STR"], data_object,
                               parent_object_key)
        elif is_dict(data_object):
            str_keys_only = filter(lambda item: type(item[0]) == str, data_object.items())
            primitives_first_items = sorted(str_keys_only, key=lambda x: self.sortation_order(x[1]))
            for key, value in primitives_first_items:
                self.collect_all_paths(data_object=value, current_path=current_path, current_view=current_view,
                                       data_object_key=key,
                                       parent_object_key=data_object_key)
        elif is_non_empty_1D_list(data_object):
            view_name = self.create_view_name(current_view, current_path)            
            self.add_explore_join(view_name, current_view, current_path)
            # Sample size i.e. the number of elements that will be sampled/processed inside an array in the JSON
            array_sample_size = 50            
            data_objects_selected = random.sample(data_object,min(len(data_object), array_sample_size))
            for element in data_objects_selected:
                self.collect_all_paths(data_object=element,
                                   current_path=current_path,
                                   current_view=view_name)

    @staticmethod
    def sortation_order(value):
        def depth(x):
            if type(x) is dict and x:
                return 1 + max(depth(x[a]) for a in x)
            if type(x) is list and x:
                return 1 + max(depth(a) for a in x)
            return 0

        # put primitives at the first place, since we will not have alternatives in case of duplicated dim names
        # the deepest dicts should be processed at the end
        if is_primitive(value) or value is None:
            return -1
        return depth(value)

    def create_view_name(self, current_view, current_path):
        """
        :param current_view:
        :param current_path:
        :return:
        """
        # create name based on the full access path
        # remove access string from view name, only one left most occurrence,
        # we cannot remove more, it can be in some field name
        templates = getattr(st, self.sql_dialect)
        full_path = current_view + ":" + current_path.replace(templates["ELEMENT_ACCESS_STR"], "", 1)

        full_path_nice = full_path.replace(self.table_alias, "", 1)
        full_path_nice = full_path_nice.replace(self.column_name, "", 1)
        view_name_candidate = get_formatted_var_name(full_path_nice)
        if len(view_name_candidate) == 0:
            view_name_candidate = get_formatted_var_name(full_path)
        return view_name_candidate

    def add_explore_join(self, new_view_name, current_view, current_path):
        """
        :param new_view_name:
        :param current_view:
        :param current_path:
        :return:
        """

        templates = getattr(st, self.sql_dialect)
        required_joins_line = lt.req_joins_str_template.format(required_join=current_view)
        join_path = current_view + ":" + current_path

        if current_view is self.table_alias:
            # root view
            required_joins_line = ""
            join_path = current_view + "." + current_path
        join_path = join_path.replace(":" + templates["ELEMENT_ACCESS_STR"], "." + templates["ELEMENT_ACCESS_STR"])
        join_separator = templates["join_separator"]
        join_statement = templates['join_str_template'].format(alias=new_view_name,
                                                     exploded_structure_path=join_path)
                                                     ## HERE

        explore_join = lt.explore_join_str_template.format(alias=new_view_name, view=new_view_name,
                                                           join_expression=join_separator + join_statement,
                                                           required_joins_line=required_joins_line)

        self.explore_joins[join_path] = explore_join

        if join_statement not in self.all_joins:
            self.all_joins.append(join_statement)

    def add_dimension(self, field_path_sql, current_view, object_key, object_value, parent_object_key,
                      primitive_array=False):
        """
        :param primitive_array:
        :param field_path_sql:
        :param current_view:
        :param object_key:
        :param object_value:
        :param parent_object_key:
        :return:
        """
        dim_type, json_type = get_dimension_types(object_value)
        full_path_nice = self.create_view_name(current_view, field_path_sql)
        field_path_with_key = field_path_sql

        dimension_name_final = get_formatted_var_name(object_key)
        nice_description = " ".join(dimension_name_final.split("_")).capitalize()

        if primitive_array:
            field_path_with_key = object_key

        group_label_string = ""
        if parent_object_key:
            group_label = " ".join(get_formatted_var_name(parent_object_key).split("_")).capitalize()
            group_label_string = "\n    group_label: \"{}\"".format(group_label)

        primary_key_field = "\n    primary_key: yes" if parent_object_key is None and self.primary_key == object_key else ""

        sql_select = self.build_sql_select(json_type, dim_type, field_path_with_key, current_view,
                                           full_path_nice.upper())

        # check for duplicate dimension name in current view by checking the sql definitions in the same view
        i = 1
        dimension_name_final_origin = dimension_name_final
        while dimension_name_final in self.dim_sql_definitions[current_view] and sql_select not in \
                self.dim_sql_definitions[current_view][dimension_name_final] and i < len(field_path_sql.split(":")) - 1:
            dimension_name_final = "_".join(field_path_sql.split(":")[-i - 1:-1]) + dimension_name_final_origin
            dimension_name_final = get_formatted_var_name(dimension_name_final)
            i += 1

        self.dim_sql_definitions[current_view][dimension_name_final] = sql_select

        new_dimension = self.get_dim_str(dim_type, object_value, dimension_name_final, field_path_with_key,
                                         group_label_string, json_type, nice_description, primary_key_field)

        self.dim_definitions[current_view].add(new_dimension)

    def get_dim_str(self, dim_type, dim_val, dimension_name_final, field_path_sql, group_label_string, json_type,
                    nice_description, primary_key_field):
        dimension_sql = getattr(st, self.sql_dialect)['dimension_sql']
        if dim_type == "time" and json_type == "timestamp":
            new_dimension = lt.dimension_group_time_template.format(
                dimension_name=dimension_name_final,
                dimension_label=nice_description,
                desc=nice_description,
                data_type_field="",
                looker_type=dim_type,
                dimension_sql=dimension_sql.format(path=field_path_sql, json_type=json_type, group_label_string = ""))

        elif dim_type == "epoch" and json_type == "number":
            new_dimension = lt.dimension_group_time_template.format(
                dimension_name=dimension_name_final,
                dimension_label=nice_description,
                desc=nice_description,
                data_type_field="\n    datatype: {}".format(dim_type),
                looker_type="time",
                dimension_sql=dimension_sql.format(path=field_path_sql, json_type=json_type + get_epoch_conversion(len(str(dim_val))), group_label_string = ""))
        else:
            new_dimension = lt.dimension_str_template.format(
                dimension_name=dimension_name_final,
                dimension_label=nice_description,
                desc=nice_description,
                looker_type=dim_type,
                primary_key_field=primary_key_field,
                dimension_sql=dimension_sql.format(path=field_path_sql, json_type=json_type, group_label_string = group_label_string))
        return new_dimension

    def build_sql_select(self, json_type, dim_type, field_path_sql, current_view, full_path_nice_upper):
        if self.handle_null_values_in_sql:

            if json_type.startswith('number'):
                return getattr(st, self.sql_dialect)['non_nullable_numeric_field_str_template'].format(
                    path=field_path_sql,
                    TABLE=current_view, json_type=json_type,
                    path_alias=full_path_nice_upper)

            elif json_type == "string" and dim_type != "time":
                return getattr(st, self.sql_dialect)['non_nullable_text_field_str_template'].format(
                    path=field_path_sql,
                    TABLE=current_view, json_type=json_type,
                    path_alias=full_path_nice_upper)
        return getattr(st, self.sql_dialect)['field_str_template'].format(
            path=field_path_sql,
            TABLE=current_view,
            json_type=json_type,
            path_alias=full_path_nice_upper)
