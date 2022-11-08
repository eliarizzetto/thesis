from helper_functions import group_ids
from create_report import create_error_dict
from validate_cits import messages
import re

def get_duplicates_cits(entities: list, data_dict: list) -> list:
    """
    Creates a list of dictionaries containing the duplication error in the whole document, either within a row
    (self-citation) or between two or more rows (duplicate citations).
    :param entities: list containing sets of strings (the IDs), where each set corresponds to a bibliographic entity
    :param data_dict: the list of the document's rows, read as dictionaries
    :return: list of dictionaries, each carrying full info about each duplication error within the document.
    """
    visited_dicts = []
    report = []
    for row_idx, row in enumerate(data_dict):
        citation = {}

        for field, value in row.items():
            if field == 'citing_id' or field == 'cited_id':
                items = re.split(r'\s', value)

                for item_idx, item in enumerate(items):
                    for set_idx, set in enumerate(entities):
                        if item in set:  # mapping the single ID to its corresponding set representing the bibl. entity
                            citation[field] = set_idx
                            break
                    break
        if citation['citing_id'] == citation['cited_id']:  # SELF-CITATION error (an entity cites itself) 
            table = {
                row_idx: {
                    'citing_id': [idx for idx in range(len(row['citing_id'].split(' ')))],
                    'cited_id': [idx for idx in range(len(row['cited_id'].split(' ')))]
                }
            }
            message = messages['m4']
            report.append(
                create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                  message=message, located_in='field', table=table))

        # SAVE CITATIONS BETWEEN ENTITIES IN A LIST. 
        # Each citation is represented as a nested dictionary in which the key-values representing the entity-to-entity 
        # citation are unique within the list, but the table representing the location of an INSTANCE of an
        # entity-to-entity citation is updated each time a new instance of such citation is found in the csv document. 

        citation_table = {
            row_idx: {
                'citing_id': [idx for idx in range(len(row['citing_id'].split(' ')))],
                'cited_id': [idx for idx in range(len(row['cited_id'].split(' ')))]
            }
        }

        cit_info = {'citation': citation, 'table': citation_table}

        if not visited_dicts:  # just for the first round of the iteration (when visited_dicts is empty)
            visited_dicts.append(cit_info)
        else:
            for dict_idx, cit_dict in enumerate(visited_dicts):
                if citation == cit_dict['citation']:
                    visited_dicts[dict_idx]['table'].update(cit_info['table'])
                    break
                elif dict_idx == (len(visited_dicts) - 1):
                    visited_dicts.append(cit_info)

    for d in visited_dicts:
        if len(d['table']) > 1:  # if there's more than 1 row in table for a citation (duplicate rows error)
            table = d['table']
            message = messages['m5']

            report.append(
                create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                  message=message, located_in='row', table=table))

    return report







