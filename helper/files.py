import csv
import json
import os

def get_filenames():
    print('\n\nIn which file is the list with the module ids?')
    print('[Enter] for the default "module_list.txt"')
    input_file = str(input('--> '))
    if input_file == '': input_file = 'module_list.txt'


    print('\n\nHow should the output file be named?')
    print('[Enter] for the default "output.CSV"')
    output_file = str(input('--> '))
    if output_file == '': output_file = 'output.CSV'
    if '.' not in output_file: output_file += '.CSV'

    return (input_file, output_file)


def read_module_ids_from_input_file(filename):
    with open(filename, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
        module_ids = []
        for row in csv_reader:
            # print(', '.join(row))
            module_ids.append(row[0])

        return module_ids

semester_list = [
    'FS20',
    'FS19',
    'FS18',
    'FS17',
    'FS16',
    'FS15',
    'FS14',
    'FS13',
    'FS12',
    'FS11',
    'FS10',
    'HS20',
    'HS19',
    'HS18',
    'HS17',
    'HS16',
    'HS15',
    'HS14',
    'HS13',
    'HS12',
    'HS11',
    'HS10'
]

def write_header_to_output_file(filename, fieldnames):
    '''

    :param filename:
    :param fieldnames: list of the fieldnames keys
    :return:
    '''
    with open(filename, 'w') as csv_file:
        # writer = csv.DictWriter(csv_file, fieldnames=fieldnames + semester_list, delimiter=';')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()


def write_data_to_output_file(filename, data, fieldnames):
    with open(filename, 'a') as csv_file:
        # print('\n\n\n --- writing to csv ---')
        # print(data)
        # writer = csv.DictWriter(csv_file, fieldnames=fieldnames + semester_list, delimiter=';', extrasaction='ignore')
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';', extrasaction='ignore')
        writer.writerow(data)

def write_data_to_json(data):
    filename = data['module_id'] if data['module_id'] else 'xxx'
    filepath = filename + '.json'
    if not os.path.exists('json'):
        try:
            os.makedirs('json')
            filepath = './json/' + filename + '.json'
        except OSError:
            pass
    else: filepath = './json/' + filename + '.json'

    with open(filepath, 'w') as f:
        f.write(json.dumps(data, indent=4, sort_keys=True))
