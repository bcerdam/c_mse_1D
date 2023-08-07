#ifndef SIGNAL_STD_FUNCS_H
#define SIGNAL_STD_FUNCS_H

double calculate_standard_deviation(double* values, int size);
double distance(int m, double* data, int i, int a, int distance_type);
double* calculate_distance_m(double* data, int i, int m, int num_entries, int distance_type);
double distance_m(double* data, int m, int num_entries, int distance_type);
double unique_values_std(double* signal_array, int num_entries);

#endif