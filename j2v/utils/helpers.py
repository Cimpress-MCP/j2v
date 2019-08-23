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
    elif type(dim_val) == int:
        dim_type = "number"
        json_type = "number"
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
