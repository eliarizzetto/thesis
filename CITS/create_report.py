# This file contains the base function to create a dictionary storing the information
# about an error (i.e. create a single error report).


def create_error_dict(validation_level: str, error_type: str, message: str, row: int, field=None, idx_in_field=None):
    """
    Creates a dictionary with the information about an error
    :param validation_level: str, one of the following values: 'csv_wellformedness', 'external_syntax', 'semantic'
    :param error_type: str, one of the following values: 'error', 'warning'
    :param message: str, the message explaining the error to display to the user
    :param row: int, the index of the row in which the error is located
    :param field: (Optional) str, one of the following values: "id", "title", "author", "pub_date", "venue", "volume", "issue",
    "page", "type", "publisher", "editor", "citing_id", "citing_publication_date", "cited_id", "cited_publication_date".
    Must be specified whenever the error is inside a specific field.
    :param idx_in_field: (Optional) int, the index of a list element
    :return: dict with the error's details
    """
    position = {'row': row}

    if field is not None:
        position['field'] = field
    if idx_in_field is not None:
        position['idx_in_field'] = idx_in_field

    result = {
        'validation_level': validation_level,
        'error_type': error_type,
        'message': message,
        'position': position
    }

    return result
