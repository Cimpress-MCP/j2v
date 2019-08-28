import pytest

from j2v.utils.helpers import get_dimension_types

@pytest.mark.parametrize(
    "candidate_value, expected_result",
    [
        pytest.param("foo bar", ("string", "string"), id="Valid string is mapped to string"),
        pytest.param(" ", ("string", "string"), id="Empty string is mapped to string"),
        pytest.param(None, ("string", "string"), id="None is mapped to string"),
        # TODO: implement support for conversion between string representation of number -> number
        # pytest.param("1", ("number", "number"), id="string representation of integer is mapped to number"),
        # pytest.param("100.99", ("number", "number"), id="string representation of float is mapped to number"),
        pytest.param("2019-01-01T00:00:00.000Z", ("time", "timestamp"), id="timestamp is mapped to timestamp"),
        pytest.param(True, ("yesno", "boolean"), id="True is mapped to boolean"),
        # TODO: implement support for conversion between string representation of boolean -> boolean
        # pytest.param("true", ("yesno", "boolean"), id="'True' is mapped to boolean"),
        # pytest.param("false", ("yesno", "boolean"), id="'False' is mapped to boolean"),
        pytest.param(False, ("yesno", "boolean"), id="True is mapped to boolean"),
        pytest.param(1, ("number", "number"), id="integer is mapped to number"),
        pytest.param(100.99, ("number", "number"), id="float is mapped to number"),

    ],
)
def test_get_dimension_types(candidate_value, expected_result):
    actual_result = get_dimension_types(candidate_value)
    assert actual_result == expected_result
