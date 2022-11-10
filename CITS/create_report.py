# This file contains the base function to create a dictionary storing the information
# about an error (i.e. create a single error report).


def create_error_dict(validation_level: str, error_type: str, message: str, error_label:str, located_in: str, table: dict, valid=False):
    """
    Creates a dictionary representing the error, i.e. the negative output of a validation function.
    :param validation_level: one of the following values: "csv_wellformedness", "external_syntax", "semantic".
    :param error_type: one of the following values: "error", "warning".
    :param error_label: a machine-readable label, connected to one and only one validating function.
    :param message: the message for the user.
    :param located_in: the type of the table's area where the error is located; one of the following values: "row, "field", "item".
    :param table: the tree representing the exact location of all the elements that make the error.
    :param valid = flag for specifying whether the data raising the error is still valid or not. Defaults to False, meaning that the error makes the whole document invalid.
    :return: the details of a specific error, as it is detected by executing a validation function.
    """

    position = {
        'located_in': located_in,
        'table': table
    }

    result = {
        'validation_level': validation_level,
        'error_type': error_type,
        'error_label': error_label,
        'valid': valid, # todo: consider removing 'valid' if for all warnings 'valid'=True and for all errors 'valid'=False
        'message': message,
        'position': position
    }

    return result
