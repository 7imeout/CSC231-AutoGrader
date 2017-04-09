#!/usr/local/bin/python3

import filecmp, json, os, sys
from diff_adt import DiffConfig, DiffResult
from time import localtime, strftime
from subprocess import call

CURRENT_TIMESTAMP = strftime("%Y-%m-%d-%H%M", localtime())
DEBUG_MODE = False


def main():
    print('Getting config and preparing run ...', end=' ')
    config = get_config()
    print('done!')

    print('Initiating grading', *config.labs, '...', end='\n\n')

    print('Running MATLAB script ...', end='\n\n')
    print('\n\nMATLAB run ' + ('finished!' if generate_MATLAB_output() else '\n\nFAILED!'), end='\n\n')

    print('Comparing results and writing output ...', end=' ')
    result = DiffResult()

    for lab in config.labs:
        diff_lab_outputs(result, lab[:-2], config)

    output_result_to_csv(result, config)
    print('ALL DONE!', end='\n\n')


def generate_MATLAB_output():
    script = 'generate_output_vm.m' if sys.argv[1].lower() == '-vm' else 'generate_output.m'
    return not call(['matlab', '-nodesktop', '-nosplash', '-nodisplay', '-r',
                     "try, run('./{}'), catch exc, getReport(exc), end, exit".format(script)])


def diff_lab_outputs(result_obj, lab_dir_name, config):
    submissions_dir = config.submissions_dir
    solutions_dir = config.solutions_dir
    results_dir = config.results_dir

    files = [f for f in os.listdir(results_dir)
             if os.path.isfile(os.path.join(results_dir, f)) and lab_dir_name in f]

    solution_file = solutions_dir + lab_dir_name + '.out.txt'
    alt_solution_file = solutions_dir + lab_dir_name + '.alt.txt'

    for f in files:
        second_underscore_index = f.find('_', f.index('_') + 1)
        author_name = f[:second_underscore_index]

        if DEBUG_MODE:
            print('comparing', solution_file, 'and', submissions_dir + f, end='')

        if os.path.isfile(alt_solution_file):
            diff_result = filecmp.cmp(solution_file, results_dir + f) \
                          or (filecmp.cmp(alt_solution_file, results_dir + f))
        else:
            diff_result = filecmp.cmp(solution_file, results_dir + f)

        if DEBUG_MODE:
            print(' ... comparison result', diff_result)

        result_obj.add_result(author_name, lab_dir_name, diff_result)


def output_result_to_csv(result_obj, config):
    if DEBUG_MODE:
        print('Final Result Object:\n', result_obj)

    result = result_obj.result
    csv = open(config.csv_path + CURRENT_TIMESTAMP + '_' + config.csv_name, 'w')
    write_to_csv(csv, config.csv_header)

    result_tuple_list = sorted([(k, v) for k, v in result.items()])

    for author_name, diff_results in result_tuple_list:
        write_to_csv(csv, author_name + ',' + per_author_result_to_csv_entry(config.labs, diff_results))

    csv.close()


def per_author_result_to_csv_entry(lab_file_names, author_result):
    csv_entry_str = ''
    for lab_file_name in lab_file_names:
        lab = lab_file_name[:-2]
        csv_entry_str += str(author_result[lab]) if lab in author_result else ''
        csv_entry_str += ','
    return csv_entry_str


def write_to_csv(csv_file, line_to_write):
    if DEBUG_MODE:
        print(line_to_write)
    csv_file.write(line_to_write + '\n')


def get_config():
    with open('diff_config.json') as data_file:
        data = json.load(data_file)

    # get the list of lab file names
    lab_file_names = []
    for num in data['labs']:
        lab_file_names.append('lab{:02}.m'.format(num) if num else 'final.m')

    # also write to .dat file for MATLAB to read which items to execute
    lab_list_dat = open(data['submissions_dir'] + 'lab_list.dat', 'w')
    for name in lab_file_names:
        lab_list_dat.write(name + '\n')
    lab_list_dat.close()

    return DiffConfig(lab_file_names,
                      data['submissions_dir'], data['solutions_dir'], data['results_dir'],
                      data['result_csv_path'], data['result_csv_name'])


if __name__ == '__main__':
    main()
