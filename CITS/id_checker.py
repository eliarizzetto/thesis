from CITS.oc_idmanager import doi, isbn, issn, orcid, pmcid, pmid, ror, url, viaf, wikidata, wikipedia

# This file contains the function(s) for validating an item: A) According to externally-specified syntax (2nd level
# of validation) (service-specific format, e.g. the schema for a DOI) B) According to its "semantics" (3rd level of
# validation), i.e. checking whether it exists in the database/service linked to its prefix, and checking whether the
# value inserted in the "type" field is compatible with the ID associated to the bibliographic resource.



# todo: importa id manager e usa qui syntax_ok. prima però devi capire di che tipo di ID si tratta, ovviamente.
#   Magari, visto che la funzione è già pronta, una nuova funzione non serve scriverla a parte se non per farsi
#       un'idea preliminare di ciò che andrà integrato nella funzione principale.

# TODO: usare metodo per stringhe .removeprefix(), anche se dà problemi per la backcompatibility di Python (< v.3.9)?


def check_id_syntax(id:str):

    oc_prefix = id[:(id.index(':')+1)]

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


def check_id_existence(id:str):

    oc_prefix = id[:(id.index(':')+1)]

    if oc_prefix == 'doi:':
        vldt = doi.DOIManager()
        return vldt.exists(id.removeprefix(oc_prefix))  # todo: use id.replace(oc_prefix, '', 1) for Python < v.3.9
    if oc_prefix == 'isbn:':
        vldt = isbn.ISBNManager()
        return vldt.exists(id.removeprefix(oc_prefix))
    if oc_prefix == 'issn:':
        vldt = issn.ISSNManager()
        return vldt.exists(id.removeprefix(oc_prefix))
    if oc_prefix == 'orcid:':
        vldt = orcid.ORCIDManager()
        return vldt.exists(id.removeprefix(oc_prefix))
    if oc_prefix == 'pmcid:':
        vldt = pmcid.PMCIDManager()
        return vldt.exists(id.removeprefix(oc_prefix))
    if oc_prefix == 'pmid:':
        vldt = pmid.PMIDManager()
        return vldt.exists(id.removeprefix(oc_prefix))
    if oc_prefix == 'ror:':
        vldt = ror.RORManager()
        return vldt.exists(id.removeprefix(oc_prefix))
    if oc_prefix == 'url:':
        vldt = url.URLManager()
        return vldt.exists(id.removeprefix(oc_prefix))
    if oc_prefix == 'viaf:':
        vldt = viaf.ViafManager()
        return vldt.exists(id.removeprefix(oc_prefix))
    if oc_prefix == 'wikidata:':
        vldt = wikidata.WikidataManager()
        return vldt.exists(id.removeprefix(oc_prefix))
    if oc_prefix == 'wikipedia:':
        vldt = wikipedia.WikipediaManager()
        return vldt.exists(id.removeprefix(oc_prefix))