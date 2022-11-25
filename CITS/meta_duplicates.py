from helper_functions import group_ids
from create_report import create_error_dict
# from validate_cits import messages
import re


def get_duplicates_meta(entities: list, data_dict: list, messages) -> list:
    """
    Creates a list of dictionaries containing the duplication error in the whole document between two or more rows.
    :param entities: list containing sets of strings (the IDs), where each set corresponds to a bibliographic entity.
    :param data_dict: the list of the document's rows, read as dictionaries
    :param messages: the dictionary containing the messages as they're read from the .yaml config file
    :return: list of dictionaries, each carrying full info about each duplication error within the document.
    """
    visited_dicts = []
    report = []
    for row_idx, row in enumerate(data_dict):
        br = {}

        items = re.split(r'\s', row['id'])

        for item_idx, item in enumerate(items):
            for set_idx, set in enumerate(entities):
                if item in set:  # mapping the single ID to its corresponding set representing the bibl. entity
                    br['meta_id'] = set_idx
                    br['table'] = {row_idx: {'id': list(range(len(items)))}}
                    break
            break

        if not visited_dicts:  # just for the first round of the iteration (when visited_dicts is empty)
            visited_dicts.append(br)
        else:
            for visited_br_idx, visited_br in enumerate(visited_dicts):
                if br['meta_id'] == visited_br['meta_id']:
                    visited_dicts[visited_br_idx]['table'].update(br['table'])
                    break
                elif visited_br_idx == (len(visited_dicts) - 1):
                    visited_dicts.append(br)

    for d in visited_dicts:
        if len(d['table']) > 1:  # if there's more than 1 row in table for a br (duplicate rows error)
            table = d['table']
            message = messages['m11']

            report.append(
                create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                  message=message, error_label='duplicate_br', located_in='row', table=table))

    return report
