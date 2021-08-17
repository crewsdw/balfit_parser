import numpy as np
from nptdms import TdmsFile


class Data:
    def __init__(self, path, name):
        # path
        file_path = path + name + '.tdms'
        # file
        self.tdms = TdmsFile.read(file_path)
        # properties
        self.properties = self.tdms.properties

        # groups
        self.groups = self.tdms.groups()
        self.paths = [self.groups[i].path
                      for i in range(len(self.groups))]
        # loadings
        self.num_variations = len(self.paths)
        self.variations = [self.paths[i].split('\'')[1]
                        for i in range(len(self.paths))]  # loadings types

        # channels
        self.channels = [self.groups[i].channels()
                         for i in range(len(self.paths))]

        # loads
        self.data_paths = [self.channels[0][i].path
                           for i in range(len(self.channels[0]))]
        self.data_labels = [self.data_paths[i].split('\'')[3]
                            for i in range(len(self.channels[0]))]
        self.data_properties = [self.channels[0][i].properties
                                for i in range(len(self.channels[0]))]
        self.units = [self.data_properties[i]['unit_string']
                      for i in range(len(self.channels[0]))]

        self.size = len(self.data_paths)

        # Collect all data
        self.data = [[self.data_labels[s], [np.array(self.channels[k][s][:])
                                            for k in range(len(self.variations))]]
                     for s in range(self.size)]

        # Init only
        self.averages = None
        self.tared_data = None

    def average_all(self):
        self.averages = [[self.data_labels[s], [np.mean(np.array(self.channels[k][s][:]))
                                                for k in range(self.num_variations)]]
                         for s in range(self.size)]
        # self.averages = [[self.data_labels[s], [np.mean(np.array(self.tared_data[s][1][k]))
        #                                         for k in range(self.num_variations)]]
        #                  for s in range(self.size)]

    def tare_all(self):
        if self.averages is None:
            print('Err: First compute averages')
            quit()
        else:
            # print(self.data[1][1][0])
            # quit()
            self.tared_data = [[self.data_labels[s], [self.averages[s][1][k] - self.averages[s][1][0] * np.heaviside(6-s, 0.0)
                                                      for k in range(self.num_variations)]]
                               for s in range(self.size)]
            # print(self.size)
            # print(self.averages)
            # print(self.tared_data)
            # quit()
            # self.tared_channels = [self.data[s][k] - ]
            # quit()

# Trash bin

        # debug
        # print(self.paths)
        # print(self.variations)
        # print(self.groups)
        # print(self.channels)
        # print(self.channels[0][0][:])
        # print(self.data_paths)
        # print(self.data_labels)
        # print(self.groups[0])
        # print(self.tdms[self.groups[0]])

        # quit()
