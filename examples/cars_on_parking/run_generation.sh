#!/usr/bin/env bash
source ../../venv/bin/activate
python ../../main.py --json_files data2.json data1.json --output_view parking --output_explore parking --column_name data_column --sql_table_name parking_table --handle_null_values_in_sql false