from json import load
from jsonschema import validate

from os.path import dirname, join


def check_validation_output(validation_output_instance):
    """
    Checks whether the output of a validation process, either a list of errors (such as the whole error report)
    or a dictionary (such as the output of a single validation function), complies with its respective JSON Schema
    for the output (i.e. the one for an array of objects or the one for a single object). Returns True if no error
    is raised, stops execution otherwise, raising the errors from jsonschema.validate().
    :param validation_output_instance: dict|list
    :return: True
    """
    schema = None

    if type(validation_output_instance) == list:
        # schema = load(open('error_report_schema.json', 'r'))
        schema = load(open(join(dirname(__file__), 'error_report_schema.json'), 'r'))
        # the line above allows to access the json file from any working directory
    elif type(validation_output_instance) == dict:
        # schema = load(open('single_validation_output_schema.json', 'r'))
        schema = load(open(join(dirname(__file__), 'single_validation_output_schema.json'), 'r'))
        # the line above allows to access the json file from any working directory
    else:
        raise TypeError("The function's argument must be either a dictionary or a list!")

    if validate(validation_output_instance, schema) is None:
        return True
    # if any error is raised inside "validate", the execution will just stop, and the error(s) will be printed
