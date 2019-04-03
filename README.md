# JSONs to Looker views (J2V)

J2V is a simple command-line tool to convert JSON to [Looker](https://looker.com/) readable files in forms of [Looker Views](https://docs.looker.com/reference/view-params/view) and [Looker Explores](https://docs.looker.com/reference/explore-params/explore).

This is useful to be used in combination with databases that are focusing on schema-on-read, and data is stored in raw JSON instead of exploded into columns of a table or view.

## Example use case

You have a table in your database. This table contains a column containing JSONs (one JSON per row). You are very curious how these data look like exploded, but you do not want to spend 2h going through the JSON structure and specifying all the fields just to surface them in Looker.

With J2V all the structures are discovered automatically and two files are generated - a Looker View and Looker Explore. All you need to do is copy/paste the output of this command line tool into your Looker project and you can start exploring.

# Usage

## Requirements

[Python 3](https://www.python.org/downloads/) must be installed.

## How to run
* use code from github or
* `pip install j2v`

## Parameters

* `json_files`: Files in JSON format, representing the data stored in a table
* `output_view`: Name of Looker View output file to be created
* `output_explore`: Name of Looker model output file to be created
* `sql_table_name`: Name of the DB table to be used (this is only used in the LookML files; no actual connection to a database will be done as part of this tool)
* `columnn_name`: Name of the column in the DB table as specified in `sql_table_name`. (this is only used in the LookML files; no actual connection to a database will be done as part of this tool)

## Output

* `output_view`: File containing definitions of Looker views (see [examples](./examples/) directory in this repository)
* `output_explore`: File containing definition of looker explore exploading the structures (see [examples](./examples/) directory in this repository)

## Example usage

### Using all parameters

`python3 main.py --json_files data1.json data2.json --output_view restaurant_chain.view --output_explore restaurant_chain.lkml --columnn_name raw_data --sql_table_name chains`

### Using only mandatory parameters

`python3 main.py --json_files order_example.json order_example2.json order_example3.json`<br />

# Contribution

## Project structure:

* `j2v` - source code of a package
* `examples` - working examples
* `tests` - tests

## Contribute

1. If unsure, open an issue for a discussion
1. Create a fork
1. Make your change
1. Make a pull request
1. Happy contribution!
