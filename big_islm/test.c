#include <stdio.h>
#include <time.h>
#include "big_islm.h"

#define REP 1000

int main(void) {
    double y[3500], y_in[3500] = {0}, x[1000]= {0}, d[1500] = {0}, 
           a[2000] = {0},  fixval[2000] = {0}, p[14] = {10};
    int fix[2000] = {0};

    int i;
    for (i = 0; i < 14; i++) {
        p[i] = 10;
    }
    for (i = 500; i < 1000; i++) {
        x[i] = 0.2;
    }

    clock_t start = clock(), diff;
    for (i = 0; i < REP; i++) {
        run_model_c(y, y_in, x, d, a, fix, fixval, p);
    }
    diff = clock() - start;


    double sum = 0.0;
    for (i = 0; i < 3500; i++) {
        sum = sum + y[i];
    }
    printf("sum = %g\n", sum);
    double msec = 1e3 * diff / (REP * CLOCKS_PER_SEC);
    printf("Time taken  in milliseconds %g\n", msec);
}
