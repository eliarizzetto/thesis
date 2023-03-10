# Copyright (c) 2023, OpenCitations <contact@opencitations.net>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.

from validator.main import Validator
import time
import statistics
import os
import platform
import psutil
from os.path import join


valid_cits = 'evaluation/test_files/valid_cits.csv'
valid_meta = 'evaluation/test_files/valid_meta.csv'
invalid_cits = 'evaluation/test_files/invalid_cits.csv'
invalid_meta = 'evaluation/test_files/invalid_meta.csv'
meta_with_ids = 'evaluation/test_files/meta_table_with_ids.csv'
meta_no_ids = 'evaluation/test_files/meta_table_no_ids.csv'

files_to_validate = [valid_cits, valid_meta, invalid_cits, invalid_meta]
comparison_api = [meta_with_ids, meta_no_ids]
eval_output_dir = 'evaluation/evaluation_results'


for doc in comparison_api:

    v = Validator(csv_doc=doc, output_dir='tmp')

    # Define a list to store the execution times
    execution_times = []

    # Run your validation software 10 different times
    for i in range(10):
        start_time = time.perf_counter() # Start the timer
        v.validate() # Replace with the path to your csv file
        end_time = time.perf_counter() # Stop the timer
        execution_time = end_time - start_time # Calculate the execution time
        execution_times.append(execution_time) # Add the execution time to the list

    # size of validated file
    file_size = os.path.getsize(doc)
    processor_current_speed = psutil.cpu_freq().current

    with open((join(eval_output_dir, doc[(doc.index('/') + 1):-4]) + '_evaluation.txt'), "w", encoding='utf-8') as f:
        f.write(f"THE TABLE IS: {doc}\n\n")
        f.write(f"File size: {file_size} bytes\n")
        f.write(f"Minimum execution time: {min(execution_times)} seconds\n")
        f.write(f"Maximum execution time: {max(execution_times)} seconds\n")
        f.write(f"Median execution time: {statistics.median(execution_times)} seconds\n")
        f.write(f"Mean execution time: {statistics.mean(execution_times)} seconds\n")
        f.write(f"Standard deviation of execution time: {statistics.stdev(execution_times)} seconds\n")
        f.write(f"\nProcessor Current Speed: {processor_current_speed}")

    # Print the minimum, maximum, median, mean, and standard deviation of the execution times
    print(f"THE TABLE IS: {doc}\n\n")
    print(f"File size: {file_size} bytes\n")
    print(f"Minimum execution time: {min(execution_times)} seconds\n")
    print(f"Maximum execution time: {max(execution_times)} seconds\n")
    print(f"Median execution time: {statistics.median(execution_times)} seconds\n")
    print(f"Mean execution time: {statistics.mean(execution_times)} seconds\n")
    print(f"Standard deviation of execution time: {statistics.stdev(execution_times)} seconds\n")
    print(f"Processor Current Speed: {processor_current_speed})")

# CONTEXTUAL DETAILS

# Get the operating system name and version
os_name = platform.system()
os_version = platform.release()

# Get the computer's processor name and speed
processor_name = platform.processor()
processor_max_speed = psutil.cpu_freq().max
processor_current_speed = psutil.cpu_freq().current


print(f"Operating system: {os_name} {os_version}")
print(f"Processor Current Speed: {processor_current_speed})")


# RUNNING PROCESSES
# Get a list of running processes
# process_list = psutil.process_iter()

# Print the name and process ID of each process
# for process in process_list:
#     # print(f"{process.name()} (PID {process.pid})")
