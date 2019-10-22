import pytest
from j2v.utils.helpers import get_dimension_types


@pytest.mark.parametrize(
    "candidate_value, expected_result",
    [
        pytest.param("foo bar", ("string", "string"), id="Valid string is mapped to string"),
        pytest.param("2019-01-01T00:00:00.000Z", ("time", "timestamp"), id="Datetime is mapped to timestamp"),
        pytest.param(True, ("yesno", "boolean"), id="True is mapped to boolean"),
        pytest.param(False, ("yesno", "boolean"), id="True is mapped to boolean"),
        pytest.param(" ", ("string", "string"), id="Empty string is mapped to string"),
        pytest.param(None, ("string", "string"), id="None is mapped to string"),
        pytest.param(784, ("number", "number"), id="Number type verified"),
        pytest.param(1571569684, ("epoch", "number"), id="Timestamp verified"),
        pytest.param(747.34, ("number", "number(38, 2)"), id="Number (Decimal) type verified"),
        pytest.param("2019-10-21T11:55:00+02:00", ("time", "timestamp"), id="Check for ISO time")
    ]
)
def test_get_dimension_types(candidate_value, expected_result):
    actual_result = get_dimension_types(candidate_value)
    assert actual_result == expected_result
