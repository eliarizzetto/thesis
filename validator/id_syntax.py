# TODO: CHANGE IMPORTS FROM CORRECT/UPDATED LOCATION!
from CITS.oc_idmanager import doi, isbn, issn, orcid, pmcid, pmid, ror, url, viaf, wikidata, wikipedia


class IdSyntax:

    def __init__(self):
        pass

    def check_id_syntax(self, id: str):
        """
        Checks the specific external syntax of each identifier schema, calling the .syntax_ok() method from every IdManager
        module.
        :param id: the identifier (with or without its prefix)
        :return: bool
        """
        oc_prefix = id[:(id.index(':') + 1)]

        if oc_prefix == 'doi:':
            vldt = doi.DOIManager()
            return vldt.syntax_ok(id)
        if oc_prefix == 'isbn:':
            vldt = isbn.ISBNManager()
            return vldt.syntax_ok(id)
        if oc_prefix == 'issn:':
            vldt = issn.ISSNManager()
            return vldt.syntax_ok(id)
        if oc_prefix == 'orcid:':
            vldt = orcid.ORCIDManager()
            return vldt.syntax_ok(id)
        if oc_prefix == 'pmcid:':
            vldt = pmcid.PMCIDManager()
            return vldt.syntax_ok(id)
        if oc_prefix == 'pmid:':
            vldt = pmid.PMIDManager()
            return vldt.syntax_ok(id)
        if oc_prefix == 'ror:':
            vldt = ror.RORManager()
            return vldt.syntax_ok(id)
        if oc_prefix == 'url:':
            vldt = url.URLManager()
            return vldt.syntax_ok(id)
        if oc_prefix == 'viaf:':
            vldt = viaf.ViafManager()
            return vldt.syntax_ok(id)
        if oc_prefix == 'wikidata:':
            vldt = wikidata.WikidataManager()
            return vldt.syntax_ok(id)
        if oc_prefix == 'wikipedia:':
            vldt = wikipedia.WikipediaManager()
            return vldt.syntax_ok(id)