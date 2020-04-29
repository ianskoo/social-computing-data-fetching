import csv

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

def write_header_to_output_file(filename, fieldnames):
    '''

    :param filename:
    :param fieldnames: list of the fieldnames keys
    :return:
    '''
    with open(filename, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()


def write_data_to_output_file(filename, data, fieldnames):
    with open(filename, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';', extrasaction='ignore')

        writer.writerow(data)
