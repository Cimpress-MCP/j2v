from j2v.generation.processor import MainProcessor
from j2v.utils.config import generator_config
import argparse
import datetime
import time
from j2v.utils.helpers import is_truthy

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_files", nargs=argparse.ONE_OR_MORE, type=str, default=[], )
    parser.add_argument("--output_view", nargs=argparse.OPTIONAL, type=str,
                        default=generator_config['OUTPUT_VIEW_ML_OUT_DEFAULT'], )
    parser.add_argument("--output_explore", nargs=argparse.OPTIONAL, type=str,
                        default=generator_config['EXPLORE_LKML_OUT_DEFAULT'], )
    parser.add_argument("--column_name", nargs=argparse.OPTIONAL, type=str,
                        default=generator_config['COLUMN_WITH_JSONS_DEFAULT'], )
    parser.add_argument("--sql_table_name", nargs=argparse.OPTIONAL, type=str,
                        default=generator_config['TABLE_WITH_JSON_COLUMN_DEFAULT'], )
    parser.add_argument("--table_alias", nargs=argparse.OPTIONAL, type=str,
                        default=generator_config['TABLE_ALIAS_DEFAULT'], )
    parser.add_argument("--handle_null_values_in_sql", nargs=argparse.OPTIONAL, type=str,
                        default=generator_config['HANDLE_NULL_VALUES_IN_SQL_DEFAULT'], )
    parser.add_argument("--primary_key", nargs=argparse.OPTIONAL, type=str,)
    parser.add_argument("--sql_dialect", nargs=argparse.OPTIONAL, type=str,)
    args = parser.parse_args()
    p = MainProcessor(column_name=args.column_name, output_explore_file_name=args.output_explore,
                      output_view_file_name=args.output_view, sql_table_name=args.sql_table_name,
                      table_alias=args.table_alias, handle_null_values_in_sql=is_truthy(args.handle_null_values_in_sql),
                      primary_key=args.primary_key, sql_dialect=args.sql_dialect)
    start_time = time.process_time()
    print("{date} Running the generator.\n\n".format(date=datetime.datetime.now()))
    p.process_json_files(args.json_files)
    end_time = time.process_time()
    print("\n\n{date} Finished.".format(date=datetime.datetime.now()))
    print("Took {duration:10.1f} ms".format(duration=(end_time - start_time) * 1000))
