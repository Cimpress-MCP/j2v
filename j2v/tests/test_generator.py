import os
import sys
import pytest

from j2v.generation.generator import Generator

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

ORDERS_TABLE_NAME = "orders"
IF_NULL_PREFIX = "IFNULL("
NUMERIC_SUFFIX = ",0) AS"
STRING_SUFFIX = ",'N/A') AS"


def test_empty():
    """
    For empty JSON nothing should be created.
    :return:
    """
    g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=False,primary_key=None)
    g.collect_all_paths(current_dict={})
    assert not g.dim_definitions
    assert not g.explore_joins


def test_int_key():
    """
    Int key in JSON should be ignored
    :return:
    """
    g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=False,
                  primary_key=None)
    g.collect_all_paths(current_dict={1: 2})
    assert not g.dim_definitions
    assert not g.explore_joins


def test_one_array():
    """
    Exactly 1 view should be created with 1 dimension, and one LATERAL FLATTEN expression
    :return:
    """
    g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=False,
                  primary_key=None)
    g.collect_all_paths(current_dict={ORDERS_TABLE_NAME: [{"id": 3}, {"id": 334}]})
    assert ORDERS_TABLE_NAME in g.dim_definitions
    assert 1 == len(g.dim_definitions["orders"])
    assert "id" in list(g.dim_definitions["orders"])[0]
    assert 1 == len(g.explore_joins)


@pytest.mark.parametrize(
    "json_data, prefix, suffix",
    [
        pytest.param([{"id": 3}, {"id": 334}], IF_NULL_PREFIX, NUMERIC_SUFFIX, id="replace null integer values with 0"),
        pytest.param([{"price_1": 3.01}, {"price_2": 3.34}], IF_NULL_PREFIX, NUMERIC_SUFFIX,
                     id="replace null float values with 0"),
        pytest.param([{"name": "P Sherman"}, {"address": "42 Wallaby Way, Sydney"}], IF_NULL_PREFIX, STRING_SUFFIX,
                     id="replace null string values with N/A"),

    ],
)
def test_replaces_nulls_values_in_json(json_data, prefix, suffix):
    """"
    the appropriate null handling code should be added to all columns in all_non_null_fields
    """
    g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=True,primary_key=None)
    g.collect_all_paths(current_dict={ORDERS_TABLE_NAME: json_data})
    for column_def in g.dim_sql_definitions[ORDERS_TABLE_NAME].values():
        assert column_def.startswith(prefix)
        assert suffix in column_def
