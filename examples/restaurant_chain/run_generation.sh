#!/usr/bin/env bash
source ../../venv/bin/activate
python ../../main.py --json_files data1.json data2.json --output_view restaurant_chain --output_explore restaurant_chain.lkml --columnn_name DATA --sql_table_name RESTAURANT_DETAILS --handle_null_values_in_sql true