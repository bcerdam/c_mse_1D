#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

double calculate_standard_deviation(double* values, int size) {
    double mean = 0.0;
    double sum = 0.0;

    for (int i = 0; i < size; i++) {
        mean += values[i];
    }
    mean /= size;

    for (int i = 0; i < size; i++) {
        double diff = fabs(values[i] - mean);
        sum += diff * diff;
    }

    double variance = sum / size;
    double standard_deviation = sqrt(variance);

    return standard_deviation;
}


double distance(int m, double* data, int i, int a, int distance_type) {
    if (distance_type == 0){
        double max_dist = 0;
        for(int n = 0; n < m; n++){
            double dist = fabs(data[i+n] - data[a+n]);
            if(dist > max_dist) {
                max_dist = dist;
            }
        }
        return max_dist;
    }
    else{
        double sum_dist = 0;
        for(int n = 0; n < m; n++){
            double dist = powf(fabs(data[i+n] - data[a+n]), distance_type);
            sum_dist += dist;
        }
        sum_dist = powf(sum_dist, (1.0/distance_type));
        return sum_dist;
    }
}

double* calculate_distance_m(double* data, int i, int m, int num_entries, int distance_type) {
    double* dists_array = (double*)malloc((num_entries-m-1) * sizeof(double));
    int co = 0;
    for(int a = 0; a < num_entries-m; a++){
        if(a == i){
            continue;
        }
        else{
            double dist = distance(m, data, i, a, distance_type);
            dists_array[co] = dist;
            co += 1;
        }
    }
    return dists_array;
}

double distance_m(double* data, int m, int num_entries, int distance_type) {
    int size = num_entries - m;
    double** pos = (double**)malloc(size * sizeof(double*));
    int c = 0;

    for (int i = 0; i < num_entries - m; i++){
        pos[c] = calculate_distance_m(data, i, m, num_entries, distance_type);
        c += 1;
    }

    int quant = (num_entries-m)*(num_entries-m);
    double* distances_flattened = (double*)malloc(quant * sizeof(double));
    int co = 0;
    for(int i = 0; i < size; i++){
        for(int j = 0; j < size; j++){
            distances_flattened[co] = pos[i][j];
            co += 1;
        }
    }
    
    for(int i = 0; i < size; i++){
        free(pos[i]);
    }
    free(pos);
    return calculate_standard_deviation(distances_flattened, quant);
}

double unique_values_std(double* signal_array, int num_entries){
    return calculate_standard_deviation(signal_array, num_entries);
}
