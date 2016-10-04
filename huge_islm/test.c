#include <stdio.h>
#include <time.h>
#include "huge_islm.h"

#define REP 1000

int main(void) {
    double y[14000], y_in[14000] = {0}, x[4000]= {0}, d[6000] = {0}, 
           a[8000] = {0},  fixval[8000] = {0}, p[14] = {10};
    int fix[8000] = {0};

    int i;
    for (i = 0; i < 14; i++) {
        p[i] = 10;
    }
    for (i = 2000; i < 4000; i++) {
        x[i] = 0.2;
    }

    clock_t start = clock(), diff;
    for (i = 0; i < REP; i++) {
        run_model_c(y, y_in, x, d, a, fix, fixval, p);
    }
    diff = clock() - start;


    double sum = 0.0;
    for (i = 0; i < 14000; i++) {
        sum = sum + y[i];
    }
    printf("sum = %g\n", sum);
    double msec = 1e3 * diff / (REP * CLOCKS_PER_SEC);
    printf("Time taken  in milliseconds %g\n", msec);
}
