class Semantics:
    def __init__(self):
        pass

    def check_semantics(self, row: dict, alignment: dict) -> dict:
        """
        Checks if all the IDs specified in 'id' are compatible with the value of 'type'.
        Return a dictionary with the fields and items involved in the error, or an empty
        dictionary if no error was found.
        :param row: (dict) the row in the table
        :param alignment: (dict) the possible associations between a type and a set of IDs
        :return: (dict)
        """
        invalid_row = {}
        row_type = row['type']
        row_ids = row['id'].split(' ')  # list
        invalid_ids_idxs = []

        for id_idx, id in enumerate(row_ids):
            if id[:id.index(':')] not in alignment[row_type]:
                invalid_ids_idxs.append(id_idx)
        if invalid_ids_idxs:
            invalid_row['id'] = invalid_ids_idxs
            invalid_row['type'] = [0]
        return invalid_row
