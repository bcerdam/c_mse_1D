#include <stdio.h>
#include <stdlib.h>
#include <math.h>

double* coarse_graining(double* data, int num_entries, int scale) {
    if (scale == 1) {
        return data;
    }
    int new_num_entries = num_entries / scale;
    double* new_data = (double*)malloc(new_num_entries * sizeof(double));
    for (int i = 0; i < new_num_entries; i++) {
        double sum = 0.0;
        for (int s = i * scale; s < (i + 1) * scale; s++) {
            sum += data[s];
        }
        new_data[i] = sum / (double)scale;
    }
    return new_data;
}

double fuzzy_membership(double distance, double r, double delta, double min, double max) {
    if (r == 0){
        return 1;
    }
    else{
        //
        return expf(powf(distance, 2) * log(delta) / powf(r, 2.0));
        //

        //
        // return expf(-powf((distance/r), 2)); // OG fuzzy function
        //

        // NEUROKIT2 FUZZY MEMBERSHIP FUNCTION: Very bad, does not adjust to 'r'.
        // return expf(-powf(distance, 2)/r);
        //

        // Linear fuzzy membership (UNIQUE_VALUES):
        // return (-1/max)*distance + 1;

        // Linear fuzzy membership (UNIQUE_DISTANCES):
        // return (-1/fabs(max-min))*distance + 1;
    }
}