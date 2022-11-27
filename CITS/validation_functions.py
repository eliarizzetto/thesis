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
    # todo: create stricter regex for not allowing characters that are likely to be illegal in a person's name/surname
    #   (e.g. digits, apostrophe, underscore, full-stop, etc.)
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


def wellformedness_venue(venue_value: str):
    """
    Validates the well-formedness of the string inside the 'venue' field of a row,
    checking its compliance with META-CSV syntax.
    :param venue_value: str
    :return: bool
    """
    outside_brackets_venue = r'(?:[^\s\[\]]+(?:\s[^\s\[\]]+)*)'
    # pmid and pmcid are not valid identifiers for 'venues'!
    inside_brackets_venue = r'\[(doi|issn|isbn|url|wikidata|wikipedia):\S+(?:\s(doi|issn|isbn|url|wikidata|wikipedia):\S+)*\]'
    venue_pattern = f'^(?:({outside_brackets_venue}\\s{inside_brackets_venue})|({outside_brackets_venue})|({inside_brackets_venue}))$'

    if match(venue_pattern, venue_value):
        return True
    else:
        return False


def orphan_venue_id(venue_value: str):
    """
    Looks for IDs of BRs that might be a venue but are NOT enclosed in brackets, as they should be. Returns True if the
    input string is likely to contain one or more BR ID outside square brackets.
    :param venue_value: the value of the 'venue' field of a row.
    :return:
    bool, True if a match is found (the string is likely NOT well-formed), False if NO match is found.
    """
    if search(r'(doi|issn|isbn|url|wikidata|wikipedia):', sub(r'\[.*\]', '', venue_value)):
        return True
    else:
        return False


def wellformedness_volume_issue(vi_value: str):
    """
    Validates the well-formedness of the string inside the 'volume' or 'issue' field of a row,
    checking its compliance with META-CSV syntax.
    :param vi_value: str
    :return: bool
    """
    vi_pattern = r'^\S+(?:\s\S+)*$'

    if match(vi_pattern, vi_value):
        return True
    else:
        return False


def wellformedness_page(page_value: str):
    """
    Validates the well-formedness of the string inside the 'page' field of a row,
    checking its compliance with META-CSV syntax.
    :param page_value: str
    :return: bool
    """
    # todo: create stricter regex for roman numerals and valid intervals
    # NB: incorrect roman numerals and impossible ranges (e.g. 200-20) still validate!
    natural_numbers = r'^(?:[1-9][0-9]*)-(?:[1-9][0-9]*)$'
    roman_numerals = r'^(?:[IiVvXxLlCcDdMm]+)-(?:[IiVvXxLlCcDdMm]+)$'
    page_pattern = f'{natural_numbers}|{roman_numerals}'

    if match(page_pattern, page_value):
        return True
    else:
        return False


def wellformedness_type(type_value: str):
    """
    Validates the well-formedness of the string inside the 'type' field of a row,
    checking its compliance with META-CSV syntax.
    :param type_value: str
    :return: bool
    """
    valid_types = ['book', 'book chapter', 'book part', 'book section', 'book series', 'book set', 'book track',
                   'component', 'dataset', 'data file', 'dissertation', 'edited book', 'journal', 'journal article',
                   'journal issue', 'journal volume', 'monograph', 'other', 'peer review', 'posted content',
                   'web content', 'proceedings', 'proceedings article', 'proceedings series', 'reference book',
                   'reference entry', 'report', 'report series', 'standard', 'standard series']

    if type_value in valid_types:
        return True
    else:
        return False
