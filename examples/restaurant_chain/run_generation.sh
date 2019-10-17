#!/usr/bin/env bash
source ../../venv/bin/activate
python ../../main.py --json_files data1.json data2.json --output_view RESTAURANT_CHAIN --output_explore RESTAURANT_CHAIN --column_name DATA --sql_table_name RESTAURANT_DETAILS --table_alias CHAINS_TABLE --handle_null_values_in_sql true --primary_key apiVersion