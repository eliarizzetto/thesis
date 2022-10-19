# This module contains the validation functions for a CITS-CSV instance.

from re import match


def wellformedness_single_id(id_element):
    """
    Validates the well-formedness of a single element inside the 'citing_id', 'cited_id' or 'id' field of a row, checking its
    compliance with CITS-csv/META-CSV syntax.
    :param id_element: str
    :return: bool
    """
    id_pattern = r'^(doi|issn|isbn|pmid|pmcid|url|wikidata|wikipedia):\S+$'
    if match(id_pattern, id_element):
        return True
    else:
        return False

def wellformedness_date(date_field):
    """
    Validates the well-formedness of the content of the 'citing_publication_date', 'cited_publication_date'
    or 'pub_date' field of a row, checking its compliance with CITS-csv/META-CSV syntax.
    :param id_element: str
    :return: bool
    """
    date_pattern = r'^((?:\d{4}\-(?:0[1-9]|1[012])(?:\-(?:0[1-9]|[12][0-9]|3[01]))?)|(?:\d{4}))$'
    if match(date_pattern, date_field):
        return True
    else:
        return False



