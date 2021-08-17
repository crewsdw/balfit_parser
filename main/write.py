import numpy as np
import csv


class InputFile:
    def __init__(self, path, name, zlo_file, linear_data, nonlin_data):  # data_files, str_ids, signs):
        self.file_path = path + name + '.csv'

        # Names of variables
        self.var_names = ['N1', 'N2', 'S1', 'S2', 'RM', 'AF', 'rN1', 'rN2', 'rS1', 'rS2', 'rRM', 'rAF']
        self.var_types = ['N1(indep.)', 'N2(indep.)', 'S1(indep.)', 'S2(indep.)', 'RM(indep.)', 'AF(indep.)',
                          'rN1(dep.)', 'rN2(dep.)', 'rS1(dep.)', 'rS2(dep.)', 'rRM(dep.)', 'rAF(dep.)']
        self.load_capacities = ['200', '200', '200', '200', '60', '50']  # lbs (0-3), in-lbs (4), lbs (5)

        # zero load-off (ZLO) information
        self.orientations = zlo_file.variations
        self.orientations[0] = '0'
        self.num_orientations = zlo_file.num_variations
        self.zlo_averages = [zlo_file.averages[s][1]
                             for s in range(zlo_file.size)]

        # linear fileset information
        self.linear_variations = [[data.num_variations for data in path_elements] for path_elements in linear_data]
        self.tared_linear_data = [[[data.tared_data[s][1]
                                    for s in range(data.size)]
                                   for data in path_elements]
                                  for path_elements in linear_data]

        # nonlinear fileset information
        self.nonlin_variations = [[data.num_variations for data in path_elements] for path_elements in nonlin_data]
        self.tared_nonlin_data = [[[data.tared_data[s][1]
                                    for s in range(data.size)]
                                   for data in path_elements]
                                  for path_elements in nonlin_data]

        # Empty sizes
        self.four_empty = ['', '', '', '']
        self.six_empty = ['', '', '', '', '', '']

    def preamble(self, comments=''):
        with open(self.file_path, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONE)
            writer.writerow(['; BALFIT Input File for 3x3 Tunnel Calibration'])
            if comments:
                for itm in comments:
                    writer.writerow(['; ' + itm])

    def file_comments(self, comments=''):
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONE)
            if comments:
                for itm in comments:
                    writer.writerow([';; ' + itm])

    def headers(self,
                file_type='DATA_FOR_ITERATIVE_REGRESSION_ANALYSIS',
                balance_name='StudentTunnel',
                description='Data2017'):
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONE)
            # Header variables
            writer.writerow('')
            writer.writerow(['; header variables'])
            writer.writerow(['FILE_TYPE', file_type])
            writer.writerow(['BALANCE_NAME', balance_name])
            writer.writerow(['DESCRIPTION', description])
            # data variable names
            writer.writerow('')
            writer.writerow(['; load and gage output symbols'])
            writer.writerow(['', '', '', ''] + self.var_names)
            # data variable units
            writer.writerow('')
            writer.writerow(['; load and gage output units'])
            writer.writerow(['', '', '', ''] + ['lbs', 'lbs', 'lbs', 'lbs', 'in-lbs', 'lbs',
                                                'microV/V', 'microV/V', 'microV/V', 'microV/V', 'microV/V', 'microV/V'])
            # Load capacities
            writer.writerow('')
            writer.writerow(['; load capacities'])
            writer.writerow(['', '', '', ''] + self.load_capacities)

    def write_zlo(self):
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONE)
            # Zero load-off values
            writer.writerow(['; zero load-off averages'])
            writer.writerow([';', 'point id', 'series', 'orientation'] + ['', '', '', '', '', ''] + self.var_names[6:])
            for s in range(self.num_orientations - 1):
                if float(self.orientations[s]) < 0:
                    self.orientations[s] = int(self.orientations[s]) % 360  # if negative angle make positive
                line = ['', 'NZ-' + str(s + 1).zfill(4), 'A', str(self.orientations[s])] + self.six_empty
                for k in range(6):
                    line += [str(self.zlo_averages[6:][k][s])]
                writer.writerow(line)

    def write_data(self):
        with open(self.file_path, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_NONE)
            # Zero load-off values
            writer.writerow(['; data for analysis (series 1 = load series number '
                             'and series 2 = natural zero series number)'])
            writer.writerow([';', 'point id', 'series 1', 'series 2'] + self.var_types)
            # Start counting point ID
            point_idx = 1
            var_counter = 1
            # Write linear data
            for path_idx, path_elements in enumerate(self.linear_variations):
                for vars_idx, variations in enumerate(path_elements):
                    for s in range(variations):
                        line = ['', 'P-' + str(point_idx).zfill(4), str(var_counter), 'A']  # + self.six_empty
                        for k in range(12):
                            # line += [str(self.linear_averages[i][k][s])]
                            line += [str(self.tared_linear_data[path_idx][vars_idx][k][s])]
                        writer.writerow(line)
                        point_idx += 1
                    var_counter += 1
            # print('Made it through linear data')
            # Write nonlinear (interactions) data
            for path_idx, path_elements in enumerate(self.nonlin_variations):
                for vars_idx, variations in enumerate(path_elements):
                    for s in range(variations):
                        line = ['', 'P-' + str(point_idx).zfill(4), str(var_counter), 'A']  # + self.six_empty
                        for k in range(12):
                            # line += [str(self.linear_averages[i][k][s])]
                            line += [str(self.tared_nonlin_data[path_idx][vars_idx][k][s])]
                        writer.writerow(line)
                        point_idx += 1
                    var_counter += 1

# Trash bin
#     def adjust_data(self):
#         """
#         Adjust the data column and sign because it's all messed up...
#         """
#         for i in range(len(self.linear_variations)):
#             for s in range(self.linear_variations[i]):
# for i in range(len(self.linear_variations)):
#     for s in range(self.linear_variations[i]):
#         line = ['', 'P-' + str(point_idx).zfill(4), str(i + 1), 'A']  # + self.six_empty
#         for k in range(12):
#             # line += [str(self.linear_averages[i][k][s])]
#             line += [str(self.tared_linear_data[i][k][s])]
#         writer.writerow(line)
#         point_idx += 1
# Write nonlinear data
