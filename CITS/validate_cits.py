# This file contains the base structure wherein to call the validation functions for CITS-CSV.

from helper_functions import content
from validation_functions import wellformedness_id_field, wellformedness_single_id, wellformedness_date
from create_report import create_error_dict
from check_output.check_validation_output import check_validation_output
import re
from pprint import pprint

# sample_row = {
#     'citing_id': 'doi:10/10894u4i3 wikidata:Q5163238 issn:73874',
#     'citing_publication_date': '2020-04-17',
#     'cited_id': 'isbn:7388748744',
#     'cited_publication_date': '2018-02-14'
# }
sample_invalid_row = {
    'citing_id': 'ciao:10/10894u4i3 wikidata:Q5163238   issn:73874',
    'citing_publication_date': '2020-17',
    'cited_id': 'isbn:7388748744',
    'cited_publication_date': '2018/02/14'
}

error_final_report = []

for field, value in sample_invalid_row.items():
    if content(value):

        if field == 'citing_id' or field == 'cited_id':
            items = re.split('\s', value)

            if not wellformedness_id_field(value):
                message = "The value in this field is not expressed in compliance with the syntax of OpenCitations " \
                          "CITS-CSV. The content of 'citing_id' and 'cited_id' must be either a single ID or a sequence" \
                          " of IDs, each separated by one single space character (Unicode Character “SPACE”, U+0020). " \
                          "Each ID must not have spaces within itself, and must be of the following form: " \
                          "ID abbreviation + “:” + ID value. "

                wrong_items_idxs = []  # find and append to list which item locations raise the error (extra spaces)
                for idx, item in enumerate(items):
                    if item == '':
                        wrong_items_idxs.append(idx)

                error_final_report.append(
                    create_error_dict(validation_level='csv_wellformedness', error_type='error', message=message,
                                      located_in='row',
                                      row=[0], field=[field], item=wrong_items_idxs))


            # badly_formed_items_idxs = []  # list with items that share the same error (failed well-formedness)
            for id_idx, id in enumerate(items):

                if not wellformedness_single_id(id):
                    message = "The value in this field is not expressed in compliance with the syntax of OpenCitations " \
                              "CITS-CSV. Each identifier in 'citing_id' and/or 'cited_id' must have the following " \
                              "form: ID abbreviation + “:” + ID value. No spaces are admitted within the ID. Example: " \
                              "doi:10.48550/arXiv.2206.03971. The accepted prefixes (ID abbreviations) are the " \
                              "following: 'doi', 'issn', 'isbn', 'pmid', 'pmcid', 'url', 'wikidata', 'wikipedia'. "

                    # badly_formed_items_idxs.append(id_idx)
                    error_final_report.append(
                        create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                          message=message, located_in='item', row=[0], field=[field], item=[id_idx]))

            # if badly_formed_items_idxs != []:
            #     error_final_report.append(
            #         create_error_dict(validation_level='csv_wellformedness', error_type='error',
            #                           message=message, located_in='item', row=[0], field=[field], item=badly_formed_items_idxs))


                    # -------------ADD CHECK ON LEVEL 2 (EXTERNAL SYNTAX) AND 3 (SEMANTICS) FOR THE SINGLE IDs

        if field == 'citing_publication_date' or field == 'cited_publication_date':
            if not wellformedness_date(value):
                message = "The value in this field is not expressed in compliance with the syntax of OpenCitations " \
                          "CITS-CSV. The content of 'citing_publication_date' and/or 'cited_publication_date' must be " \
                          "of one of the following forms (according to standard ISO 86014): YYYY-MM-DD, YYYY-MM, " \
                          "YYYY. If year is required, month and day are optional. If the day is expressed, " \
                          "the day must also be expressed. Examples: '2000'; '2000-04'; '2000-04-27'."

                error_final_report.append(create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                            message=message, located_in='field', row=[0],
                                                            field=[field]))

pprint(error_final_report)
