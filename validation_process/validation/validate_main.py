import re
from csv import DictReader
from re import match

accepted_fields = ["id", "title", "author", "pub_date", "venue", "volume", "issue", "page", "type", "publisher",
                   "editor"]


def validate():
    input_csv_path = "test_files/test_0.csv"
    input_csv = open(input_csv_path, 'r', encoding='utf-8')
    input_data = DictReader(input_csv)

    for row_idx, row in enumerate(input_data):

        for field, field_value in row.items():
            if content(field_value): # check if the field is empty
                if field == "id":

                    # Check id field (whole cell) for level 1, if whole cell doesn't validate, checks elements inside field
                    id_lev1(field_value)
                    print(id_lev1(field_value))
                    pass  # check OC format and later external syntax
                elif field == "title":
                    pass  # check OC format
                elif field == "author":
                    pass  # check OC format and later external syntax
                elif field == "pubdate":
                    pass  # check OC format
                elif field == "venue":
                    pass  # check OC format
                elif field == "volume":
                    pass  # check OC format
                elif field == "issue":
                    pass  # check OC format
                elif field == "page":
                    pass  # check OC format
                elif field == "type":
                    pass  # check OC format (complex!)
                elif field == "publisher":
                    pass  # check OC format and later external syntax
                elif field == "editor":
                    pass  # check OC format and later external syntax

    input_csv.close()
    pass


def content(field_str: str):
    """
    Check whether the string contains usable data.
    :param field_str: String corresponding to the value for any field key
    (e.g. the string value for the field "id").
    :return: False if the string doesn't contain only spaces or is empty, True otherwise
    """
    if match(r'^\s*$', field_str) or field_str.lower() == "none" or field_str.lower() == "nan":
        return False
    else:
        return True


def id_lev1(whole_id_field):
    """
    Checks the well-formedness of the (stripped) value for the field 'id' of a row,
    validating it according to the META-CSV format. Returns a dictionary with the errors, if any is found.
    :param whole_id_field: str
    :return: True or dict
    """
    id_field_pattern_prefix_agnostic = r'^\s*(?:(?:\S+:\S+)+(?:\s+\S+:\S+)*)\s*$'  # admits MORE than one space between the IDs
    id_field_pattern_oc_prefixes = r'^\s*(?:doi|pmid|pmcid|url|issn|isbn|wikipedia|wikidata):\S+(\s+(' \
                                   r'?:doi|pmid|pmcid|url|issn|isbn|wikipedia|wikidata):\S+)*\s*$ '  # admits MORE than one space between the IDs

    if match(id_field_pattern_oc_prefixes, whole_id_field):
        return True
    else:
        result = dict()
        for item in whole_id_field.split():
            if id_items_lev1(item) != True: # non è lo stesso che "if not id_items_lev1(item)"!!!!
                result[item] = id_items_lev1(item)
        return result

def id_items_lev1(item_in_id_field: str):
    """
    Checks the well-formedness of each specific identifier inside the 'id' field,
    validating it according to the META-CSV format. Non-accepted prefixes raise warnings.
    :param items_in_id_field: str
    :return: True or dict
    """
    single_id_pattern_prefix_agnostic = r'^[^\s:]+:\S+$'
    single_id_pattern_oc_prefix = r'^(doi|issn|isbn|pmid|pmcid|url|wikidata|wikipedia):\S+$'

    if match(single_id_pattern_oc_prefix, item_in_id_field.strip()):  # means that string is well-formatted
        return True
    elif match(single_id_pattern_prefix_agnostic, item_in_id_field.strip()):
        return {"validation_level": "1",
                "error_type": "warning"}  # means that only prefix could be wrong. doesn't validate
    else:
        return {"validation_level": "1",
                "error_type": "error"}  # means that string is certainly wrong. doesn't validate

print(validate())