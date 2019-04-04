import json
from string import digits
import re
from collections import defaultdict

from j2v.str_templates import looker_templates as lt
from j2v.utils.helpers import *
from j2v.utils.config import generator_config

TABLE_WITH_JSON_COLUMN_DEFAULT = generator_config['TABLE_WITH_JSON_COLUMN_DEFAULT']
OUTPUT_VIEW_ML_OUT_DEFAULT = generator_config['OUTPUT_VIEW_ML_OUT_DEFAULT']
COLUMN_WITH_JSONS_DEFAULT = generator_config['COLUMN_WITH_JSONS_DEFAULT']
EXPLORE_LKML_OUT_DEFAULT = generator_config['EXPLORE_LKML_OUT_DEFAULT']
ELEMENT_ACCESS_STR = generator_config['ELEMENT_ACCESS_STR']


class Generator:
    def __init__(self, column_name=COLUMN_WITH_JSONS_DEFAULT, output_explore_file_name=EXPLORE_LKML_OUT_DEFAULT,
                 output_view_file_name=OUTPUT_VIEW_ML_OUT_DEFAULT, sql_table_name=TABLE_WITH_JSON_COLUMN_DEFAULT):
        """
        Init empty lists and ops counter.
        """
        self.views_dimensions_expr = defaultdict(set)
        self.explore_joins = {}
        self.ops = 0
        # setting for name construction, leave 1 or increment
        self.maximum_naming_levels = 1
        self.output_explore_file_name = output_explore_file_name if output_explore_file_name else EXPLORE_LKML_OUT_DEFAULT
        self.output_view_file_name = output_view_file_name if output_view_file_name else OUTPUT_VIEW_ML_OUT_DEFAULT
        self.column_name = column_name if column_name else COLUMN_WITH_JSONS_DEFAULT
        self.sql_table_name = sql_table_name if sql_table_name else TABLE_WITH_JSON_COLUMN_DEFAULT
        self.visited_paths = set()
        self.all_joins = []
        self.all_fields = defaultdict(set)

    def process_jsons(self, json_string_list):
        """

        :param json_string_list: List with python dicts
        :return:
        """
        for json_file in json_string_list:
            with open(json_file) as f_in:
                json_obj = json.load(f_in)
            self.collect_all_paths(current_dict=json_obj)
        self.__create_view_file()
        self.__create_explore_file()

        self.print_sql()

    def print_sql(self):
        print("SELECT")

        after_select = True
        for view, fields in self.all_fields.items():
            print(("," if not after_select else "") + "\n---{view} Information".format(view=view))
            print("\n,".join(sorted(list(fields))))
            after_select = False

        print("FROM {table},".format(table=self.sql_table_name))
        print("\n,".join(self.all_joins))

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
            current_path = self.column_name
        if not current_view:
            current_view = self.sql_table_name
        if not root_view:
            root_view = self.sql_table_name
        for key, value in current_dict.items():
            if type(key) != str:
                continue
            path = current_path + ":" + key
            if is_primitive(value):
                self.__add_dimension(current_path, current_view, key, value)
            elif is_dict(value):
                self.collect_all_paths(value, path, current_view, root_view)
            elif is_non_empty_list(value):
                sample_element = value[0]
                new_view_name = key
                if path not in self.visited_paths and self.views_dimensions_expr[key]:
                    # path not visited but view name exists
                    new_view_name = (current_view + "_" + key)
                self.visited_paths.add(path)
                self.__add_explore_join(new_view_name=new_view_name, current_view=current_view,
                                        key=key, current_path=current_path)

                if is_dict(sample_element):
                    self.collect_all_paths(current_dict=sample_element, current_path=ELEMENT_ACCESS_STR,
                                           current_view=new_view_name,
                                           root_view=current_view)

                elif is_primitive(sample_element):
                    self.__add_dimension("", new_view_name, ELEMENT_ACCESS_STR, sample_element)

    def __add_explore_join(self, new_view_name, current_view, key, current_path):
        """

        :param new_view_name:
        :param current_view:
        :param key:
        :param current_path:
        :return:
        """
        join_path = current_view + (":" if current_view != self.sql_table_name else ".") + current_path + ":" + key
        join_path = join_path.replace(":" + ELEMENT_ACCESS_STR, "." + ELEMENT_ACCESS_STR)

        if current_view is self.sql_table_name:
            required_joins_line = ""
        else:
            required_joins_line = lt.req_joins_str_template.format(required_join=current_view)

        explore_join = lt.explore_join_str_template.format(alias=new_view_name, view=new_view_name,
                                                           exploded_structure_path=join_path,
                                                           required_joins_line=required_joins_line)

        self.explore_joins[current_path] = explore_join
        join_statement = lt.join_template.format(alias=new_view_name, exploded_structure_path=join_path)
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
        dimension_name_path = '"' + dimension_name + '"' if " " in dimension_name else dimension_name
        path_elements = list(filter(lambda _: ELEMENT_ACCESS_STR not in _, current_path.split(":")))
        path_elements.reverse()
        path_elements_for_name = path_elements[:self.maximum_naming_levels]
        # create nice description and dim name based on path and dimension name
        dimension_name = re.sub('[^0-9a-z_A-Z]+', '_', dimension_name)
        dimension_name_words = re.sub('(?!^)([A-Z][a-z]+)', r' \1', dimension_name).split()
        dimension_name_words_for_desc = map(lambda _: _.capitalize(),
                                            path_elements_for_name + dimension_name_words)
        dimension_name_words_for_dim = map(lambda _: _.lower(), path_elements_for_name + dimension_name_words)
        nice_description = ' '.join(dimension_name_words_for_desc).replace("_", " ")
        nice_dimension_name = '_'.join(dimension_name_words_for_dim).lstrip(digits)
        current_path = current_path + (":" if current_path else "") + dimension_name_path

        new_dimension = lt.dimension_str_template.format(__dimension_name=nice_dimension_name,
                                                         __desc=nice_description,
                                                         __path=current_path,
                                                         looker_type=dim_type, json_type=json_type)

        self.views_dimensions_expr[current_view].add(new_dimension)

        sql_select = lt.field_template.format(__path=current_path, TABLE=current_view, json_type=json_type)
        self.all_fields[current_view].add(sql_select)

    def __create_view_file(self):
        """

        :return:
        """
        views_out_file = open(self.output_view_file_name, "w")
        for view, dimensions in self.views_dimensions_expr.items():
            source_table = ""
            if view == self.sql_table_name:
                source_table = """\n  sql_table_name: {sql_table} ;;""".format(sql_table=self.sql_table_name)

            views_out_file.write(lt.view_start_str_template.format(name=view, base_table=source_table))
            for dim in dimensions:
                views_out_file.write(dim)
            views_out_file.write(lt.view_end_str)
        views_out_file.close()

    def __create_explore_file(self):
        """

        :return:
        """
        explore_out_file = open(self.output_explore_file_name, "w")
        explore_out_file.write(
            lt.explore_start_str_template.format(explore_name=self.sql_table_name, base_view_alias=self.sql_table_name,
                                                 base_view=self.sql_table_name,
                                                 description=self.sql_table_name + " explore",
                                                 label=self.sql_table_name + " explore",
                                                 view_file_name=self.output_view_file_name))
        for explore_join in self.explore_joins.values():
            explore_out_file.write(explore_join)

        explore_out_file.write(lt.explore_end)
        explore_out_file.close()
