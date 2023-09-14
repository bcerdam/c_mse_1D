import os
import time
import numpy as np
import subprocess
import utils
import json

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


# ['HRVSB', 'HRVSC', 'HRVSE']

# Promedio: [0.8776156435954757, 0.8638387142837791, 0.9292345608368804]

# Desviacion Estandar: [0.036897335874133394, 0.034874328840382926, 0.04398955255410731]

# Varianza: [0.0016309201594386243, 0.0016602733746504852, 0.002341552903543662]


# import os
#
# folder_path = '/Users/brunocerdamardini/Desktop/repo/c_mse_1D/datos/HRV/hrv_sc_wp'
# for item in os.listdir(folder_path):
#     item_path = os.path.join(folder_path, item)
#
#     if 'B' in item:
#         file = np.genfromtxt(item_path, delimiter=',')
#         b.append(np.mean(file))
#     elif 'C' in item:
#         file = np.genfromtxt(item_path, delimiter=',')
#         c.append(np.mean(file))
#     elif 'E' in item:
#         file = np.genfromtxt(item_path, delimiter=',')
#         e.append(np.mean(file))
