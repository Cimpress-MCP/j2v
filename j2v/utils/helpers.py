import datetime


def get_dimension_types(dim_val):
    """

    :param dim_val:
    :return:
    """
    json_type = "string"
    dim_type = "string"
    if type(dim_val) == str:
        dim_type = "string"
        json_type = "string"
        if is_str_timestamp(dim_val):
            dim_type = "time"
            json_type = "timestamp"
    elif type(dim_val) == bool:
        dim_type = "yesno"
        json_type = "boolean"
    elif type(dim_val) == int or type(dim_val) == float:
        dim_type = "number"
        json_type = "number"
    elif dim_val is None:
        dim_type = "string"
        json_type = "string"
    return dim_type, json_type


def is_str_timestamp(potential_ts):
    """
    Checks if a string represents a timestamp
    :param potential_ts:
    :return: True only if string represents a timestamp
    """
    try:
        datetime.datetime.strptime(potential_ts, "%Y-%m-%dT%H:%M:%S.%fZ")
        return True
    except:
        return False


def is_non_empty_array_with_dicts(value):
    return is_non_empty_1D_list(value) and is_dict(value[0])


def is_non_empty_array_with_primitives(value):
    return is_non_empty_1D_list(value) and is_primitive(value[0])


def is_dict(value):
    return type(value) == dict


def is_non_empty_1D_list(value):
    # limit the level of nested lists
    # eg we will not process a list like [[""]]
    return type(value) == list and len(value) > 0 and type(value[0]) != list


def is_primitive(value):
    """
    Checks if value if a python primitive
    :param value:
    :return:
    """
    return type(value) in (int, float, bool, str)


def doublequote(str_expression):
    return '"' + str_expression + '"'


def is_truthy(candidate_value):
    """
    Converts many representations of "True" into a boolean True
    @param: candidate_value - the value to be evaluated. Any of the following will be considered True
    "true", "TRUE", "True", "1", any number except zero, True
    """
    if isinstance(candidate_value, str):
        return candidate_value.lower() in ["true", "1"]
    elif isinstance(candidate_value, int):
        return bool(candidate_value)
    elif isinstance(candidate_value, bool):
        return candidate_value
    else:
        raise TypeError("Expected a str, int or bool and got {}".format(type(candidate_value)))
