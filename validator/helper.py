
class Helper:
    def __init__(self):  # todo: è necessario mettere init?
        self.descr = 'contains helper functions'

    def content(self, value):
        """
        Checks whether the value of a given field contains data, i.e. is not an empty string.
        :param value: the value for any field key
        (e.g. the string value for the field "id").
        :return: False if the value is an empty string, True otherwise
        """
        # does not consider None values, given that csv.DictReader automatically converts them into empty strings
        return False if value == '' else True

    def group_ids(self, id_groups: list):
        """
        Divides identifiers in a list of sets, where each set corresponds to a bibliographic entity.
        Takes in input a list of sets where each set represent the field 'citing_id', 'cited_id' or 'id' of a single row.
        Two IDs are considered to be associated to the same bibliographic entity if they occur together in a set at
        least once.
        :param id_groups: list containing sets of formally valid IDs
        :return: list of sets grouping the IDs associated to the same bibliographic entity
        """
        old_len = len(id_groups) + 1
        while len(id_groups) < old_len:
            old_len = len(id_groups)
            for i in range(len(id_groups)):
                for j in range(i + 1, len(id_groups)):
                    if len(id_groups[i] & id_groups[j]):
                        id_groups[i] = id_groups[i] | id_groups[j]
                        id_groups[j] = set()
            id_groups = [id_groups[i] for i in range(len(id_groups)) if id_groups[i] != set()]

        return id_groups

    def create_error_dict(self, validation_level: str, error_type: str, message: str, error_label: str, located_in: str,
                          table: dict, valid=False):
        """
        Creates a dictionary representing the error, i.e. the negative output of a validation function.
        :param validation_level: one of the following values: "csv_wellformedness", "external_syntax", "semantic".
        :param error_type: one of the following values: "error", "warning".
        :param error_label: a machine-readable label, connected to one and only one validating function.
        :param message: the message for the user.
        :param located_in: the type of the table's area where the error is located; one of the following values: "row, "field", "item".
        :param table: the tree representing the exact location of all the elements that make the error.
        :param valid = flag for specifying whether the data raising the error is still valid or not. Defaults to False, meaning that the error makes the whole document invalid.
        :return: the details of a specific error, as it is detected by executing a validation function.
        """

        position = {
            'located_in': located_in,
            'table': table
        }

        result = {
            'validation_level': validation_level,
            'error_type': error_type,
            'error_label': error_label,
            'valid': valid,
            # todo: consider removing 'valid' if for all warnings 'valid'=True and for all errors 'valid'=False
            'message': message,
            'position': position
        }

        return result

    def missing_values(self, row: dict) -> dict:
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
        if not self.content(row['id']):  # ID value is missing

            if self.content(row['type']):  # ID is missing and 'type' is specified

                if row['type'] in ['book', 'dataset', 'data file', 'dissertation', 'edited book', 'journal',
                                   'journal article', 'monograph', 'other', 'peer review', 'posted content',
                                   'web content', 'proceedings article', 'reference book', 'report']:
                    if not self.content(row['title']):
                        missing['type'] = [0]
                        missing['title'] = None
                    if not self.content(row['pub_date']):
                        missing['type'] = [0]
                        missing['pub_date'] = None
                    if not self.content(row['author']) and not self.content(row['editor']):
                        missing['type'] = [0]
                        if not self.content(row['author']):
                            missing['author'] = None
                        if not self.content(row['editor']):
                            missing['editor'] = None

                elif row['type'] in ['book chapter', 'book part', 'book section', 'book track', 'component',
                                     'reference entry']:
                    if not self.content(row['title']):
                        missing['type'] = [0]
                        missing['title'] = None
                    if not self.content(row['venue']):
                        missing['type'] = [0]
                        missing['venue'] = None

                elif row['type'] in ['book series', 'book set', 'journal', 'proceedings', 'proceedings series',
                                     'report series', 'standard', 'standard series']:
                    if not self.content(row['title']):
                        missing['type'] = [0]
                        missing['title'] = None

                elif row['type'] == 'journal issue':
                    if not self.content(row['venue']):
                        missing['type'] = [0]
                        missing['venue'] = None
                    if not self.content(row['title']) and not self.content(row['issue']):
                        missing['type'] = [0]
                        if not self.content(row['title']):
                            missing['title'] = None
                        if not self.content(row['issue']):
                            missing['issue'] = None

                elif row['type'] == 'journal volume':
                    if not self.content(row['venue']):
                        missing['type'] = [0]
                        missing['venue'] = None
                    if not self.content(row['title']) and not self.content(row['volume']):
                        missing['type'] = [0]
                        if not self.content(row['title']):
                            missing['title'] = None
                        if not self.content(row['volume']):
                            missing['volume'] = None

            else:  # ID and type are both missing
                # Se l'id non è specificato e manca anche il valore di 'type',
                # allora tutti i seguenti field devono essere specificati:
                # 'title', 'pub_date', 'author' OR 'editor'. Considera di escludere da questo if statement i casi
                # in cui sono specificati 'volume' e/o 'issue'

                if not self.content(row['title']):
                    missing['type'] = None
                    missing['title'] = None
                if not self.content(row['pub_date']):
                    missing['type'] = None
                    missing['pub_date'] = None
                if not self.content(row['author']) and not self.content(row['editor']):
                    missing['type'] = None
                    if not self.content(row['author']):
                        missing['author'] = None
                    if not self.content(row['editor']):
                        missing['editor'] = None

        # INDIPENDENTEMENTE (???? verifica con Arca!!) dal fatto che l'ID sia specificato o no, se 'volume' e/o 'issue' sono specificati,
        # si applicano (possibilmente in aggiunta ad altri requirements già controllati):
        #   1) il fatto che il 'type' deve essere presente e deve essere uno dei seguenti valori: 'journal article',
        #           'journal volume', 'journal issue' (OCCHIO! il fatto che il type non sia il valore giusto
        #           potrebbe diventare anche un altro tipo di errore/messaggio...)
        #   2) il fatto che deve essere specificato anche 'venue'

        if self.content(row[
                       'id']):  # todo: se la presenza di 'id' è irrelevante, togli if statement e indenta indietro i primi 2 if blocks sottostanti!
            if self.content(row['volume']):
                if not self.content(row['venue']):
                    missing['volume'] = [0]
                    missing['venue'] = None
                if row['type'] not in ['journal article', 'journal volume', 'journal issue']:
                    missing['volume'] = [0]
                    if not self.content(row['type']):
                        missing['type'] = None
                    else:
                        missing['type'] = [0]

            if self.content(row['issue']):
                if not self.content(row['venue']):
                    missing['issue'] = [0]
                    missing['venue'] = None
                if row['type'] not in ['journal article', 'journal volume', 'journal issue']:
                    missing['issue'] = [0]
                    if not self.content(row['type']):
                        missing['type'] = None
                    else:
                        missing['type'] = [0]

        return missing