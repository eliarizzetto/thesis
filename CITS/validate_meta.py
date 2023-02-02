# This file contains the base structure wherein to call the validation functions for META-CSV.

from helper_functions import content, group_ids, check_fieldnames_meta
from validation_functions import *
from create_report import create_error_dict
# from check_output.check_validation_output import check_validation_output
import re
from pprint import pprint
import yaml
from csv import DictReader
from meta_duplicates import get_duplicates_meta
from meta_required_fields import missing_values
from json import load

csv_doc = 'C:/Users/media/Desktop/thesis23/thesis_resources/validation_process/validation/test_files/test_0.csv'


def validate_meta(csv_doc: str) -> list:
    """
    Validates META-CSV.
    :param csv_doc
    :return: the list of error, i.e. the report of the validation process
    """
    with open(csv_doc, 'r', encoding='utf-8') as f:
        data_dict = list(DictReader(f))

        # TODO: Handling strategy for the error here below, which doesn't allow further processing!
        if not check_fieldnames_meta(data_dict):  # check fieldnames
            raise KeyError

        error_final_report = []

        messages = yaml.full_load(open('messages.yaml', 'r', encoding='utf-8'))
        id_type_dict = load(open('id_type_alignment.json', 'r', encoding='utf-8')) # for ID-type alignment (semantics)

        br_id_groups = []

        for row_idx, row in enumerate(data_dict):

            missing_required_fields = missing_values(row)  # dict w/ positions of error in row; empty if row is fine
            if missing_required_fields:
                message = messages['m17']
                table = {row_idx: missing_required_fields}
                error_final_report.append(
                    create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                      message=message, error_label='required_fields', located_in='field',
                                      table=table))
            else:
                pass
                # TODO: AGGIUNGI FUNZIONE PER VALIDARE SEMANTICA DELLA ROW (ID-TYPE ALIGNMENT)


            for field, value in row.items():

                if field == 'id':
                    if content(value):
                        br_ids_set = set()  # set where to put valid br IDs only
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
                                if item not in br_ids_set:
                                    br_ids_set.add(item)
                                else:  # in-field duplication of the same ID
                                    table = {row: {field: [i for i, v in enumerate(item) if v == item]}}
                                    message = messages['m6']

                                    error_final_report.append(
                                        create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                          message=message, error_label='duplicate_id',
                                                          located_in='item', table=table)  # valid=False
                                    )
                                # TODO: ADD CHECK ON LEVEL 2 (EXTERNAL SYNTAX) AND 3 (SEMANTICS) FOR THE SINGLE IDs

                                #  2nd validation level: EXTERNAL SYNTAX
                                if not check_id_syntax(item):
                                    message = messages['m19']
                                    table = {row_idx: {field: [item_idx]}}
                                    error_final_report.append(
                                        create_error_dict(validation_level='external_syntax', error_type='error',
                                                          message=message, error_label='br_id_syntax',
                                                          located_in='item',
                                                          table=table))

                        if len(br_ids_set) >= 1:
                            br_id_groups.append(br_ids_set)

                if field == 'title':
                    if content(value):
                        if value.isupper():
                            message = messages['m8']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                create_error_dict(validation_level='csv_wellformedness', error_type='warning',
                                                  message=message, error_label='uppercase_title', located_in='item',
                                                  table=table, valid=True))

                if field == 'author' or field == 'editor':
                    if content(value):
                        items = re.split(r';\s', value)

                        for item_idx, item in enumerate(items):

                            if orphan_ra_id(item):
                                message = messages['m10']
                                table = {row_idx: {field: [item_idx]}}
                                error_final_report.append(
                                    create_error_dict(validation_level='csv_wellformedness', error_type='warning',
                                                      message=message, error_label='orphan_ra_id', located_in='item',
                                                      table=table, valid=True))

                            if not wellformedness_people_item(item):
                                message = messages['m9']
                                table = {row_idx: {field: [item_idx]}}
                                error_final_report.append(
                                    create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                      message=message, error_label='people_item_format',
                                                      located_in='item', table=table))

                            else:
                                ids = [m.group() for m in
                                       re.finditer(r'((?:crossref|orcid|viaf|wikidata|ror):\S+)(?=\s|\])', item)]

                                for id in ids:
                                    pass
                                    # TODO: ADD CHECKS FOR lev2 and lev3 for each id inside the current item

                if field == 'pub_date':
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

                if field == 'venue':
                    if content(value):

                        if orphan_venue_id(value):
                            message = messages['m15']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                create_error_dict(validation_level='csv_wellformedness', error_type='warning',
                                                  message=message, error_label='orphan_venue_id', located_in='item',
                                                  table=table, valid=True))

                        if not wellformedness_venue(value):
                            message = messages['m12']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='venue_format', located_in='item',
                                                  table=table))

                        else:
                            ids = [m.group() for m in
                                   re.finditer(r'((?:doi|issn|isbn|url|wikidata|wikipedia):\S+)(?=\s|\])', value)]

                            for id in ids:
                                pass
                                # TODO: ADD CHECKS FOR lev2 and lev3 for each id inside the current item

                if field == 'volume':
                    if content(value):
                        if not wellformedness_volume_issue(value):
                            message = messages['m13']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='volume_issue_format', located_in='item',
                                                  table=table))

                if field == 'issue':
                    if content(value):
                        if not wellformedness_volume_issue(value):
                            message = messages['m13']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='volume_issue_format', located_in='item',
                                                  table=table))

                if field == 'page':
                    if content(value):
                        if not wellformedness_page(value):
                            message = messages['m14']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='page_format', located_in='item',
                                                  table=table))
                        else:
                            if not check_page_interval(value):
                                message = messages['m18']
                                table = {row_idx: {field: [0]}}
                                error_final_report.append(
                                    create_error_dict(validation_level='csv_wellformedness', error_type='warning',
                                                      message=message, error_label='page_interval', located_in='item',
                                                      table=table, valid=True))

                if field == 'type':
                    if content(value):
                        if not wellformedness_type(value):
                            message = messages['m16']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='type_format', located_in='item',
                                                  table=table))

                if field == 'publisher':
                    if content(value):
                        if orphan_ra_id(value):
                            message = messages['m10']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                create_error_dict(validation_level='csv_wellformedness', error_type='warning',
                                                  message=message, error_label='orphan_ra_id', located_in='item',
                                                  table=table, valid=True))

                        if not wellformedness_publisher_item(value):
                            message = messages['m9']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='publisher_format', located_in='item',
                                                  table=table))

                        else:
                            ids = [m.group() for m in
                                   re.finditer(r'((?:crossref|orcid|viaf|wikidata|ror):\S+)(?=\s|\])', item)]

                            for id in ids:
                                pass
                                # TODO: ADD CHECKS FOR lev2 and lev3 for each id inside the current item

        # GET BIBLIOGRAPHIC ENTITIES
        br_entities = group_ids(br_id_groups)

        # GET DUPLICATE BIBLIOGRAPHIC ENTITIES (returns the list of error reports)
        duplicate_report = get_duplicates_meta(entities=br_entities, data_dict=data_dict, messages=messages)

        if duplicate_report:
            error_final_report.extend(duplicate_report)

        return error_final_report


pprint(validate_meta(csv_doc))
