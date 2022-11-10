# This file contains auxiliary functions that might be of use when dealing with a recurring task in the validation steps.

from re import match

def content(value):
    """
    Checks whether the value of a given field contains data, i.e. is not an empty string.
    :param value: the value for any field key
    (e.g. the string value for the field "id").
    :return: False if the value is an empty string, True otherwise
    """
    # does not consider None values, given that csv.DictReader automatically converts them into empty strings
    return False if value == '' else True


def group_ids(id_groups: list):
    """
    Divides identifiers in a list of sets, where each set corresponds to a bibliographic entity.
    Takes in input a list of sets where each set represent the field 'citing_id', 'cited_id' or 'id' of a single row.
    Two IDs are considered to be associated to the same bibliographic entity if they occur together in a set at
    least once.
    :param id_groups: list containing sets of formally valid IDs
    :return: list of sets grouping the IDs associated to the same bibliographic entity
    """
    old_len = len(id_groups) + 1
    while len(id_groups) < old_len:
        old_len = len(id_groups)
        for i in range(len(id_groups)):
            for j in range(i+1, len(id_groups)):
                if len(id_groups[i] & id_groups[j]):
                    id_groups[i] = id_groups[i] | id_groups[j]
                    id_groups[j] = set()
        id_groups = [id_groups[i] for i in range(len(id_groups)) if id_groups[i] != set()]

    return id_groups

def check_fieldnames_cits(data:list):
    """
    Checks whether all the fieldnames are present, correct, and in the right order in all the rows of the .csv documents.
    :param data: the list of dictionaries, each representing a row
    :return: bool
    """
    return all(list(row.keys()) == ['citing_id', 'citing_publication_date', 'cited_id', 'cited_publication_date'] for row in data)
