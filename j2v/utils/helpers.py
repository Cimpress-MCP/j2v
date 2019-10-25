from datetime import datetime, timedelta


def get_dimension_types(dim_val):
    """
        :param dim_val:
        :return: dim_type, json_type
    """
    json_type = "string"
    dim_type = "string"
    if type(dim_val) == str and (is_str_timestamp(dim_val) or is_ISO_Time(dim_val)):
        dim_type = "time"
        json_type = "timestamp"
    elif type(dim_val) == bool:
        dim_type = "yesno"
        json_type = "boolean"
    elif type(dim_val) == int:
        dim_type = "number"
        json_type = "number"
        if is_unix_timestamp(dim_val):
            dim_type = "epoch"
    elif type(dim_val) == float:
        dim_type = "number"
        json_type = "number(38, 2)"
    return dim_type, json_type


def is_str_timestamp(dim_val):
    """
    Checks if a string represents a timestamp
    :param dim_val:
    :return: True only if string represents a timestamp
    """
    try:
        datetime.strptime(dim_val, "%Y-%m-%dT%H:%M:%S.%fZ")
        return True
    except:
        return False


def is_ISO_Time(dim_val):
    """
    Checks if a string represents a ISO timestamp
    :param dim_val:
    :return: True only if string represents an ISO timestamp
    """
    try:
        datetime.fromisoformat(dim_val)
        return True
    except:
        return False


def is_unix_timestamp(dim_val):
    """
    Checks if dim_val represents a timestamp if in seconds, milliseconds and microseconds
    :param dim_val:
    :return: True only if string represents a timestamp
    """
    date_now = datetime.now()
    date_delta = timedelta(days=365)
    number_digits = len(str(dim_val))
    base_10 = 10
    
    if dim_val > 0 and number_digits in {base_10, 13, 16}:
        dim_val = int(dim_val / base_10 ** (number_digits - base_10))
        return date_now + date_delta > datetime.fromtimestamp(dim_val) > date_now - date_delta
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
