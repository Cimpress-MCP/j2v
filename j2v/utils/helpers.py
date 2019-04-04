import datetime


def get_dimension_types(dim_val):
    """

    :param dim_val:
    :return:
    """
    json_type = "string"
    if dim_val is None or (type(dim_val) == list and len(dim_val) == 0):
        dim_type = ""
    elif type(dim_val) == str:
        dim_type = "string"
        json_type = "string"
        if is_str_timestamp(dim_val):
            dim_type = "date_time"
    elif type(dim_val) == bool:
        dim_type = "yesno"
        json_type = "boolean"
    elif type(dim_val) == int:
        dim_type = "number"
        json_type = "number"
    else:
        dim_type = "date"
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
    return is_non_empty_list(value) and is_dict(value[0])


def is_non_empty_array_with_primitives(value):
    return is_non_empty_list(value) and is_primitive(value[0])


def is_dict(value):
    return type(value) == dict


def is_non_empty_list(value):
    if type(value) == list and len(value) > 0:
        if type(value[0]) == list:
            return False
        return True
    return False


def is_primitive(value):
    """
    Checks if value if a python primitive
    :param value:
    :return:
    """
    return type(value) in (int, float, bool, str)
