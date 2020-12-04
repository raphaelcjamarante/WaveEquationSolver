#include "stdlib.h"
#include "math.h"

int Solver(double dt, double h_x, double h_y, double u[3][21][21], int time_M, int time_m, int x_M, int x_m, int y_M, int y_m){
   int t;
   int x;
   int y;
   for (t = time_m; t < time_M; t += 1) {
      for (x = x_m; x < x_M; x += 1) {
         for (y = y_m; y < y_M; y += 1) {
            u[(t + 1)%3][x][y] = 1.0*pow(dt, 2)*(-2.0*u[(t)%3][x][y]/pow(h_y, 2) + u[(t)%3][x][y - 1]/pow(h_y, 2) + u[(t)%3][x][y + 1]/pow(h_y, 2) - 2.0*u[(t)%3][x][y]/pow(h_x, 2) + u[(t)%3][x - 1][y]/pow(h_x, 2) + u[(t)%3][x + 1][y]/pow(h_x, 2) + 2.0*u[(t)%3][x][y]/pow(dt, 2) - 1.0*u[(t - 1)%3][x][y]/pow(dt, 2));
         };
      };
   };
}

int main() {
    double myarray[3][21][21] = {{{1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000}, {1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000}, {1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00001, 1.00001, 1.00001, 1.00001, 1.00002, 1.00002, 1.00002, 1.00002, 1.00002, 1.00002, 1.00002, 1.00001, 1.00001}, {1.00000, 1.00000, 1.00000, 1.00000, 1.00003, 1.00011, 1.00029, 1.00056, 1.00090, 1.00128, 1.00166, 1.00202, 1.00232, 1.00255, 1.00269, 1.00274, 1.00269, 1.00255, 1.00232, 1.00202, 1.00166}, {1.00000, 1.00000, 1.00000, 1.00003, 1.00030, 1.00130, 1.00337, 1.00652, 1.01049, 1.01491, 1.01938, 1.02352, 1.02705, 1.02972, 1.03139, 1.03195, 1.03139, 1.02972, 1.02705, 1.02352, 1.01938}, {1.00000, 1.00000, 1.00000, 1.00011, 1.00130, 1.00557, 1.01441, 1.02788, 1.04490, 1.06383, 1.08294, 1.10067, 1.11575, 1.12719, 1.13432, 1.13674, 1.13432, 1.12719, 1.11575, 1.10067, 1.08294}, {1.00000, 1.00000, 1.00000, 1.00029, 1.00337, 1.01441, 1.03727, 1.07210, 1.11610, 1.16504, 1.21445, 1.26031, 1.29929, 1.32888, 1.34732, 1.35357, 1.34732, 1.32888, 1.29929, 1.26031, 1.21445}, {1.00000, 1.00000, 1.00000, 1.00056, 1.00652, 1.02788, 1.07210, 1.13949, 1.22462, 1.31930, 1.41490, 1.50362, 1.57904, 1.63628, 1.67194, 1.68405, 1.67194, 1.63628, 1.57904, 1.50362, 1.41490}, {1.00000, 1.00000, 1.00001, 1.00090, 1.01049, 1.04490, 1.11610, 1.22462, 1.36170, 1.51417, 1.66811, 1.81098, 1.93243, 2.02460, 2.08204, 2.10153, 2.08204, 2.02460, 1.93243, 1.81098, 1.66811}, {1.00000, 1.00000, 1.00001, 1.00128, 1.01491, 1.06383, 1.16504, 1.31930, 1.51417, 1.73091, 1.94974, 2.15283, 2.32547, 2.45650, 2.53815, 2.56586, 2.53815, 2.45650, 2.32547, 2.15283, 1.94974}, {1.00000, 1.00000, 1.00001, 1.00166, 1.01938, 1.08294, 1.21445, 1.41490, 1.66811, 1.94974, 2.23410, 2.49798, 2.72232, 2.89258, 2.99867, 3.03468, 2.99867, 2.89258, 2.72232, 2.49798, 2.23410}, {1.00000, 1.00000, 1.00001, 1.00202, 1.02352, 1.10067, 1.26031, 1.50362, 1.81098, 2.15283, 2.49798, 2.81830, 3.09061, 3.29727, 3.42605, 3.46976, 3.42605, 3.29727, 3.09061, 2.81830, 2.49798}, {1.00000, 1.00000, 1.00002, 1.00232, 1.02705, 1.11575, 1.29929, 1.57904, 1.93243, 2.32547, 2.72232, 3.09061, 3.40369, 3.64131, 3.78937, 3.83963, 3.78937, 3.64131, 3.40369, 3.09061, 2.72232}, {1.00000, 1.00000, 1.00002, 1.00255, 1.02972, 1.12719, 1.32888, 1.63628, 2.02460, 2.45650, 2.89258, 3.29727, 3.64131, 3.90242, 4.06511, 4.12034, 4.06511, 3.90242, 3.64131, 3.29727, 2.89258}, {1.00000, 1.00000, 1.00002, 1.00269, 1.03139, 1.13432, 1.34732, 1.67194, 2.08204, 2.53815, 2.99867, 3.42605, 3.78937, 4.06511, 4.23693, 4.29525, 4.23693, 4.06511, 3.78937, 3.42605, 2.99867}, {1.00000, 1.00000, 1.00002, 1.00274, 1.03195, 1.13674, 1.35357, 1.68405, 2.10153, 2.56586, 3.03468, 3.46976, 3.83963, 4.12034, 4.29525, 4.35463, 4.29525, 4.12034, 3.83963, 3.46976, 3.03468}, {1.00000, 1.00000, 1.00002, 1.00269, 1.03139, 1.13432, 1.34732, 1.67194, 2.08204, 2.53815, 2.99867, 3.42605, 3.78937, 4.06511, 4.23693, 4.29525, 4.23693, 4.06511, 3.78937, 3.42605, 2.99867}, {1.00000, 1.00000, 1.00002, 1.00255, 1.02972, 1.12719, 1.32888, 1.63628, 2.02460, 2.45650, 2.89258, 3.29727, 3.64131, 3.90242, 4.06511, 4.12034, 4.06511, 3.90242, 3.64131, 3.29727, 2.89258}, {1.00000, 1.00000, 1.00002, 1.00232, 1.02705, 1.11575, 1.29929, 1.57904, 1.93243, 2.32547, 2.72232, 3.09061, 3.40369, 3.64131, 3.78937, 3.83963, 3.78937, 3.64131, 3.40369, 3.09061, 2.72232}, {1.00000, 1.00000, 1.00001, 1.00202, 1.02352, 1.10067, 1.26031, 1.50362, 1.81098, 2.15283, 2.49798, 2.81830, 3.09061, 3.29727, 3.42605, 3.46976, 3.42605, 3.29727, 3.09061, 2.81830, 2.49798}, {1.00000, 1.00000, 1.00001, 1.00166, 1.01938, 1.08294, 1.21445, 1.41490, 1.66811, 1.94974, 2.23410, 2.49798, 2.72232, 2.89258, 2.99867, 3.03468, 2.99867, 2.89258, 2.72232, 2.49798, 2.23410}}, {{1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000}, {1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000}, {1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00000, 1.00001, 1.00001, 1.00001, 1.00001, 1.00002, 1.00002, 1.00002, 1.00002, 1.00002, 1.00002, 1.00002, 1.00001, 1.00001}, {1.00000, 1.00000, 1.00000, 1.00000, 1.00003, 1.00011, 1.00029, 1.00056, 1.00090, 1.00128, 1.00166, 1.00202, 1.00232, 1.00255, 1.00269, 1.00274, 1.00269, 1.00255, 1.00232, 1.00202, 1.00166}, {1.00000, 1.00000, 1.00000, 1.00003, 1.00030, 1.00130, 1.00337, 1.00652, 1.01049, 1.01491, 1.01938, 1.02352, 1.02705, 1.02972, 1.03139, 1.03195, 1.03139, 1.02972, 1.02705, 1.02352, 1.01938}, {1.00000, 1.00000, 1.00000, 1.00011, 1.00130, 1.00557, 1.01441, 1.02788, 1.04490, 1.06383, 1.08294, 1.10067, 1.11575, 1.12719, 1.13432, 1.13674, 1.13432, 1.12719, 1.11575, 1.10067, 1.08294}, {1.00000, 1.00000, 1.00000, 1.00029, 1.00337, 1.01441, 1.03727, 1.07210, 1.11610, 1.16504, 1.21445, 1.26031, 1.29929, 1.32888, 1.34732, 1.35357, 1.34732, 1.32888, 1.29929, 1.26031, 1.21445}, {1.00000, 1.00000, 1.00000, 1.00056, 1.00652, 1.02788, 1.07210, 1.13949, 1.22462, 1.31930, 1.41490, 1.50362, 1.57904, 1.63628, 1.67194, 1.68405, 1.67194, 1.63628, 1.57904, 1.50362, 1.41490}, {1.00000, 1.00000, 1.00001, 1.00090, 1.01049, 1.04490, 1.11610, 1.22462, 1.36170, 1.51417, 1.66811, 1.81098, 1.93243, 2.02460, 2.08204, 2.10153, 2.08204, 2.02460, 1.93243, 1.81098, 1.66811}, {1.00000, 1.00000, 1.00001, 1.00128, 1.01491, 1.06383, 1.16504, 1.31930, 1.51417, 1.73091, 1.94974, 2.15283, 2.32547, 2.45650, 2.53815, 2.56586, 2.53815, 2.45650, 2.32547, 2.15283, 1.94974}, {1.00000, 1.00000, 1.00001, 1.00166, 1.01938, 1.08294, 1.21445, 1.41490, 1.66811, 1.94974, 2.23410, 2.49798, 2.72232, 2.89258, 2.99867, 3.03468, 2.99867, 2.89258, 2.72232, 2.49798, 2.23410}, {1.00000, 1.00000, 1.00001, 1.00202, 1.02352, 1.10067, 1.26031, 1.50362, 1.81098, 2.15283, 2.49798, 2.81830, 3.09061, 3.29727, 3.42605, 3.46976, 3.42605, 3.29727, 3.09061, 2.81830, 2.49798}, {1.00000, 1.00000, 1.00002, 1.00232, 1.02705, 1.11575, 1.29929, 1.57904, 1.93243, 2.32547, 2.72232, 3.09061, 3.40369, 3.64131, 3.78937, 3.83963, 3.78937, 3.64131, 3.40369, 3.09061, 2.72232}, {1.00000, 1.00000, 1.00002, 1.00255, 1.02972, 1.12719, 1.32888, 1.63628, 2.02460, 2.45650, 2.89258, 3.29727, 3.64131, 3.90242, 4.06511, 4.12034, 4.06511, 3.90242, 3.64131, 3.29727, 2.89258}, {1.00000, 1.00000, 1.00002, 1.00269, 1.03139, 1.13432, 1.34732, 1.67194, 2.08204, 2.53815, 2.99867, 3.42605, 3.78937, 4.06511, 4.23693, 4.29525, 4.23693, 4.06511, 3.78937, 3.42605, 2.99867}, {1.00000, 1.00000, 1.00002, 1.00274, 1.03195, 1.13674, 1.35357, 1.68405, 2.10153, 2.56586, 3.03468, 3.46976, 3.83963, 4.12034, 4.29525, 4.35463, 4.29525, 4.12034, 3.83963, 3.46976, 3.03468}, {1.00000, 1.00000, 1.00002, 1.00269, 1.03139, 1.13432, 1.34732, 1.67194, 2.08204, 2.53815, 2.99867, 3.42605, 3.78937, 4.06511, 4.23693, 4.29525, 4.23693, 4.06511, 3.78937, 3.42605, 2.99867}, {1.00000, 1.00000, 1.00002, 1.00255, 1.02972, 1.12719, 1.32888, 1.63628, 2.02460, 2.45650, 2.89258, 3.29727, 3.64131, 3.90242, 4.06511, 4.12034, 4.06511, 3.90242, 3.64131, 3.29727, 2.89258}, {1.00000, 1.00000, 1.00002, 1.00232, 1.02705, 1.11575, 1.29929, 1.57904, 1.93243, 2.32547, 2.72232, 3.09061, 3.40369, 3.64131, 3.78937, 3.83963, 3.78937, 3.64131, 3.40369, 3.09061, 2.72232}, {1.00000, 1.00000, 1.00001, 1.00202, 1.02352, 1.10067, 1.26031, 1.50362, 1.81098, 2.15283, 2.49798, 2.81830, 3.09061, 3.29727, 3.42605, 3.46976, 3.42605, 3.29727, 3.09061, 2.81830, 2.49798}, {1.00000, 1.00000, 1.00001, 1.00166, 1.01938, 1.08294, 1.21445, 1.41490, 1.66811, 1.94974, 2.23410, 2.49798, 2.72232, 2.89258, 2.99867, 3.03468, 2.99867, 2.89258, 2.72232, 2.49798, 2.23410}}, {{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}, {0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}}};

    Solver(0.02, 0.05, 0.05, myarray, 101, 1, 20, 2, 20, 2);

    return 0;
}