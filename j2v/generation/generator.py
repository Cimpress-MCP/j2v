import re
from collections import defaultdict
from string import digits

from j2v.str_templates import looker_templates as lt
from j2v.str_templates import sql_templates as st
from j2v.utils.config import generator_config
from j2v.utils.helpers import *

ELEMENT_ACCESS_STR = generator_config['ELEMENT_ACCESS_STR']


def doublequote(str_expression):
    return '"' + str_expression + '"'


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
                new_view_name = self.__get_new_view_name(current_view, current_path, key)
                sample_element = value[0]
                if is_dict(sample_element):
                    self.__add_explore_join(new_view_name, current_view, key, current_path)
                    self.collect_all_paths(current_dict=sample_element, current_path=ELEMENT_ACCESS_STR,
                                           current_view=new_view_name,
                                           root_view=current_view)

                elif is_primitive(sample_element):
                    self.__add_explore_join(new_view_name, current_view, key, current_path)
                    self.__add_dimension("", new_view_name, ELEMENT_ACCESS_STR, sample_element)

    def __get_new_view_name(self, current_view, current_path, key):
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
        v_name = re.sub(lt.invalid_dim_name_regex, '_', full_path)
        # make view name nicer
        v_name = re.sub("_+", "_", v_name)
        # remove the table-column name prefix, only 1 left most occurrence
        v_name = v_name.replace(
            self.sql_table_name + "_" + self.column_name + "_", "", 1)

        return v_name

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

    def __add_dimension(self, current_path, current_view, dimension_name, dim_val):
        """

        :param current_path:
        :param current_view:
        :param dimension_name:
        :param dim_val:
        :return:
        """
        dim_type, json_type = get_dimension_types(dim_val)
        self.ops += 1
        path_elements = filter(lambda _: ELEMENT_ACCESS_STR not in _, current_path.split(doublequote(":")))
        path_elements = list(map(lambda _: _.replace('"', ""), path_elements))
        path_elements.reverse()
        # create nice description and dim name based on path and dimension name
        dimension_name = re.sub(lt.invalid_dim_name_regex, '_', dimension_name)
        dimension_name_words = re.sub('(?!^)([A-Z][a-z]+)', r' \1', dimension_name).split()
        dim_words = path_elements[:self.maximum_naming_levels] + dimension_name_words
        dimension_name_words_for_desc = map(lambda _: _.capitalize(), dim_words)
        dimension_name_words_for_dim = map(lambda _: _.lower(), dim_words)
        nice_description = ' '.join(dimension_name_words_for_desc).replace("_", " ")
        nice_dimension_name = '_'.join(dimension_name_words_for_dim).lstrip(digits)
        current_path = current_path + (":" if current_path else "") + doublequote(dimension_name)

        new_dimension = lt.dimension_str_template.format(__dimension_name=nice_dimension_name,
                                                         __desc=nice_description,
                                                         __path=current_path,
                                                         looker_type=dim_type, json_type=json_type)

        self.views_dimensions_expr[current_view].add(new_dimension)

        sql_select = st.field_str_template.format(__path=current_path, TABLE=current_view,
                                                  json_type=json_type)
        self.all_fields[current_view].add(sql_select)
