error_final_report = []

for field, value in row.items():
    if content(value):

        if field == 'citing_id' or field == 'cited_id':
            items = re.split('\s', value)

            if not wellformedness_id_field(value):
                pass

            # # ----FACTOR OUT COMMON PARTS (1)
            # badly_formed_items_idxs = []  # list with items that share the same error (failed well-formedness)
            for id_idx, id in enumerate(items):

                if not wellformedness_single_id(id):
                    # # ----FACTOR OUT COMMON PARTS (2)
                    # badly_formed_items_idxs.append(id_idx)
                    error_final_report.append(
                        create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                          message=message, located_in='item', row=[0], field=[field], item=[id_idx]))
            # # ----FACTOR OUT COMMON PARTS (3)
            # if badly_formed_items_idxs != []:
            #     error_final_report.append(
            #         create_error_dict(validation_level='csv_wellformedness', error_type='error',
            #                           message=message, located_in='item', row=[0], field=[field], item=badly_formed_items_idxs))

# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------

for field, value in row.items():
    if content(value):

        if field == 'citing_id' or field == 'cited_id':
            items = re.split('\s', value)

            if not wellformedness_id_field(value):
                pass

            # ----FACTOR OUT COMMON PARTS (1)
            badly_formed_items_idxs = []  # list with items that share the same error (failed well-formedness)
            for id_idx, id in enumerate(items):

                if not wellformedness_single_id(id):
                    # ----FACTOR OUT COMMON PARTS (2)
                    badly_formed_items_idxs.append(id_idx)

                    # error_final_report.append(
                    #     create_error_dict(validation_level='csv_wellformedness', error_type='error',
                    #                       message=message, located_in='item', row=[0], field=[field], item=[id_idx]))

            # ----FACTOR OUT COMMON PARTS (3)
            if badly_formed_items_idxs != []:
                error_final_report.append(
                    create_error_dict(validation_level='csv_wellformedness', error_type='error',
                                      message=message, located_in='item', row=[0], field=[field], item=badly_formed_items_idxs))