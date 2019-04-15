import json

from j2v.generation.generator import Generator
from j2v.generation.result_writer import SQLWriter, LookerWriter
from j2v.utils.config import generator_config

TABLE_WITH_JSON_COLUMN_DEFAULT = generator_config['TABLE_WITH_JSON_COLUMN_DEFAULT']
OUTPUT_VIEW_ML_OUT_DEFAULT = generator_config['OUTPUT_VIEW_ML_OUT_DEFAULT']
COLUMN_WITH_JSONS_DEFAULT = generator_config['COLUMN_WITH_JSONS_DEFAULT']
EXPLORE_LKML_OUT_DEFAULT = generator_config['EXPLORE_LKML_OUT_DEFAULT']
ELEMENT_ACCESS_STR = generator_config['ELEMENT_ACCESS_STR']


class MainProcessor:

    def __init__(self, column_name=COLUMN_WITH_JSONS_DEFAULT, output_explore_file_name=EXPLORE_LKML_OUT_DEFAULT,
                 output_view_file_name=OUTPUT_VIEW_ML_OUT_DEFAULT, sql_table_name=TABLE_WITH_JSON_COLUMN_DEFAULT):
        """
        Init empty lists and ops counter.
        """
        self.output_explore_file_name = output_explore_file_name if output_explore_file_name else EXPLORE_LKML_OUT_DEFAULT
        self.output_view_file_name = output_view_file_name if output_view_file_name else OUTPUT_VIEW_ML_OUT_DEFAULT
        self.column_name = column_name if column_name else COLUMN_WITH_JSONS_DEFAULT
        self.sql_table_name = sql_table_name if sql_table_name else TABLE_WITH_JSON_COLUMN_DEFAULT
        self.generator = Generator(column_name=self.column_name,
                                   sql_table_name=self.sql_table_name)

        self.sql_writer = SQLWriter(self.sql_table_name)
        self.looker_writer = LookerWriter(self.output_explore_file_name, self.output_view_file_name,
                                          self.sql_table_name)

    def process_jsons(self, json_string_list):
        """

        :param json_string_list: List with python dicts
        :return:
        """
        for json_file in json_string_list:
            with open(json_file) as f_in:
                json_obj = json.load(f_in)
            self.generator.collect_all_paths(current_dict=json_obj)
        self.looker_writer.create_view_file(self.generator.views_dimensions_expr)
        self.looker_writer.create_explore_file(self.generator.explore_joins)

        self.sql_writer.print_sql(self.generator.all_fields, self.generator.all_joins)
