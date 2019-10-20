import pytest
from j2v.utils.helpers import get_dimension_types, is_unix_timestamp


@pytest.mark.parametrize(
    "candidate_value, expected_result",
    [
        pytest.param("foo bar", ("string", "string"), id="Valid string is mapped to string"),
        pytest.param("2019-01-01T00:00:00.000Z", ("time", "timestamp"), id="timestamp is mapped to timestamp"),
        pytest.param(True, ("yesno", "boolean"), id="True is mapped to boolean"),
        pytest.param(False, ("yesno", "boolean"), id="True is mapped to boolean"),
        pytest.param(" ", ("string", "string"), id="Empty string is mapped to string"),
        pytest.param(None, ("string", "string"), id="None is mapped to string"),
        pytest.param(784, ("number", "number"), id ="Number type verified"),
        pytest.param(1571569684, ("epoch", "number"), id="Timestamp verified"),
        pytest.param(747.34, ("number", "number(38, 2)"), id="Number type verified"),
    ]
)
def test_get_dimension_types(candidate_value, expected_result):
    actual_result = get_dimension_types(candidate_value)
    assert actual_result == expected_result
