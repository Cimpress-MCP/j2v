#!/usr/bin/env bash
source ../../venv/bin/activate
python ../../main.py --json_files object.json --output_view object --output_explore object
python ../../main.py --json_files primitive.json --output_view primitive --output_explore primitive
python ../../main.py --json_files array_of_primitives.json --output_view array_of_primitives --output_explore array_of_primitives
python ../../main.py --json_files array_of_objects.json --output_view array_of_objects --output_explore array_of_objects
