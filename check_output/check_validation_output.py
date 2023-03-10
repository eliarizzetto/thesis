# Copyright (c) 2023, OpenCitations <contact@opencitations.net>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.

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
    try:
        if type(validation_output_instance) == list:
            schema = load(open(join(dirname(__file__), 'error_report_schema.json'), 'r'))
            # the line above allows to access the json file from any working directory

            # if any error is raised inside "validate", the execution will just stop, and the error(s) will be printed
            return validate(validation_output_instance, schema)

        elif type(validation_output_instance) == dict:
            schema = load(open(join(dirname(__file__), 'single_error_schema.json'), 'r'))
            # the line above allows to access the json file from any working directory

            return validate(validation_output_instance, schema)

    except TypeError:
        return False, "The function's argument must be either a dictionary or a list!"

