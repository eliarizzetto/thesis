# This file contains the base structure wherein to call the validation functions for CITS-CSV.

from helper_functions import content, group_ids, check_fieldnames_cits
from validation_functions import wellformedness_id_field, wellformedness_br_id, wellformedness_date
from create_report import create_error_dict
# from check_output.check_validation_output import check_validation_output
import re
from pprint import pprint
import yaml
from csv import DictReader
from get_duplicates import get_duplicates_cits

csv_doc = 'C:/Users/media/Desktop/thesis23/thesis_resources/validation_process/validation/test_files/sample_cits.csv'


def validate_cits(csv_doc: str) -> list:
    """
    Validates CITS-CSV.
    :param csv_doc
    :return: the list of error, i.e. the report of the validation process
    """
    with open(csv_doc, 'r', encoding='utf-8') as f:
        data_dict = list(DictReader(f))

        # TODO: Handling strategy for the error here below, which doesn't allow further processing!
        if not check_fieldnames_cits(data_dict):  # check fieldnames
            raise KeyError

        error_final_report = []

        messages = yaml.full_load(open('messages.yaml', 'r', encoding='utf-8'))

        id_fields_instances = []

        for row_idx, row in enumerate(data_dict):
            for field, value in row.items():
                if field == 'citing_id' or field == 'cited_id':
                    if not content(value):  # Check required fields
                        message = messages['m7']
                        table = {row_idx: {field: None}}
                        error_final_report.append(
                            create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                              message=message, error_label='required_value_cits', located_in='field',
                                              table=table))
                    else:  # i.e. if string is not empty...
                        ids_set = set()  # set where to put valid IDs only
                        items = re.split(r'\s', value)

                        for item_idx, item in enumerate(items):

                            if item == '':
                                message = messages['m1']
                                table = {row_idx: {field: [item_idx]}}
                                error_final_report.append(
                                    create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                      message=message, error_label='extra_space', located_in='item',
                                                      table=table))

                            elif not wellformedness_br_id(item):
                                message = messages['m2']
                                table = {row_idx: {field: [item_idx]}}
                                error_final_report.append(
                                    create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                      message=message, error_label='br_id_format', located_in='item',
                                                      table=table))

                            else:
                                # TODO: ADD CHECK ON LEVEL 2 (EXTERNAL SYNTAX) AND 3 (SEMANTICS) FOR THE SINGLE IDs

                                if item not in ids_set:
                                    ids_set.add(item)
                                else:  # in-field duplication of the same ID
                                    table = {row: {field: [i for i, v in enumerate(item) if v == item]}}
                                    message = messages['m6']

                                    error_final_report.append(
                                        create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                          message=message, error_label='duplicate_id', located_in='item',
                                                          table=table)  # 'valid'=False
                                    )

                        if len(ids_set) >= 1:
                            id_fields_instances.append(ids_set)

                if field == 'citing_publication_date' or field == 'cited_publication_date':
                    # todo: consider splitting into items also some one-item fields, like the ones for the date,
                    #  in order to identify the error location more precisely (for example, in case of extra spaces)
                    if content(value):
                        if not wellformedness_date(value):
                            message = messages['m3']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='date_format', located_in='item',
                                                  table=table))

        # GET BIBLIOGRAPHIC ENTITIES
        entities = group_ids(id_fields_instances)
        # GET SELF-CITATIONS AND DUPLICATE CITATIONS (returns the list of error reports)
        duplicate_report = get_duplicates_cits(entities=entities, data_dict=data_dict, messages=messages)

        if duplicate_report:
            error_final_report.extend(duplicate_report)

        return error_final_report


pprint(validate_cits(csv_doc))
