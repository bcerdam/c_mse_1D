import os
import time
import numpy as np
import subprocess
import utils

def info_matriz(csv_path):
    data_array = np.genfromtxt(csv_path, delimiter=',')
    num_elements = data_array.shape[0]
    return (num_elements, data_array.min(), data_array.max())


def run_c_program(csv_path, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, std_type=1):
    info = info_matriz(csv_path)
    command = [os.path.join(os.path.dirname(os.getcwd()), 'core_c', 'executables', 'mse_1d_p'), csv_path, str(scales), str(m), str(r), str(fuzzy), str(method),
               str(delta), str(distance_type), str(m_distance), str(info[0]), str(std_type), str(info[1]), str(info[2])]
    result = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    n_values = list(result.split())
    n_values = [float(x) for x in n_values]
    return n_values

def mse_1d(folder_path, scales, m, r, fuzzy, method, delta=0.7, distance_type=0, m_distance=2, std_type='UNIQUE_VALUES'):
    # Fuzzy params
    if fuzzy == True:
        fuzzy = 1
    else:
        fuzzy = 0

    # Method params: MSE (MultiScale Entropy), CMSE (Composite MultiScale Entropy), RCMSE (Refined Composite MultiScale Entropy)
    if method in ['CMSE', 'RCMSE']:
        if method == 'CMSE':
            method = 1
        elif method == 'RCMSE':
            method = 2
    else:
        method = 0

    if std_type == 'UNIQUE_DISTANCES':
        std_type = 1
    elif std_type == 'UNIQUE_VALUES':
        std_type = 0

    mse_values = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        print('Working on: ', filename)
        start_time = time.time()

        mse_values.append([filename, run_c_program(file_path, scales, m, r, fuzzy, method, delta, distance_type, m_distance, std_type)])

        end_time = time.time()
        execution_time = end_time - start_time
        print(execution_time)

    return mse_values

# compilar con:
# gcc -o core_c/executables/mse_1d core_c/scripts/mse_1d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c  -lm -Icore_c/headers
# clang -Xclang -fopenmp -I/usr/local/opt/libomp/include -L/opt/homebrew/Cellar/libomp/16.0.6/lib -lomp -Icore_c/headers core_c/scripts/mse_1d.c core_c/scripts/read_csv.c core_c/scripts/signal_std.c core_c/scripts/utils.c -o core_c/executables/mse_1d_p

# v = mse_1d('/Users/brunocerdamardini/Desktop/repo/c_mse_1D/datos/HRV/hrv_sc_wp', 10, 2, 0.05, True, 'RCMSE', delta=0.8, std_type='UNIQUE_VALUES')
# mse_b = []
# mse_c = []
# mse_e = []
# for x in v:
#     if 'B' in x[0]:
#         mse_b.append(np.array(x[1]))
#     elif 'C' in x[0]:
#         mse_c.append(np.array(x[1]))
#     elif 'E' in x[0]:
#         mse_e.append(np.array(x[1]))
#
# import numpy as np
#
#
# def calculate_average_positions(arrays_list):
#     """
#     Calculate the average of positions across the given list of one-dimensional NumPy arrays.
#     Args:
#         arrays_list (list): A list of one-dimensional NumPy arrays.
#     Returns:
#         numpy.ndarray: An array representing the averaged values at each position.
#     """
#     # Ensure all arrays have the same length
#     array_lengths = set(len(arr) for arr in arrays_list)
#     if len(array_lengths) > 1:
#         raise ValueError("All arrays must have the same length.")
#     # Stack the arrays into a 2D array where each row corresponds to one array
#     stacked_arrays = np.stack(arrays_list)
#     # Calculate the average along the first axis (axis=0) to get the average of positions
#     averaged_positions = np.mean(stacked_arrays, axis=0)
#     return averaged_positions
#
#
# b_array = calculate_average_positions(mse_b)
# c_array = calculate_average_positions(mse_c)
# e_array = calculate_average_positions(mse_e)
# v = [['hrvsb', list(b_array)], ['hrvsc', list(c_array)], ['hrvse', list(e_array)]]
# utils.plot_arrays(v, title='Fuzzy RCMSE 1D ; m=2 ; r=0.15 ; delta=0.8 ; std=valores_unicos', xlabel='Scales', ylabel='Entropy')
