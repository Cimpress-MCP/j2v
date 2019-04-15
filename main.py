from j2v.generation.processor import MainProcessor
from j2v.utils.config import generator_config
import argparse
import datetime
import time

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--json_files", nargs=argparse.ONE_OR_MORE, type=str, default=[], )
    parser.add_argument("--output_view", nargs=argparse.OPTIONAL, type=str,
                        default=generator_config['OUTPUT_VIEW_ML_OUT_DEFAULT'], )
    parser.add_argument("--output_explore", nargs=argparse.OPTIONAL, type=str,
                        default=generator_config['EXPLORE_LKML_OUT_DEFAULT'], )
    parser.add_argument("--columnn_name", nargs=argparse.OPTIONAL, type=str,
                        default=generator_config['COLUMN_WITH_JSONS_DEFAULT'], )
    parser.add_argument("--sql_table_name", nargs=argparse.OPTIONAL, type=str,
                        default=generator_config['TABLE_WITH_JSON_COLUMN_DEFAULT'], )
    args = parser.parse_args()
    p = MainProcessor(column_name=args.columnn_name, output_explore_file_name=args.output_explore,
                      output_view_file_name=args.output_view, sql_table_name=args.sql_table_name)
    start_time = time.time_ns()
    print("{date} Running the generator.\n\n".format(date=datetime.datetime.now()))
    p.process_json_files(args.json_files)
    end_time = time.time_ns()
    print("\n\n{date} Finished.".format(date=datetime.datetime.now()))
    print("Took {duration} ms".format(duration=(end_time - start_time) / 10e6))
