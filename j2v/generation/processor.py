import json

from j2v.generation.generator import Generator
from j2v.generation.result_writer import SQLWriter, LookerWriter
from j2v.utils.config import generator_config
from j2v.utils.helpers import get_formatted_var_name

TABLE_WITH_JSON_COLUMN_DEFAULT = generator_config['TABLE_WITH_JSON_COLUMN_DEFAULT']
OUTPUT_VIEW_ML_OUT_DEFAULT = generator_config['OUTPUT_VIEW_ML_OUT_DEFAULT']
COLUMN_WITH_JSONS_DEFAULT = generator_config['COLUMN_WITH_JSONS_DEFAULT']
EXPLORE_LKML_OUT_DEFAULT = generator_config['EXPLORE_LKML_OUT_DEFAULT']
ELEMENT_ACCESS_STR = generator_config['ELEMENT_ACCESS_STR']
TABLE_ALIAS_DEFAULT = generator_config['TABLE_ALIAS_DEFAULT']
HANDLE_NULL_VALUES_IN_SQL_DEFAULT = generator_config['HANDLE_NULL_VALUES_IN_SQL_DEFAULT']


class MainProcessor:

    def __init__(self, column_name=COLUMN_WITH_JSONS_DEFAULT, output_explore_file_name=EXPLORE_LKML_OUT_DEFAULT,
                 output_view_file_name=OUTPUT_VIEW_ML_OUT_DEFAULT, sql_table_name=TABLE_WITH_JSON_COLUMN_DEFAULT,
                 table_alias=TABLE_ALIAS_DEFAULT, handle_null_values_in_sql=HANDLE_NULL_VALUES_IN_SQL_DEFAULT,
                 primary_key=None):
        """
        Init empty lists and ops counter.
        """
        self.output_explore_file_name = output_explore_file_name or EXPLORE_LKML_OUT_DEFAULT
        self.output_view_file_name = output_view_file_name or OUTPUT_VIEW_ML_OUT_DEFAULT
        self.column_name = column_name or COLUMN_WITH_JSONS_DEFAULT
        self.sql_table_name = sql_table_name or TABLE_WITH_JSON_COLUMN_DEFAULT
        self.table_alias = get_formatted_var_name(table_alias or TABLE_ALIAS_DEFAULT)
        self.handle_null_values_in_sql = handle_null_values_in_sql or HANDLE_NULL_VALUES_IN_SQL_DEFAULT
        self.generator = Generator(column_name=self.column_name,
                                   table_alias=self.table_alias,
                                   handle_null_values_in_sql=self.handle_null_values_in_sql,
                                   primary_key=primary_key)

        self.sql_writer = SQLWriter(self.sql_table_name, self.table_alias)
        self.looker_writer = LookerWriter(self.output_explore_file_name, self.output_view_file_name,
                                          self.sql_table_name, self.table_alias)

    def process_json_files(self, json_file_list):
        """
        :param json_file_list: List with python dicts
        :return:
        """
        for json_file in json_file_list:
            with open(json_file) as f_in:
                json_obj = json.load(f_in)
                self.process_single_object(json_obj)

        self.looker_writer.create_view_file(self.generator.dim_definitions)
        self.looker_writer.create_explore_file(self.generator.explore_joins)
        self.sql_writer.print_sql(self.generator.dim_sql_definitions, self.generator.all_joins,
                                  self.handle_null_values_in_sql)

    def transform(self, data_object):
        self.pre_process()
        self.process_single_object(data_object)
        model, sql, views = self.post_process()
        return {"sql": sql, "model": model, "views": views}

    def transform_rich(self, data_object_list):
        self.pre_process()
        for data_object in data_object_list:
            self.process_single_object(data_object)
        model, sql, views = self.post_process()
        return {"sql": sql, "model": model, "views": views}

    def pre_process(self):
        self.generator.clean()

    def post_process(self):
        views = self.looker_writer.get_view_str(self.generator.dim_definitions)
        model = self.looker_writer.get_explore_str(self.generator.explore_joins)
        sql = self.sql_writer.get_sql_str(self.generator.dim_sql_definitions, self.generator.all_joins)
        return model, sql, views

    def process_single_dict(self, python_dict):
        self.process_single_object(data_object=python_dict)

    def process_single_object(self, data_object):
        self.generator.collect_all_paths(data_object=data_object)
