#include <stdio.h>
#include <stdlib.h>
#include <string.h>

double* read_csv(const char* filepath, int num_entries) {
    FILE* file = fopen(filepath, "r");
    if (file == NULL) {
        printf("Error opening file: %s\n", filepath);
        return NULL;
    }

    double* data = (double*)malloc(num_entries * sizeof(double));
    if (data == NULL) {
        printf("Memory allocation failed.\n");
        fclose(file);
        return NULL;
    }

    char line[256];
    char* token;
    int i = 0;

    while (fgets(line, sizeof(line), file) != NULL && i < num_entries) {
        token = strtok(line, ",");
        while (token != NULL && i < num_entries) {
            data[i] = atof(token);
            token = strtok(NULL, ",");
            i++;
        }
    }

    fclose(file);
    return data;
}