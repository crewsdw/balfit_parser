import numpy as np
import os
import re  # parsing for regular expressions
import read as read

# List of possible headers
# NF1 = N1, NF2 = N2, SF1 = S1, SF2 = S2, RM = L1, AF = A1
headers = ['NF1', 'NF2', 'SF1', 'SF2', 'RM', 'AF']


def read_all_files(paths, file_names, file_str_ids, file_signs):
    """
    Read all files from list "file_names" and adjust data (fixing headers / signs) according to str_ids and signs
    :param paths: list of intended file paths, e.g. [['Interactions/Normals'], ['Interactions/Side-Roll']]
    :param file_names: list of file names (i.e. +NF1.tdms)
    :param file_str_ids: list of header IDs (identifications) for correct headers (i.e. NF1)
    :param file_signs: list of numerical signs for correct column (+- 1)
    :return: list of adjusted data files
    """
    data_files = []
    for path_idx, path_set in enumerate(file_names):
        path_files = []
        for file_idx, file_name in enumerate(path_set):
            # Read data file
            data_file = read.Data(path=paths[path_idx], name=file_name)
            # Average data, tare based on zero measurement (assumed first set), and adjust data
            data_file.average_all()
            data_file.tare_all()
            adjust_data(data_file=data_file, file_str_ids=file_str_ids[path_idx][file_idx],
                        file_sign=file_signs[path_idx][file_idx])
            # Accumulate this data file
            path_files += [data_file]
        data_files += [path_files]
    return data_files


def determine_files(paths):
    """
    Read all files in specified path and obtain their signs and strings
    :param paths: filepath relative to current working directory
    :return: list of lists: per path files, signs, and header strings
    """
    # get directory
    cwd = os.getcwd()

    # get filenames without extension
    all_files, all_signs, all_strings = [], [], []
    for path in paths:
        # Get file names
        files = []
        for file in os.listdir(cwd + '/' + path):
            if file.endswith('.tdms'):
                files += [os.path.splitext(file)[0]]
        # Get their associated sign and string indexes
        signs, strings = signs_and_strings(files)
        # Accumulate
        all_files += [files]
        all_signs += [signs]
        all_strings += [strings]

    return all_files, all_signs, all_strings


def signs_and_strings(files):
    """
    From file info, obtain their numerical signs and strings based on the given filename
    :param files: list of filenames in folder
    :return: the signs and strings based on filename
    """
    signs, strings = [], []
    for item in files:
        tmp_signs, tmp_strings = [], []
        # check for signs and number of data columns
        for char in item:
            if char == '+':
                tmp_signs += [1.0]
            if char == '-':
                tmp_signs += [-1.0]
        # determine index of header types, first remove +/-'s and _'s
        split_item = re.split('[+_-]', item)
        # now remove empty strings
        while '' in split_item:
            split_item.remove('')
        # grab strings associated with the signs
        # for i in range(len(tmp_signs)):
        #     pure_str = split_item[i]  # +1 for leading ['', ... ]
        #     tmp_strings += [headers.index(pure_str.upper())]
        for idx, pure_str in enumerate(split_item):
            tmp_strings += [headers.index(pure_str.upper())]
        # Accumulate
        signs += [tmp_signs]
        strings += [tmp_strings]
    return signs, strings


def adjust_data(data_file, file_str_ids, file_sign):
    """
    Adjust data object because columns are all screwed up...
    :param data_file: data object for this file
    :param file_str_ids: string ids
    :param file_sign: numerical sign of applied load
    """
    # Grab correct column and zero everything else
    target_arrays = []  # np.zeros(data_file.num_variations)  # init
    for j in range(6):
        if np.amax(np.absolute(data_file.tared_data[j][1])) > 10:  # check if loaded, value > zero-off readings
            target_arrays += [data_file.tared_data[j][1]]
        data_file.tared_data[j][1] = np.zeros_like(data_file.tared_data[j][1])

    # Set value
    # print(data_file.tared_data)
    # print(target_arrays)
    for idx, array in enumerate(target_arrays):
        data_file.tared_data[file_str_ids[idx]][1] = array
        # Fix sign
        if np.sign(data_file.tared_data[file_str_ids[idx]][1])[1] != file_sign[idx]:
            data_file.tared_data[file_str_ids[idx]][1] = -1 * np.array(data_file.tared_data[file_str_ids[idx]][1])
