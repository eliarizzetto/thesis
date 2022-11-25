# This module contains the validation functions for a CITS-CSV instance.

from re import match, search, sub


def wellformedness_id_field(id_field):
    """
    Validates the well-formedness of the 'citing_id', 'cited_id' or 'id' field of a row (taken as a whole), checking its
    compliance with CITS-csv/META-CSV syntax.
    :param id_field: str, the whole string value of 'citing_id', 'cited_id' or 'id'
    :return: bool
    """
    id_field_pattern = r'^\S+( \S+)*$'  # no multiple adjacent spaces, no spaces at the beginning or end of the string!
    if match(id_field_pattern, id_field):
        return True
    else:
        return False


def wellformedness_br_id(id_element):
    """
    Validates the well-formedness of a single element inside the 'citing_id', 'cited_id' or 'id' field of a row,
    checking its compliance with CITS-csv/META-CSV syntax.
    :param id_element: str
    :return: bool
    """
    id_pattern = r'^(doi|issn|isbn|pmid|pmcid|url|wikidata|wikipedia):\S+$'
    if match(id_pattern, id_element):
        return True
    else:
        return False


def wellformedness_people_item(ra_item: str):
    """
    Validates the well-formedness of an item inside the 'author' or 'editor' field of a row,
    checking its compliance with META-CSV syntax.
    :param ra_item: str
    :return: bool
    """
    outside_brackets = r'(?:[^\s,;\[\]]+(?:\s[^\s,;\[\]]+)*),?(?:\s[^\s,;\[\]]+)*'
    inside_brackets = r'\[(crossref|orcid|viaf|wikidata|ror):\S+(?:\s(crossref|orcid|viaf|wikidata|ror):\S+)*\]'
    ra_item_pattern = f'^(?:({outside_brackets}\\s{inside_brackets})|({outside_brackets})|({inside_brackets}))$'

    if match(ra_item_pattern, ra_item):
        return True
    else:
        return False

def wellformedness_publisher_item(ra_item: str):
    """
    Validates the well-formedness of an item inside the 'publisher' field of a row,
    checking its compliance with META-CSV syntax.
    :param ra_item: str
    :return: bool
    """
    outside_brackets_pub = r'(?:[^\s\[\]]+(?:\s[^\s\[\]]+)*)'
    inside_brackets = r'\[(crossref|orcid|viaf|wikidata|ror):\S+(?:\s(crossref|orcid|viaf|wikidata|ror):\S+)*\]'
    ra_item_pattern = f'^(?:({outside_brackets_pub}\\s{inside_brackets})|({outside_brackets_pub})|({inside_brackets}))$'

    if match(ra_item_pattern, ra_item):
        return True
    else:
        return False

def orphan_ra_id(ra_item: str):
    """
    Looks for possible ID of responsible agents ('author', 'publisher' or 'editor') that are NOT enclosed in
    brackets, as they should be. Returns True if the input string is likely to contain one or more R.A. ID outside
    square brackets.
    :param ra_item: the item inside a R.A. field, as it is split by the '; ' separator.
    :return:
    bool, True if a match is found (the string is likely NOT well-formed), False if NO match is found.
    """
    if search(r'(crossref|orcid|viaf|wikidata|ror):', sub(r'\[.*\]', '', ra_item)):
        return True
    else:
        return False


def wellformedness_date(date_field):
    """
    Validates the well-formedness of the content of the 'citing_publication_date', 'cited_publication_date'
    or 'pub_date' field of a row, checking its compliance with CITS-csv/META-CSV syntax.
    :param date_field: str
    :return: bool
    """
    date_pattern = r'^((?:\d{4}\-(?:0[1-9]|1[012])(?:\-(?:0[1-9]|[12][0-9]|3[01]))?)|(?:\d{4}))$'
    if match(date_pattern, date_field):
        return True
    else:
        return False
