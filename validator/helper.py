class Helper:
    def __init__(self):  # todo: è necessario mettere init?
        self.descr = 'contains helper functions'

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

    def create_validation_summary(self, error_report):
        """
        Creates a natural language summary of the validation error report.
        :param error_report:
        :return:
        """
        #  TODO: either call this inside validate_cits and validate_meta or use it separately.
        #   If used inside validate_meta/validate_cits, it must be called before returning error dict,
        #   it must take in input the list final_error_report, and just write the summary on an external
        #   txt file (returning None)
        #   If used separately it must take in input the JSON file of final_error_report and must return
        #   the summary as a string (as well as saving the output on a file).
        #   Consider the possibility of combining both possibilities, i.e. being called separately and inside
        #   the two main methods of Validator. Think about argparser!
        return ''
