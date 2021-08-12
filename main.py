import numpy as np
from nptdms import TdmsFile
import read as read
import write as write
import tools as tools

# Path information
linear_paths = ['1st_order/']
nonlin_paths = ['Interactions/Normals/', 'Interactions/Normal-Roll/', 'Interactions/Side-Roll/']

# Load tdms data files, first ZLO
print("\nLoading ZLO file...")
ZLO = read.Data(path='ZLO/', name='ZLO')
ZLO.average_all()

# Linear sets (single loads)
print("\nDetermining linear data files from paths ", linear_paths)
linear_names, linear_signs, linear_str_id = tools.determine_files(paths=linear_paths)

# Nonlinear or Interaction sets (multiple simultaneous loadings)
print("\nDetermining nonlinear data files from paths ", nonlin_paths)
nonlin_names, nonlin_signs, nonlin_str_id = tools.determine_files(paths=nonlin_paths)

# Read files and adjust files
print("\nLoading linear data files...")
linear_data = tools.read_all_files(paths=linear_paths, file_names=linear_names,
                                   file_str_ids=linear_str_id, file_signs=linear_signs)
print("\nLoading nonlinear data files...")
nonlin_data = tools.read_all_files(paths=nonlin_paths, file_names=nonlin_names,
                                   file_str_ids=nonlin_str_id, file_signs=nonlin_signs)
# print(nonlin_data)
# quit()
print('\nWriting BALFIT input file...')
Writer = write.InputFile(path='', name='InputTest', zlo_file=ZLO, linear_data=linear_data, nonlin_data=nonlin_data)
                         # data_files=linear_data, str_ids=linear_str_id, signs=linear_signs)
Writer.preamble(comments=['I am a fish', 'I am a shoe'])
Writer.file_comments(comments=['DATA ORIGIN = 3x3 Tunnel'])
Writer.headers()
print('Writing ZLOs...')
Writer.write_zlo()
print('Writing linear (single vector) loadings...')
Writer.write_data()
print('Writing nonlinear (interactions) loadings...')

# Trash Bin
# print(file_names)
# print(file_str_id)
# print(file_signs)
# quit()
# Nonlinear / interaction sets (two or more applied loads)
# path_i0 = 'Interactions/'
# path_i_nr = 'Normal-Roll/'
# path_i_sr = 'Side-Roll/'
# inter_nr = ['+NF1_+RM', '+NF1_-RM', '+NF2_+RM', '+NF2_-RM', '-NF1_+RM', '-NF1_-RM', '-NF2_+RM', '-NF2_-RM']
# for i in range(len(inter_names)):
#     inter_names[i] = path_i0 + path_i_nr + inter_names[i]
# inter_sr = ['+SF1_+RM', '+SF1_-RM', '+SF2_+RM', '+SF2_-RM', '-SF1_+RM', '-SF1_-RM', '-SF2_+RM', '-SF2_-RM']

# file_names = ['+AF', '-AF', '+NF1', '-NF1', '+NF2', '-NF2', '+Rm', '-Rm', '+SF1', '-SF1', '+SF2', '-SF2']
# file_str_id = [5, 5, 0, 0, 1, 1, 4, 4, 2, 2, 3, 3]
# file_signs = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1]
