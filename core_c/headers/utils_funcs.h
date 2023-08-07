#ifndef UTILS_FUNCS_H
#define UTILS_FUNCS_H

double* coarse_graining(double* data, int num_entries, int scale);
double fuzzy_membership(double distance, double r, double delta, double min, double max);

#endif