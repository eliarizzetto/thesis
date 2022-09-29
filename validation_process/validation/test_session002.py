import glob
from random import sample, choices
from csv import DictReader, DictWriter

source_paths = 'C:/Users/media/Desktop/thesis23/meta_input'

source_data = glob.glob(f'{source_paths}/**/*.csv', recursive=True)
sample_list_of_paths = []
for file_path in sample(source_data, k=5):
    sample_list_of_paths.append(file_path)

print("sample paths: ", sample_list_of_paths)

temp_list = []
for f in sample_list_of_paths:
    with open(f, 'r', encoding='utf-8') as source_file:
        data_dict = DictReader(source_file)
        data_list = list(data_dict)
        temp_list.append(sample(data_list, k=20))



with open("test_files/test_session002.csv", "x", encoding="utf-8") as f:
    fieldnames = ['id',"title","author","pub_date","venue","volume","issue","page","type","publisher","editor"]
    writer = DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for l in temp_list:
        for row in l:
            writer.writerow(row)
