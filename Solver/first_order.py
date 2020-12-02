import sys
import numpy as np
import paths
import template
import devito
import sympy
from devito import Grid, TimeFunction, Eq, Operator, solve


def write_devito_operator_code(op, nt, dt, c):
    with open(f"{paths.GENERATED_CODE_DIR}/Devito_grau2_nt_{nt}_dt_{dt}_c_{c}.c", "w") as file:
        orig_stdout = sys.stdout
        sys.stdout = file
        print(op.ccode)
        sys.stdout = orig_stdout


nt = 100  # Number of timesteps
dt = 0.2 * 2. / 80  # Timestep size (sigma=0.2)
c = 1  # Value for c

# Then we create a grid and our function
grid = Grid(shape=(81, 81), extent=(2., 2.))
u = TimeFunction(name='u', grid=grid)

equation = u.dt + c * u.dxl + c * u.dyl
stencil = Eq(u.forward, devito.solve(equation, u.forward))
op = Operator(stencil)
op(time=nt+1, dt=dt)

write_devito_operator_code(op, nt, dt, c)

u_info = {
    "data": u.data
}

pde = {
    "dt": dt,
    "step_x": grid.extent[0] / (grid.shape[0] - 1),
    "step_y": grid.extent[1] / (grid.shape[1] - 1),
    "u": u_info,
    "max_time": nt+1, # or nt?
    "min_time": 1, # or 0?
    "max_x": (grid.shape[0] - 1),
    "min_x": 0,
    "max_y": (grid.shape[1] - 1),
    "min_y": 0
}
template.render_template(pde)