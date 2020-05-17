######################################################################

# For hypothesis 2

######################################################################


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
# remove potential duplicates
module_ids = list(dict.fromkeys(module_ids))

print("\n\n\033[1;35;40m " + str(len(module_ids)) + " modules found in " + input_file + " \n")
print("\033[1;35;40m Start processing. \n\n")

data = {}

for module_id in module_ids:
    print("\033[1;35;40m Processing " + module_id + "...")
    module = Module(module_id)

    # print(module.get_aggregated_semester_information())

    for (key, value) in module.get_aggregated_semester_information().items():
        # print('looking at', key)
        ratings_sum = 0
        ratings_count = 0
        ratings_average = 0
        if 'ratings' in value:
            for rating in value['ratings']:
                ratings_sum += rating['score']
                ratings_count += 1
            ratings_average = round(ratings_sum / ratings_count, 2)
        # print('found', ratings_count, 'ratings with an average of', ratings_average)

        grades_average = 0
        grades_total = 0
        grades_passed = 0
        grades_failed = 0
        if 'gradesDetail' in value:
            grades_average = value['gradesDetail']['average']
            grades_passed = value['gradesDetail']['passed']
            grades_failed = value['gradesDetail']['failed']
            grades_total = grades_passed + grades_failed
        # print('from', grades_total, 'students', grades_passed, 'passed and the average was', grades_average)

        module_semester_hash = str(module_id) + key
        data[module_semester_hash] = {
            'moduleId': module_id,
            'semester': key,
            'averageRatings': ratings_average,
            'totalRatings': ratings_count,
            'averageGrades': grades_average,
            'totalGrades': grades_total,
            'passedGrades': grades_passed,
            'failedGrades': grades_failed,
        }

fieldnames = [
    'moduleId',
    'semester',
    'averageRatings',
    'totalRatings',
    'averageGrades',
    'totalGrades',
    'passedGrades',
    'failedGrades'
]

write_header_to_output_file(output_file, fieldnames)

for key, value in data.items():
    write_data_to_output_file(output_file, value, fieldnames)

print("\n\n\033[1;32;40m Process finished successful.\n")
print("\033[1;32;40m Check " + output_file + " for the results.")
print("\033[1;32;40m Check the /json folder for formatted output.")
















