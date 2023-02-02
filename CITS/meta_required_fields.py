from helper_functions import content

# https://github.com/opencitations/metadata/blob/master/documentation/csv_documentation.pdf

def missing_values(row:dict) -> dict:
    """
    Checks whether a row has all required fields, depending on the specified 'type' of the resource, in case the value
    of 'id' is not specified.
    :param row:
    :return:
    """
    # valid_types = ['book', 'book chapter', 'book part', 'book section', 'book series', 'book set', 'book track',
    #                'component', 'dataset', 'data file', 'dissertation', 'edited book', 'journal', 'journal article',
    #                'journal issue', 'journal volume', 'monograph', 'other', 'peer review', 'posted content',
    #                'web content', 'proceedings', 'proceedings article', 'proceedings series', 'reference book',
    #                'reference entry', 'report', 'report series', 'standard', 'standard series']

    # TODO: Consider using an external config file, as you do for checking id-type semantic alignment, since the list
    #  of accepted types might change/be extended frequently!

    missing = {}
    if not content(row['id']):  # ID value is missing

        if content(row['type']): # ID is missing and 'type' is specified

            if row['type'] in ['book', 'dataset', 'data file', 'dissertation', 'edited book', 'journal',
                               'journal article',  'monograph', 'other', 'peer review', 'posted content',
                               'web content', 'proceedings article', 'reference book', 'report']:
                if not content(row['title']):
                    missing['type'] = [0]
                    missing['title'] = None
                if not content(row['pub_date']):
                    missing['type'] = [0]
                    missing['pub_date'] = None
                if not content(row['author']) and not content(row['editor']):
                    missing['type'] = [0]
                    if not content(row['author']):
                        missing['author'] = None
                    if not content(row['editor']):
                        missing['editor'] = None

            elif row['type'] in ['book chapter', 'book part', 'book section', 'book track', 'component',
                                 'reference entry']:
                if not content(row['title']):
                    missing['type'] = [0]
                    missing['title'] = None
                if not content(row['venue']):
                    missing['type'] = [0]
                    missing['venue'] = None

            elif row['type'] in ['book series', 'book set', 'journal', 'proceedings', 'proceedings series',
                                 'report series', 'standard', 'standard series']:
                if not content(row['title']):
                    missing['type'] = [0]
                    missing['title'] = None

            elif row['type'] == 'journal issue':
                if not content(row['venue']):
                    missing['type'] = [0]
                    missing['venue'] = None
                if not content(row['title']) and not content(row['issue']):
                    missing['type'] = [0]
                    if not content(row['title']):
                        missing['title'] = None
                    if not content(row['issue']):
                        missing['issue'] = None

            elif row['type'] == 'journal volume':
                if not content(row['venue']):
                    missing['type'] = [0]
                    missing['venue'] = None
                if not content(row['title']) and not content(row['volume']):
                    missing['type'] = [0]
                    if not content(row['title']):
                        missing['title'] = None
                    if not content(row['volume']):
                        missing['volume'] = None

        else:  # ID and type are both missing
            # Se l'id non è specificato e manca anche il valore di 'type',
            # allora tutti i seguenti field devono essere specificati:
            # 'title', 'pub_date', 'author' OR 'editor'. Considera di escludere da questo if statement i casi
            # in cui sono specificati 'volume' e/o 'issue'


            if not content(row['title']):
                missing['type'] = None
                missing['title'] = None
            if not content(row['pub_date']):
                missing['type'] = None
                missing['pub_date'] = None
            if not content(row['author']) and not content(row['editor']):
                missing['type'] = None
                if not content(row['author']):
                    missing['author'] = None
                if not content(row['editor']):
                    missing['editor'] = None



    # INDIPENDENTEMENTE (???? verifica con Arca!!) dal fatto che l'ID sia specificato o no, se 'volume' e/o 'issue' sono specificati,
    # si applicano (possibilmente in aggiunta ad altri requirements già controllati):
    #   1) il fatto che il 'type' deve essere presente e deve essere uno dei seguenti valori: 'journal article',
    #           'journal volume', 'journal issue' (OCCHIO! il fatto che il type non sia il valore giusto
    #           potrebbe diventare anche un altro tipo di errore/messaggio...)
    #   2) il fatto che deve essere specificato anche 'venue'

    if content(row['id']): # todo: se la presenza di 'id' è irrelevante, togli if statement e indenta indietro i primi 2 if blocks sottostanti!
        if content(row['volume']):
            if not content(row['venue']):
                missing['volume'] = [0]
                missing['venue'] = None
            if row['type'] not in ['journal article', 'journal volume', 'journal issue']:
                missing['volume'] = [0]
                if not content(row['type']):
                    missing['type'] = None
                else:
                    missing['type'] = [0]

        if content(row['issue']):
            if not content(row['venue']):
                missing['issue'] = [0]
                missing['venue'] = None
            if row['type'] not in ['journal article', 'journal volume', 'journal issue']:
                missing['issue'] = [0]
                if not content(row['type']):
                    missing['type'] = None
                else:
                    missing['type'] = [0]

    return missing

