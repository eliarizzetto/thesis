# This file contains auxiliary functions that might be of use when dealing with a recurring task in the validation steps.

from re import match

def content(field_str: str):
    """
    Check whether the string contains usable data.
    :param field_str: String corresponding to the value for any field key
    (e.g. the string value for the field "id").
    :return: False if the string contains only spaces or is empty, True otherwise
    """
    if match(r'^\s*$', field_str) or field_str.lower() == "none" or field_str.lower() == "nan" or field_str.lower() == 'null' or field_str == '':
        return False
    else:
        return True

