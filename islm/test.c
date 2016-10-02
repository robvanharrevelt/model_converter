#include <stdio.h>
#include <time.h>
#include "islm.h"

#define REP 1000

int main(void) {
    double y[7], y_in[7] = {0}, x[2]= {0}, d[3] = {0}, a[4] = {0},  
           fixval[4] = {0}, p[14] = {10};
    int fix[4] = {0};

    int i;
    for (i = 0; i < 14; i++) {
        p[i] = 10;
    }
    x[1] = 0.2;

    clock_t start = clock(), diff;
    for (i = 0; i < REP; i++) {
        run_model_c(y, y_in, x, d, a, fix, fixval, p);
    }
    diff = clock() - start;


    double sum = 0;
    for (i = 0; i < 7; i++) {
        sum = sum + y[i];
    }
    printf("sum = %g\n", sum);
    double msec = 1e6 * diff / (REP * CLOCKS_PER_SEC);
    printf("Time taken  in microseconds %g\n", msec);
}
