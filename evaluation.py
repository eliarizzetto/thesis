from validator.main import Validator
import time
import statistics
import os
import platform
import psutil

file_to_validate = 'test_files/valid_cits.csv'

v = Validator(csv_doc=file_to_validate, output_dir='software_evaluation')


# Define a list to store the execution times
execution_times = []

# Run your validation software 10 different times
for i in range(10):
    start_time = time.perf_counter() # Start the timer
    v.validate() # Replace with the path to your csv file
    end_time = time.perf_counter() # Stop the timer
    execution_time = end_time - start_time # Calculate the execution time
    execution_times.append(execution_time) # Add the execution time to the list

# Print the minimum, maximum, mean, and standard deviation of the execution times
print(f"Minimum execution time: {min(execution_times)} seconds")
print(f"Maximum execution time: {max(execution_times)} seconds")
print(f"Mean execution time: {statistics.mean(execution_times)} seconds")
print(f"Standard deviation of execution time: {statistics.stdev(execution_times)} seconds")

# CONTEXTUAL DETAILS

# size of validated file
file_size = os.path.getsize(file_to_validate)
print(f"File size: {file_size} bytes")

# Get the operating system name and version
os_name = platform.system()
os_version = platform.release()

# Get the computer's processor name and speed
processor_name = platform.processor()
processor_max_speed = psutil.cpu_freq().max
processor_current_speed = psutil.cpu_freq().current


print(f"Operating system: {os_name} {os_version}")
print(f"Processor: {processor_name} (Max speed: {processor_max_speed} MHz; Current speed: {processor_current_speed})")


# RUNNING PROCESSES
# Get a list of running processes
# process_list = psutil.process_iter()

# Print the name and process ID of each process
# for process in process_list:
#     # print(f"{process.name()} (PID {process.pid})")
