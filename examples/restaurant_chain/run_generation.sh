#!/usr/bin/env bash
source ../../venv/bin/activate
python ../../main.py --json_files data1.json data2.json --output_view restaurant_chain.view --output_explore restaurant_chain.lkml --columnn_name raw_data_column --sql_table_name chains_table