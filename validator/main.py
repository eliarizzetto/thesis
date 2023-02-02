import os.path
from csv import DictReader
import yaml
from json import load, dump
from os.path import exists, join
from os import makedirs
import re
from helper import Helper
from csv_wellformedness import Wellformedness
from id_syntax import IdSyntax
from id_existence import IdExistence
import argparse

class Validator:
    def __init__(self, csv_doc, output_dir):
        self.data = self.read_csv(csv_doc)
        self.table_to_process = self.process_selector(self.data)
        self.helper = Helper()
        self.wellformed = Wellformedness()
        self.syntax = IdSyntax()
        self.existence = IdExistence()
        self.messages = yaml.full_load(open('validator/messages.yaml', 'r', encoding='utf-8'))
        self.id_type_dict = load(open('validator/id_type_alignment.json', 'r', encoding='utf-8'))  # for ID-type alignment (semantics)
        self.output_dir = output_dir
        if not exists(self.output_dir):
            makedirs(self.output_dir)

    def read_csv(self, csv_doc):
        with open(csv_doc, 'r', encoding='utf-8') as f:
            data_dict = list(DictReader(f))
            return data_dict

    def process_selector(self, data: list):
        process_type = None
        try:
            if all(list(row.keys()) == ["id", "title", "author", "pub_date", "venue", "volume", "issue", "page", "type",
                                        "publisher", "editor"] for row in data):
                process_type = 'meta'
                return process_type
            elif all(list(row.keys()) == ['citing_id', 'citing_publication_date', 'cited_id', 'cited_publication_date']
                     for row in
                     data):
                process_type = 'cits'
                return process_type
            else:
                return process_type
        except KeyError:
            print('The table is neither META-CSV nor CITS-CSV')
            return process_type

    def validate(self):
        if self.table_to_process == 'meta':
            self.validate_meta()
        elif self.table_to_process == 'cits':
            self.validate_cits()
        else:
            return 'Table is not well formed'

    def validate_meta(self) -> list:
        """
        Validates META-CSV.
        :param csv_doc
        :return: the list of error, i.e. the report of the validation process
        """
        error_final_report = []

        messages = self.messages
        id_type_dict = self.id_type_dict

        br_id_groups = []

        for row_idx, row in enumerate(self.data):

            missing_required_fields = self.helper.missing_values(row)  # dict w/ positions of error in row; empty if row is fine
            if missing_required_fields:
                message = messages['m17']
                table = {row_idx: missing_required_fields}
                error_final_report.append(
                    self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                      message=message, error_label='required_fields', located_in='field',
                                      table=table))
            else:
                #  4th validation level: SEMANTICS
                pass
                # TODO: AGGIUNGI FUNZIONE PER VALIDARE SEMANTICA DELLA ROW (ID-TYPE ALIGNMENT)

            for field, value in row.items():

                if field == 'id':
                    if self.helper.content(value):
                        br_ids_set = set()  # set where to put valid br IDs only
                        items = re.split(r'\s', value)

                        for item_idx, item in enumerate(items):

                            if item == '':
                                message = messages['m1']
                                table = {row_idx: {field: [item_idx]}}
                                error_final_report.append(
                                    self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                      message=message, error_label='extra_space', located_in='item',
                                                      table=table))

                            elif not self.wellformed.wellformedness_br_id(item):
                                message = messages['m2']
                                table = {row_idx: {field: [item_idx]}}
                                error_final_report.append(
                                    self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                      message=message, error_label='br_id_format',
                                                      located_in='item',
                                                      table=table))

                            else:
                                if item not in br_ids_set:
                                    br_ids_set.add(item)
                                else:  # in-field duplication of the same ID
                                    table = {row: {field: [i for i, v in enumerate(item) if v == item]}}
                                    message = messages['m6']

                                    error_final_report.append(
                                        self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                          message=message, error_label='duplicate_id',
                                                          located_in='item', table=table)  # valid=False
                                    )

                                #  2nd validation level: EXTERNAL SYNTAX OF ID (BIBLIOGRAPHIC RESOURCE)
                                if not self.syntax.check_id_syntax(item):
                                    message = messages['m19']
                                    table = {row_idx: {field: [item_idx]}}
                                    error_final_report.append(
                                        self.helper.create_error_dict(validation_level='external_syntax', error_type='error',
                                                          message=message, error_label='br_id_syntax',
                                                          located_in='item',
                                                          table=table))
                                #  3rd validation level: EXISTENCE OF ID (BIBLIOGRAPHIC RESOURCE)
                                elif not self.existence.check_id_existence(item):
                                    message = messages['m20']
                                    table = {row_idx: {field: [item_idx]}}
                                    error_final_report.append(
                                        self.helper.create_error_dict(validation_level='existence', error_type='warning',
                                                          message=message, error_label='br_id_existence',
                                                          located_in='item',
                                                          table=table, valid=True))

                        if len(br_ids_set) >= 1:
                            br_id_groups.append(br_ids_set)

                if field == 'title':
                    if self.helper.content(value):
                        if value.isupper():
                            message = messages['m8']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='warning',
                                                  message=message, error_label='uppercase_title', located_in='item',
                                                  table=table, valid=True))

                if field == 'author' or field == 'editor':
                    if self.helper.content(value):
                        items = re.split(r';\s', value)

                        for item_idx, item in enumerate(items):

                            if self.wellformed.orphan_ra_id(item):
                                message = messages['m10']
                                table = {row_idx: {field: [item_idx]}}
                                error_final_report.append(
                                    self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='warning',
                                                      message=message, error_label='orphan_ra_id',
                                                      located_in='item',
                                                      table=table, valid=True))

                            if not self.wellformed.wellformedness_people_item(item):
                                message = messages['m9']
                                table = {row_idx: {field: [item_idx]}}
                                error_final_report.append(
                                    self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                      message=message, error_label='people_item_format',
                                                      located_in='item', table=table))

                            else:
                                ids = [m.group() for m in
                                       re.finditer(r'((?:crossref|orcid|viaf|wikidata|ror):\S+)(?=\s|\])', item)]

                                for id in ids:
                                    #  2nd validation level: EXTERNAL SYNTAX OF ID (RESPONSIBLE AGENT)
                                    if not self.syntax.check_id_syntax(item):
                                        message = messages['m21']
                                        table = {row_idx: {field: [item_idx]}}
                                        error_final_report.append(
                                            self.helper.create_error_dict(validation_level='external_syntax',
                                                                          error_type='error',
                                                                          message=message, error_label='ra_id_syntax',
                                                                          located_in='item',
                                                                          table=table))
                                    #  3rd validation level: EXISTENCE OF ID (RESPONSIBLE AGENT)
                                    elif not self.existence.check_id_existence(item):
                                        message = messages['m22']
                                        table = {row_idx: {field: [item_idx]}}
                                        error_final_report.append(
                                            self.helper.create_error_dict(validation_level='existence',
                                                                          error_type='warning',
                                                                          message=message,
                                                                          error_label='ra_id_existence',
                                                                          located_in='item',
                                                                          table=table, valid=True))
                if field == 'pub_date':
                    # todo: consider splitting into items also some one-item fields, like the ones for the date,
                    #  in order to identify the error location more precisely (for example, in case of extra spaces)
                    if self.helper.content(value):
                        if not self.wellformed.wellformedness_date(value):
                            message = messages['m3']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='date_format', located_in='item',
                                                  table=table))

                if field == 'venue':
                    if self.helper.content(value):

                        if self.wellformed.orphan_venue_id(value):
                            message = messages['m15']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='warning',
                                                  message=message, error_label='orphan_venue_id', located_in='item',
                                                  table=table, valid=True))

                        if not self.wellformed.wellformedness_venue(value):
                            message = messages['m12']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='venue_format', located_in='item',
                                                  table=table))

                        else:
                            ids = [m.group() for m in
                                   re.finditer(r'((?:doi|issn|isbn|url|wikidata|wikipedia):\S+)(?=\s|\])', value)]

                            for id in ids:

                                #  2nd validation level: EXTERNAL SYNTAX OF ID (BIBLIOGRAPHIC RESOURCE)
                                if not self.syntax.check_id_syntax(id):
                                    message = messages['m19']
                                    table = {row_idx: {field: [item_idx]}}
                                    error_final_report.append(
                                        self.helper.create_error_dict(validation_level='external_syntax',
                                                                      error_type='error',
                                                                      message=message, error_label='br_id_syntax',
                                                                      located_in='item',
                                                                      table=table))
                                #  3rd validation level: EXISTENCE OF ID (BIBLIOGRAPHIC RESOURCE)
                                elif not self.existence.check_id_existence(id):
                                    message = messages['m20']
                                    table = {row_idx: {field: [item_idx]}}
                                    error_final_report.append(
                                        self.helper.create_error_dict(validation_level='existence',
                                                                      error_type='warning',
                                                                      message=message, error_label='br_id_existence',
                                                                      located_in='item',
                                                                      table=table, valid=True))
                if field == 'volume':
                    if self.helper.content(value):
                        if not self.wellformed.wellformedness_volume_issue(value):
                            message = messages['m13']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='volume_issue_format',
                                                  located_in='item',
                                                  table=table))

                if field == 'issue':
                    if self.helper.content(value):
                        if not self.wellformed.wellformedness_volume_issue(value):
                            message = messages['m13']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='volume_issue_format',
                                                  located_in='item',
                                                  table=table))

                if field == 'page':
                    if self.helper.content(value):
                        if not self.wellformed.wellformedness_page(value):
                            message = messages['m14']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='page_format', located_in='item',
                                                  table=table))
                        else:
                            if not self.wellformed.check_page_interval(value):
                                message = messages['m18']
                                table = {row_idx: {field: [0]}}
                                error_final_report.append(
                                    self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='warning',
                                                      message=message, error_label='page_interval',
                                                      located_in='item',
                                                      table=table, valid=True))

                if field == 'type':
                    if self.helper.content(value):
                        if not self.wellformed.wellformedness_type(value):
                            message = messages['m16']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='type_format', located_in='item',
                                                  table=table))

                if field == 'publisher':
                    if self.helper.content(value):
                        if self.wellformed.orphan_ra_id(value):
                            message = messages['m10']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='warning',
                                                  message=message, error_label='orphan_ra_id', located_in='item',
                                                  table=table, valid=True))

                        if not self.wellformed.wellformedness_publisher_item(value):
                            message = messages['m9']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='publisher_format',
                                                  located_in='item',
                                                  table=table))

                        else:
                            ids = [m.group() for m in
                                   re.finditer(r'((?:crossref|orcid|viaf|wikidata|ror):\S+)(?=\s|\])', item)]

                            for id in ids:

                                #  2nd validation level: EXTERNAL SYNTAX OF ID (RESPONSIBLE AGENT)
                                if not self.syntax.check_id_syntax(item):
                                    message = messages['m21']
                                    table = {row_idx: {field: [item_idx]}}
                                    error_final_report.append(
                                        self.helper.create_error_dict(validation_level='external_syntax',
                                                                      error_type='error',
                                                                      message=message, error_label='ra_id_syntax',
                                                                      located_in='item',
                                                                      table=table))
                                #  3rd validation level: EXISTENCE OF ID (RESPONSIBLE AGENT)
                                elif not self.existence.check_id_existence(item):
                                    message = messages['m22']
                                    table = {row_idx: {field: [item_idx]}}
                                    error_final_report.append(
                                        self.helper.create_error_dict(validation_level='existence',
                                                                      error_type='warning',
                                                                      message=message,
                                                                      error_label='ra_id_existence',
                                                                      located_in='item',
                                                                      table=table, valid=True))

        # GET BIBLIOGRAPHIC ENTITIES
        br_entities = self.helper.group_ids(br_id_groups)

        # GET DUPLICATE BIBLIOGRAPHIC ENTITIES (returns the list of error reports)
        duplicate_report = self.wellformed.get_duplicates_meta(entities=br_entities, data_dict=self.data, messages=messages)

        if duplicate_report:
            error_final_report.extend(duplicate_report)

        with open(join(self.output_dir,'out_validate_meta.json'), 'w', encoding='utf-8') as f:
            dump(error_final_report, f)

        return error_final_report

    def validate_cits(self) -> list:
        """
        Validates CITS-CSV.
        :param csv_doc
        :return: the list of error, i.e. the report of the validation process
        """

        error_final_report = []

        messages = yaml.full_load(open('validator/messages.yaml', 'r', encoding='utf-8'))

        id_fields_instances = []

        for row_idx, row in enumerate(self.data):
            for field, value in row.items():
                if field == 'citing_id' or field == 'cited_id':
                    if not self.helper.content(value):  # Check required fields
                        message = messages['m7']
                        table = {row_idx: {field: None}}
                        error_final_report.append(
                            self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                              message=message, error_label='required_value_cits',
                                              located_in='field',
                                              table=table))
                    else:  # i.e. if string is not empty...
                        ids_set = set()  # set where to put valid IDs only
                        items = re.split(r'\s', value)

                        for item_idx, item in enumerate(items):

                            if item == '':
                                message = messages['m1']
                                table = {row_idx: {field: [item_idx]}}
                                error_final_report.append(
                                    self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                      message=message, error_label='extra_space', located_in='item',
                                                      table=table))

                            elif not self.wellformed.wellformedness_br_id(item):
                                message = messages['m2']
                                table = {row_idx: {field: [item_idx]}}
                                error_final_report.append(
                                    self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                      message=message, error_label='br_id_format',
                                                      located_in='item',
                                                      table=table))

                            else:
                                # TODO: ADD CHECK ON LEVEL 2 (EXTERNAL SYNTAX) AND 3 (SEMANTICS) FOR THE SINGLE IDs

                                if item not in ids_set:
                                    ids_set.add(item)
                                else:  # in-field duplication of the same ID
                                    table = {row: {field: [i for i, v in enumerate(item) if v == item]}}
                                    message = messages['m6']

                                    error_final_report.append(
                                        self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                          message=message, error_label='duplicate_id',
                                                          located_in='item',
                                                          table=table)  # 'valid'=False
                                    )
                                #  2nd validation level: EXTERNAL SYNTAX OF ID (BIBLIOGRAPHIC RESOURCE)
                                if not self.syntax.check_id_syntax(item):
                                    message = messages['m19']
                                    table = {row_idx: {field: [item_idx]}}
                                    error_final_report.append(
                                        self.helper.create_error_dict(validation_level='external_syntax', error_type='error',
                                                          message=message, error_label='br_id_syntax',
                                                          located_in='item',
                                                          table=table))
                                #  3rd validation level: EXISTENCE OF ID (BIBLIOGRAPHIC RESOURCE)
                                elif not self.existence.check_id_existence(item):
                                    message = messages['m20']
                                    table = {row_idx: {field: [item_idx]}}
                                    error_final_report.append(
                                        self.helper.create_error_dict(validation_level='existence', error_type='warning',
                                                          message=message, error_label='br_id_existence',
                                                          located_in='item',
                                                          table=table, valid=True))

                        if len(ids_set) >= 1:
                            id_fields_instances.append(ids_set)

                if field == 'citing_publication_date' or field == 'cited_publication_date':
                    # todo: consider splitting into items also some one-item fields, like the ones for the date,
                    #  in order to identify the error location more precisely (for example, in case of extra spaces)
                    if self.helper.content(value):
                        if not self.wellformed.wellformedness_date(value):
                            message = messages['m3']
                            table = {row_idx: {field: [0]}}
                            error_final_report.append(
                                self.helper.create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                                  message=message, error_label='date_format', located_in='item',
                                                  table=table))

        # GET BIBLIOGRAPHIC ENTITIES
        entities = self.helper.group_ids(id_fields_instances)
        # GET SELF-CITATIONS AND DUPLICATE CITATIONS (returns the list of error reports)
        duplicate_report = self.wellformed.get_duplicates_cits(entities=entities, data_dict=self.data, messages=messages)

        if duplicate_report:
            error_final_report.extend(duplicate_report)

        with open(join(self.output_dir,'out_validate_cits.json'), 'w', encoding='utf-8') as f:
            dump(error_final_report, f)

        return error_final_report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest='input_csv', required=True, help='The path to the CSV document to validate.', type=str)
    parser.add_argument('-o', '--output', dest='output_dir', required=True, help='The path to the directory where to store the output json files.', type=str)
    args = parser.parse_args()
    v = Validator(args.input_csv, args.output_dir)
    v.validate()


#  python validator/main.py -i C:\Users\media\Desktop\thesis23\thesis_resources\validation_process\validation\test_files\cits_example.csv -o validation_output