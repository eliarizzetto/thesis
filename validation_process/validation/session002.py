# ----accessing and reading files
import glob
from csv import DictReader
from os import sep, makedirs, walk
from os.path import exists, basename, isdir
import tarfile

# ----managing identifiers

from index.identifier.doimanager import DOIManager
from index.identifier.issnmanager import ISSNManager
from index.identifier.orcidmanager import ORCIDManager
from re import sub, match

source_paths = 'C:/Users/media/Desktop/thesis23/meta_input'


# source_paths= "C:/Users/media/Desktop/thesis23/oc/index/index/validation/test_files"


def get_all_files(i_dir_or_targz_file):
    """
    Modified version of index.coci.glob.get_all_files() in order to access .csv files. If compressed files are found,
    it automatically decompress and read them. Returns 2 variables: a list of file paths of raw .csv files; and the
    list of decompressed files if any is found (otherwise None).
    """
    result = []
    targz_fd = None

    if isdir(i_dir_or_targz_file):
        for cur_dir, cur_subdir, cur_files in walk(i_dir_or_targz_file):
            for cur_file in cur_files:
                if cur_file.endswith(".csv") and not basename(cur_file).startswith("."):
                    result.append(cur_dir + sep + cur_file)
    elif i_dir_or_targz_file.endswith("tar.gz"):
        targz_fd = tarfile.open(i_dir_or_targz_file, "r:gz", encoding="utf-8")
        for cur_file in targz_fd:
            if cur_file.name.endswith(".csv") and not basename(cur_file.name).startswith("."):
                result.append(cur_file)
    else:
        print("It is not possible to process the input path.")
    return result, targz_fd


def access_csv(source_dir):
    """Accesses the input directory and its relative subdirectories
    and returns a list of all the .csv file paths therein"""

    source_data = glob.glob(f'{source_dir}/**/*.csv', recursive=True)
    return source_data


# ----------------parametri da mettere in input: source_paths,

doi_mngr = DOIManager()
issn_mngr = ISSNManager()

for file in access_csv(source_paths):
    with open(file, 'r', encoding='utf-8') as source_file:
        data_dict = DictReader(source_file)

        for position_in_table, row in enumerate(data_dict):
            print(row)
            field_id = row['id']
            # print(field_id)

            for position_in_field, id_instance in enumerate(field_id.split()):
                print(id_instance)

                if match("^doi:", id_instance):
                    normalized_id_instance = doi_mngr.normalise(id_instance)

                    if doi_mngr.is_valid(normalized_id_instance) is None:
                        print(
                            f'Take a look at id no. {position_in_field} at row no. {position_in_table} in file {file}')

                if match("^issn:", id_instance):
                    normalized_id_instance = issn_mngr.normalise(id_instance)
                    if issn_mngr.is_valid(normalized_id_instance) is None:
                        print(
                            f'Take a look at id no. {position_in_field} at row no. {position_in_table} in file {file}')

                if match("^isbn:", id_instance):
                    print(f'Take a look at id no. {position_in_field} at row no. {position_in_table} in file {file}')
                    print("A ISBN manager is yet to be developed")
