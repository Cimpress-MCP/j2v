import re
from collections import defaultdict

from j2v.str_templates import looker_templates as lt
from j2v.str_templates import sql_templates as st
from j2v.utils.config import generator_config
from j2v.utils.helpers import *

ELEMENT_ACCESS_STR = generator_config['ELEMENT_ACCESS_STR']


class Generator:
    def __init__(self, column_name, sql_table_name):
        """
        Init empty lists and ops counter.
        """
        self.views_dimensions_expr = defaultdict(set)
        self.explore_joins = {}
        self.ops = 0
        # setting for name construction, leave 1 or increment
        self.maximum_naming_levels = 1
        self.column_name = column_name
        self.sql_table_name = sql_table_name
        self.all_joins = []
        self.all_fields = defaultdict(set)

    def clean(self):
        self.explore_joins = {}
        self.ops = 0
        self.all_joins = []
        self.all_fields = defaultdict(set)

    def collect_all_paths(self, current_dict, current_path=None, current_view=None, root_view=None):
        """
        Recursive. Explores the data in JSON and takes appropriate actions.
        :param current_dict: Currently processed dict
        :param current_path: Path from the root dict
        :param current_view: Currently processed view
        :param root_view:
        :return:
        """
        if not current_path:
            current_path = doublequote(self.column_name)
        if not current_view:
            current_view = self.sql_table_name
        if not root_view:
            root_view = self.sql_table_name
        for key, value in current_dict.items():
            if type(key) != str:
                continue
            if is_primitive(value):
                self.__add_dimension(current_path, current_view, key, value)
            elif is_dict(value):
                relative_path = current_path + ":" + doublequote(key)
                self.collect_all_paths(value, relative_path, current_view, root_view)
            elif is_non_empty_1D_list(value):
                new_view_name = self.__get_full_path_str(current_view, current_path, key)
                sample_element = value[0]
                if is_dict(sample_element):
                    self.__add_explore_join(new_view_name, current_view, key, current_path)
                    self.collect_all_paths(current_dict=sample_element, current_path=ELEMENT_ACCESS_STR,
                                           current_view=new_view_name,
                                           root_view=current_view)

                elif is_primitive(sample_element):
                    self.__add_explore_join(new_view_name, current_view, key, current_path)
                    self.__add_dimension("", new_view_name, ELEMENT_ACCESS_STR, sample_element, primitive_array=True)

    def __get_full_path_str(self, current_view, current_path, key):
        """

        :param current_view:
        :param current_path:
        :param key:
        :return:
        """
        # create name based on the full access path
        # remove access string from view name, only one left most occurence,
        # we cannot remove more, it can be in some field name
        full_path = current_view + ":" + current_path.replace(ELEMENT_ACCESS_STR, "", 1) + key
        # make the name valid Looker view name
        full_path_nice = re.sub(lt.invalid_dim_name_regex, '_', full_path)
        # make view name nicer
        full_path_nice = re.sub("_+", "_", full_path_nice)
        # remove the table-column name prefix, only 1 left most occurrence
        full_path_nice = full_path_nice.replace(
            self.sql_table_name + "_" + self.column_name + "_", "", 1)

        return full_path_nice

    def __add_explore_join(self, new_view_name, current_view, key, current_path):
        """

        :param new_view_name:
        :param current_view:
        :param key:
        :param current_path:
        :return:
        """

        required_joins_line = lt.req_joins_str_template.format(required_join=current_view)
        join_path = current_view + ":" + current_path + ":" + doublequote(key)

        if current_view is self.sql_table_name:
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

    def __add_dimension(self, field_path_sql, current_view, dimension_name, dim_val, primitive_array=False):
        """

        :param field_path_sql:
        :param current_view:
        :param dimension_name:
        :param dim_val:
        :return:
        """
        dim_type, json_type = get_dimension_types(dim_val)
        self.ops += 1
        full_path_nice = self.__get_full_path_str(current_view, field_path_sql, dimension_name)
        field_path_sql = field_path_sql + (":" if field_path_sql else "") + doublequote(dimension_name)
        if primitive_array:
            field_path_sql = dimension_name

        name_elements = full_path_nice.split("_")

        results = []
        # split elements by camel case
        for element in name_elements[self.maximum_naming_levels if len(name_elements) > 1 else 0:]:
            results.extend(re.sub('(?!^)([A-Z][a-z]+)', r' \1', element).split())

        nice_description = map(lambda _: _.capitalize(), results)
        nice_dimension_name = map(lambda _: _.lower(), results)

        new_dimension = lt.dimension_str_template.format(__dimension_name="_".join(nice_dimension_name),
                                                         __desc=" ".join(nice_description),
                                                         __path=field_path_sql,
                                                         looker_type=dim_type, json_type=json_type)

        self.views_dimensions_expr[current_view].add(new_dimension)

        sql_select = st.field_str_template.format(__path=field_path_sql, TABLE=current_view,
                                                  json_type=json_type, path_alias=full_path_nice.upper())
        self.all_fields[current_view].add(sql_select)
