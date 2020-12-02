#include "stdlib.h"
#include "math.h"
#include <string.h>

struct dataobj
{
    void *restrict data;
    int * size;
} ;


int Kernel(const float dt, const float h_x, const float h_y, struct dataobj *restrict u_vec, const int time_M, const int time_m, const int x_M, const int x_m, const int y_M, const int y_m)
{
    float (*restrict u)[u_vec->size[1]][u_vec->size[2]] = (float (*)[u_vec->size[1]][u_vec->size[2]]) u_vec->data;

    for (int time = time_m, t0 = (time + 2)%(3), t1 = (time)%(3), t2 = (time + 1)%(3); time <= time_M; time += 1, t0 = (time + 2)%(3), t1 = (time)%(3), t2 = (time + 1)%(3))
    {
        for (int x = x_m; x <= x_M; x += 1)
        {
            for (int y = y_m; y <= y_M; y += 1)
            {
                float r6 = -2.0F*u[t1][x + 2][y + 2];
                float r5 = dt*dt;
                u[t2][x + 2][y + 2] = 1.0F*r5*((r6 + u[t1][x + 2][y + 1] + u[t1][x + 2][y + 3])/((h_y*h_y)) + (r6 + u[t1][x + 1][y + 2] + u[t1][x + 3][y + 2])/((h_x*h_x)) + (-1.0F*u[t0][x + 2][y + 2] + 2.0F*u[t1][x + 2][y + 2])/r5);
            }
        }
    }
    return 0;
}

int main() {
    int i = 101 - 1;
    int j = 20 + 1;
    int k = 20 + 1;

    size_t nbytes = i*j*k*sizeof(float);
    float* myarray = (float*) malloc(nbytes);
    memset(myarray,0,nbytes);

    int size[3] = {i,j,k};

    struct dataobj u_vec = { .data = myarray, .size = size };

    Kernel(0.02, 0.05, 0.05, &u_vec, 101, 1, 20, 0, 20, 0);

    return 0;
}