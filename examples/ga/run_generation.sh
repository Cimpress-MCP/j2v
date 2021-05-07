#!/usr/bin/env bash
source ../../venv/bin/activate
python ../../main.py --json_files data1.json --output_view ga --output_explore ga --sql_table_name ga_table --handle_null_values_in_sql true --sql_dialect=bigquery