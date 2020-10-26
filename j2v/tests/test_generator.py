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
    g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=False,
                  primary_key=None)
    g.collect_all_paths(data_object={})

    assert count_dims(g) == 0
    assert not g.explore_joins


def count_dims(g):
    count = 0
    for view, dims in g.dim_definitions.items():
        count += len(dims)
    return count


def test_int_key():
    """
    Int key in JSON should be ignored
    :return:
    """
    g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=False,
                  primary_key=None)
    g.collect_all_paths(data_object={1: 2})
    assert count_dims(g) == 0
    assert not g.explore_joins


def test_one_array():
    """
    Exactly 1 view should be created with 1 dimension, and one LATERAL FLATTEN expression
    :return:
    """
    g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=False,
                  primary_key=None)
    g.collect_all_paths(data_object={ORDERS_TABLE_NAME: [{"id": 3}, {"id": 334}]})
    assert ORDERS_TABLE_NAME in g.dim_definitions
    assert 1 == len(g.dim_definitions["orders"])
    __test_lower_cases(g)
    assert 1 == len(g.explore_joins)

def test_array_with_multiple_elements():
    """
    Exactly 1 view should be created with 4 dimensions, and one LATERAL FLATTEN expression
    :return:
    """
    g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=False,
                  primary_key=None)
    g.collect_all_paths(data_object={ORDERS_TABLE_NAME: [{"id": 3}, {"info": 334}, {"email": "a@a.com"}, {"phone_number": 3344531679}]})
    assert ORDERS_TABLE_NAME in g.dim_definitions
    assert 4 == len(g.dim_definitions["orders"])
    __test_lower_cases(g)
    assert 1 == len(g.explore_joins)


def test_array_with_missing_object_fields():
    """
    Exactly 1 view should be created with 4 dimensions, and one LATERAL FLATTEN expression
    :return:
    """
    g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=False,
                  primary_key=None)
    g.collect_all_paths(data_object={ORDERS_TABLE_NAME: [{"id": 3}, {"id": 3, "info": 334, "email": "a@a.com", "phone_number": 3344531679}]} )
    assert ORDERS_TABLE_NAME in g.dim_definitions
    assert 4 == len(g.dim_definitions["orders"])
    __test_lower_cases(g)
    assert 1 == len(g.explore_joins)



def test_one_problematic_dim_name():
    g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=False,
                  primary_key=None)
    g.collect_all_paths(data_object={ORDERS_TABLE_NAME: [{"aaaaId-ABC-DEF": 3}, {"abId-ABC--DEF": 334}], "zz": 5654.3})
    count = 0
    dims = g.dim_definitions[ORDERS_TABLE_NAME]
    for dim in dims:
        if "aaaa_id_abc_def" in dim[dim.index("dimension"):dim.index("{")]:
            count += 1

    assert count == 1


def test_lower_cases_1():
    g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=False,
                  primary_key=None)
    g.collect_all_paths(data_object={ORDERS_TABLE_NAME: [{"ID": 3}, {"ID": 334}], "AMOUNT": 5654.3})
    __test_lower_cases(g)


def test_lower_cases_2():
    g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=False,
                  primary_key=None)
    g.collect_all_paths(
        data_object={ORDERS_TABLE_NAME: [{"ID": 3}, {"ID": 334}], "AMOUNT": {"value": 5654.3, "CURRENCY": "EUR"}})
    __test_lower_cases(g)


def __test_lower_cases(g):
    for view_name, dims in g.dim_definitions.items():
        assert not any(c.isupper() for c in view_name)
        for dim in dims:
            dim_first_line = dim[dim.index("dimension"):dim.index("{")]
            assert not any(c.isupper() for c in dim_first_line)

    @pytest.mark.parametrize(
        "json_data, prefix, suffix",
        [
            pytest.param([{"id": 3}, {"id": 334}], IF_NULL_PREFIX, NUMERIC_SUFFIX,
                         id="replace null integer values with 0"),
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
        g = Generator(column_name="data_column", table_alias="data_table", handle_null_values_in_sql=True,
                      primary_key=None)
        g.collect_all_paths(data_object={ORDERS_TABLE_NAME: json_data})
        for column_def in g.dim_sql_definitions[ORDERS_TABLE_NAME].values():
            assert column_def.startswith(prefix)
            assert suffix in column_def
