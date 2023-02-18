# TODO: CHANGE IMPORTS FROM CORRECT/UPDATED LOCATION!
from oc_idmanager import doi, isbn, issn, orcid, pmcid, pmid, ror, url, viaf, wikidata, wikipedia


class IdExistence:

    def __init__(self):
        pass
    def check_id_existence(self, id:str):
        """
        Checks if a specific identifier is registered in the service it is provided by, by a request to the relative API,
        calling the .exists() method from every IdManager module.
        :param id: the string of the ID without the prefix
        :return: bool
        """

        oc_prefix = id[:(id.index(':')+1)]

        if oc_prefix == 'doi:':
            vldt = doi.DOIManager() # you can use removeprefix(oc_prefix) from Python 3.9+
            return vldt.exists(id.replace(oc_prefix, '', 1))  # todo: use id.replace(oc_prefix, '', 1) for Python < v.3.9
        if oc_prefix == 'isbn:':
            vldt = isbn.ISBNManager()
            return vldt.exists(id.replace(oc_prefix, '', 1))
        if oc_prefix == 'issn:':
            vldt = issn.ISSNManager()
            return vldt.exists(id.replace(oc_prefix, '', 1))
        if oc_prefix == 'orcid:':
            vldt = orcid.ORCIDManager()
            return vldt.exists(id.replace(oc_prefix, '', 1))
        if oc_prefix == 'pmcid:':
            vldt = pmcid.PMCIDManager()
            return vldt.exists(id.replace(oc_prefix, '', 1))
        if oc_prefix == 'pmid:':
            vldt = pmid.PMIDManager()
            return vldt.exists(id.replace(oc_prefix, '', 1))
        if oc_prefix == 'ror:':
            vldt = ror.RORManager()
            return vldt.exists(id.replace(oc_prefix, '', 1))
        if oc_prefix == 'url:':
            vldt = url.URLManager()
            return vldt.exists(id.replace(oc_prefix, '', 1))
        if oc_prefix == 'viaf:':
            vldt = viaf.ViafManager()
            return vldt.exists(id.replace(oc_prefix, '', 1))
        if oc_prefix == 'wikidata:':
            vldt = wikidata.WikidataManager()
            return vldt.exists(id.replace(oc_prefix, '', 1))
        if oc_prefix == 'wikipedia:':
            vldt = wikipedia.WikipediaManager()
            return vldt.exists(id.replace(oc_prefix, '', 1))