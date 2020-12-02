#define _POSIX_C_SOURCE 200809L
#include "stdlib.h"
#include "math.h"
#include "sys/time.h"
#include "xmmintrin.h"
#include "pmmintrin.h"

struct dataobj
{
  void *restrict data;
  int * size;
  int * npsize;
  int * dsize;
  int * hsize;
  int * hofs;
  int * oofs;
} ;


int Kernel(const float dt, const float o_x, const float o_y, struct dataobj *restrict rec_vec, struct dataobj *restrict rec_coords_vec, struct dataobj *restrict src_vec, struct dataobj *restrict src_coords_vec, struct dataobj *restrict u_vec, struct dataobj *restrict vp_vec, const int x_M, const int x_m, const int y_M, const int y_m, const int p_rec_M, const int p_rec_m, const int p_src_M, const int p_src_m, const int time_M, const int time_m)
{
  float (*restrict rec)[rec_vec->size[1]] __attribute__ ((aligned (64))) = (float (*)[rec_vec->size[1]]) rec_vec->data;
  float (*restrict rec_coords)[rec_coords_vec->size[1]] __attribute__ ((aligned (64))) = (float (*)[rec_coords_vec->size[1]]) rec_coords_vec->data;

  float (*restrict src)[src_vec->size[1]] __attribute__ ((aligned (64))) = (float (*)[src_vec->size[1]]) src_vec->data;
  float (*restrict src_coords)[src_coords_vec->size[1]] __attribute__ ((aligned (64))) = (float (*)[src_coords_vec->size[1]]) src_coords_vec->data;
  
  float (*restrict u)[u_vec->size[1]][u_vec->size[2]] __attribute__ ((aligned (64))) = (float (*)[u_vec->size[1]][u_vec->size[2]]) u_vec->data;
  float (*restrict vp)[vp_vec->size[1]] __attribute__ ((aligned (64))) = (float (*)[vp_vec->size[1]]) vp_vec->data;


  for (int time = time_m, t0 = (time + 2)%(3), t1 = (time)%(3), t2 = (time + 1)%(3); time <= time_M; time += 1, t0 = (time + 2)%(3), t1 = (time)%(3), t2 = (time + 1)%(3))
  {
    for (int x = x_m; x <= x_M; x += 1)
    {
      for (int y = y_m; y <= y_M; y += 1)
      {
        float r10 = dt*dt;
        float r9 = vp[x + 2][y + 2]*vp[x + 2][y + 2];
        u[t2][x + 2][y + 2] = r10*r9*(1.0e-2F*(u[t1][x + 1][y + 2] + u[t1][x + 2][y + 1] + u[t1][x + 2][y + 3] + u[t1][x + 3][y + 2]) - 3.99999991e-2F*u[t1][x + 2][y + 2] + (-(u[t0][x + 2][y + 2] - 2.0F*u[t1][x + 2][y + 2])/r10)/r9);
      }
    }

    for (int p_src = p_src_m; p_src <= p_src_M; p_src += 1)
    {
      float posx = -o_x + src_coords[p_src][0];
      float posy = -o_y + src_coords[p_src][1];
      int ii_src_0 = (int)(floor(1.0e-1*posx));
      int ii_src_1 = (int)(floor(1.0e-1*posy));
      int ii_src_2 = (int)(floor(1.0e-1*posy)) + 1;
      int ii_src_3 = (int)(floor(1.0e-1*posx)) + 1;
      float px = (float)(posx - 1.0e+1F*(int)(floor(1.0e-1F*posx)));
      float py = (float)(posy - 1.0e+1F*(int)(floor(1.0e-1F*posy)));
      if (ii_src_0 >= x_m - 1 && ii_src_1 >= y_m - 1 && ii_src_0 <= x_M + 1 && ii_src_1 <= y_M + 1)
      {
        float r0 = 5.99760042078401F*(vp[ii_src_0 + 2][ii_src_1 + 2]*vp[ii_src_0 + 2][ii_src_1 + 2])*(1.0e-2F*px*py - 1.0e-1F*px - 1.0e-1F*py + 1)*src[time][p_src];
        u[t2][ii_src_0 + 2][ii_src_1 + 2] += r0;
      }
      if (ii_src_0 >= x_m - 1 && ii_src_2 >= y_m - 1 && ii_src_0 <= x_M + 1 && ii_src_2 <= y_M + 1)
      {
        float r1 = 5.99760042078401F*(vp[ii_src_0 + 2][ii_src_2 + 2]*vp[ii_src_0 + 2][ii_src_2 + 2])*(-1.0e-2F*px*py + 1.0e-1F*py)*src[time][p_src];
        u[t2][ii_src_0 + 2][ii_src_2 + 2] += r1;
      }
      if (ii_src_1 >= y_m - 1 && ii_src_3 >= x_m - 1 && ii_src_1 <= y_M + 1 && ii_src_3 <= x_M + 1)
      {
        float r2 = 5.99760042078401F*(vp[ii_src_3 + 2][ii_src_1 + 2]*vp[ii_src_3 + 2][ii_src_1 + 2])*(-1.0e-2F*px*py + 1.0e-1F*px)*src[time][p_src];
        u[t2][ii_src_3 + 2][ii_src_1 + 2] += r2;
      }
      if (ii_src_2 >= y_m - 1 && ii_src_3 >= x_m - 1 && ii_src_2 <= y_M + 1 && ii_src_3 <= x_M + 1)
      {
        float r3 = 5.99760084529726e-2F*px*py*(vp[ii_src_3 + 2][ii_src_2 + 2]*vp[ii_src_3 + 2][ii_src_2 + 2])*src[time][p_src];
        u[t2][ii_src_3 + 2][ii_src_2 + 2] += r3;
      }
    }

    for (int p_rec = p_rec_m; p_rec <= p_rec_M; p_rec += 1)
    {
      float posx = -o_x + rec_coords[p_rec][0];
      float posy = -o_y + rec_coords[p_rec][1];
      int ii_rec_0 = (int)(floor(1.0e-1*posx));
      int ii_rec_1 = (int)(floor(1.0e-1*posy));
      int ii_rec_2 = (int)(floor(1.0e-1*posy)) + 1;
      int ii_rec_3 = (int)(floor(1.0e-1*posx)) + 1;
      float px = (float)(posx - 1.0e+1F*(int)(floor(1.0e-1F*posx)));
      float py = (float)(posy - 1.0e+1F*(int)(floor(1.0e-1F*posy)));
      float sum = 0.0F;
      if (ii_rec_0 >= x_m - 1 && ii_rec_1 >= y_m - 1 && ii_rec_0 <= x_M + 1 && ii_rec_1 <= y_M + 1)
      {
        sum += (1.0e-2F*px*py - 1.0e-1F*px - 1.0e-1F*py + 1)*u[t2][ii_rec_0 + 2][ii_rec_1 + 2];
      }
      if (ii_rec_0 >= x_m - 1 && ii_rec_2 >= y_m - 1 && ii_rec_0 <= x_M + 1 && ii_rec_2 <= y_M + 1)
      {
        sum += (-1.0e-2F*px*py + 1.0e-1F*py)*u[t2][ii_rec_0 + 2][ii_rec_2 + 2];
      }
      if (ii_rec_1 >= y_m - 1 && ii_rec_3 >= x_m - 1 && ii_rec_1 <= y_M + 1 && ii_rec_3 <= x_M + 1)
      {
        sum += (-1.0e-2F*px*py + 1.0e-1F*px)*u[t2][ii_rec_3 + 2][ii_rec_1 + 2];
      }
      if (ii_rec_2 >= y_m - 1 && ii_rec_3 >= x_m - 1 && ii_rec_2 <= y_M + 1 && ii_rec_3 <= x_M + 1)
      {
        sum += 1.0e-2F*px*py*u[t2][ii_rec_3 + 2][ii_rec_2 + 2];
      }
      rec[time][p_rec] = sum;
    }

  }
  return 0;
}
