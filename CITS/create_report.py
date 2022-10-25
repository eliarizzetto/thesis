# This file contains the base function to create a dictionary storing the information
# about an error (i.e. create a single error report).


def create_error_dict(validation_level: str, error_type: str, message: str, located_in: str, row: list, field=None, item=None):
    """
    Creates a dictionary with the information about an error
    :param validation_level: str, one of the following values: 'csv_wellformedness', 'external_syntax', 'semantic'
    :param error_type: str, one of the following values: 'error', 'warning'
    :param message: str, the message explaining the error to display to the user
    :param located_in: str, the type of the area where the error is located, i.e. ONE among the following: "row", "field", "item".
    :param row: list of one or more integers, i.e. the indexes of the rows in which the error is located
    :param field: either None or a list of strings among the following values: "id", "title", "author", "pub_date", "venue", "volume", "issue",
    "page", "type", "publisher", "editor", "citing_id", "citing_publication_date", "cited_id", "cited_publication_date".
    Must be specified whenever the error is inside a specific field.
    :param item: either None or a list of integers, i.e. the indexes of a field's items where the errors are located.
    :return: dict with the error's details
    """
    position = {'located_in': located_in, 'row': row, 'field': field, 'item': item}

    result = {
        'validation_level': validation_level,
        'error_type': error_type,
        'message': message,
        'position': position
    }

    return result
