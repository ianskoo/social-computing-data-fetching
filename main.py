import os
from pprint import pprint
from entities.module import Module
from helper.files import *

# get filename by console input
input_filename, output_filename = get_filenames()

cwd = os.getcwd()
input_file = cwd + '/' + input_filename
output_file = cwd +  '/' + output_filename

module_ids = read_module_ids_from_input_file(input_file)

print("\n\n\033[1;35;40m " + str(len(module_ids)) + " modules found in " + input_file + " \n")
print("\033[1;35;40m Start processing. \n\n")

"""
the array 'fieldnames' below determines which fields will be written to the output file
simply uncomment / comment in order to activate / deactivate.
"""
fieldnames = [
    'module_id', # unique id of the module
    # 'departments', # departement (usually null)
    'faculty', # f.ex. "Recht" or "Wirtschaft"
    # 'gradeStatistics',
    'gradeStatistics_average', # all grades averaged
    'gradeStatistics_count', # number of grades available
    'gradeStatistics_failed', # number of failed grades (grade < 4.0)
    'gradeStatistics_passed', # number of passed grades (grade >= 4.0)
    'messages', # amount of messages sent in chat
    'name', # name of the module (f.ex. "Labor and Employment Law")
    # 'ratingSummary',
    'ratingSummary_average', # average of all ratings
    'ratingSummary_total', # amount of ratings
    # 'shortName', # f.ex. "Labor and Employment Law"
    # 'type', # f.ex. "COURSE"
    # 'userCount',
    'userCount_all', # amount of bestande users who booked this module
    'aggregatedSemesterInformation',
]


write_header_to_output_file(output_file, fieldnames)
for module_id in module_ids:
    print("\033[1;35;40m Processing " + module_id + "...")
    module = Module(module_id)

    data = {}
    for attr in fieldnames:

        if attr == 'aggregatedSemesterInformation':
            for key, value in getattr(module, attr).items():
                data[key] = value
            continue

        data[attr] = getattr(module, attr)

    write_data_to_output_file(output_file, data, fieldnames)

    write_data_to_json(data)

print("\n\n\033[1;32;40m Process finished successful. Check " + output_file + " for the results.\n")
















