import pytest
from j2v.utils.helpers import get_dimension_types, is_unix_timestamp


@pytest.mark.parametrize(
    "candidate_value, expected_result",
    [
        pytest.param("foo bar", ("string", "string"), id="Valid string is mapped to string"),
        pytest.param(" ", ("string", "string"), id="Empty string is mapped to string"),
        pytest.param(None, ("string", "string"), id="None is mapped to string"),
        pytest.param("2019-01-01T00:00:00.000Z", ("time", "timestamp"), id="timestamp is mapped to timestamp"),
        pytest.param(True, ("yesno", "boolean"), id="True is mapped to boolean"),
        pytest.param(False, ("yesno", "boolean"), id="True is mapped to boolean"),
    ],
)
def test_get_dimension_types(candidate_value, expected_result):
    actual_result = get_dimension_types(None, candidate_value)
    assert actual_result == expected_result


@pytest.mark.parametrize(
    "candidate_dim_name,candidate_dim_val,expected_value",
    [
        pytest.param("mytime", 1571329632, True, id="\'time\' in dim_name, type of dim_val is int"),
        pytest.param("blah", 1571330161, False, id="\'time\' in dim_name, type of dim_val is int"),
        pytest.param("mytime", -1571330428, False, id="\'time\' in dim_name dim_name, of dim_val is not int"),
        pytest.param("createdAt", 1571330562, False, id="\'time\' not in dim_name dim_name, type of dim_val is not int"),
        pytest.param("mytime", 0, False, id="\'time\' in dim_name dim_name, dim_val is 0"),
    ],
)
def test_is_unix_timestamp(candidate_dim_name, candidate_dim_val, expected_value):
    actual_value = is_unix_timestamp(candidate_dim_name, candidate_dim_val)
    assert actual_value is expected_value
