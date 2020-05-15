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

    # print(getattr(module, 'gradeStatistics'))
    # print(getattr(module, 'ratingSummary'))
    #
    # gradesCount = getattr(module, 'gradeStatistics_count')
    # gradesAverage = getattr(module, 'gradeStatistics_average')
    # gradesPassed = getattr(module, 'gradeStatistics_passed')
    # gradesFailed = getattr(module, 'gradeStatistics_failed')

    # reviewTotal = getattr(module, 'ratingSummary_total')
    # reviewAverage = getattr(module, 'ratingSummary_average')

    for rating in module.get_ratings():
        if not rating['grade']:
            # skipping because we don't know the authors grade.
            continue
        ratingId = rating['_id']
        score = rating['score']
        grade = rating['grade']
        if 'voteScore' in rating: voteScore = rating['voteScore']
        else: voteScore = 0
        if 'ups' in rating: ups = rating['ups']
        else: ups = 0
        if 'downs' in rating: downs = rating['downs']
        else: downs = 0

        data[ratingId] = {
            'ratingId': ratingId,
            'moduleId': module_id,
            'score': score,
            'grade': grade,
            'voteScore': voteScore,
            'ups': ups,
            'downs': downs
        }
    # print('\n\n\n\n\n')

fieldnames = [
    'ratingId',
    'moduleId',
    'score',
    'grade',
    'voteScore',
    'ups',
    'downs'
]

write_header_to_output_file(output_file, fieldnames)

for key, value in data.items():
    write_data_to_output_file(output_file, value, fieldnames)

print("\n\n\033[1;32;40m Process finished successful.\n")
print("\033[1;32;40m Check " + output_file + " for the results.")
print("\033[1;32;40m Check the /json folder for formatted output.")
















