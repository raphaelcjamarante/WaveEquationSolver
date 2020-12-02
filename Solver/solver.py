import sys
import paths
import devito_parser
import template
from devito import Grid, TimeFunction, Eq, Operator, solve
from sympy import ccode
from ccode_generator import generate_solver

# This function will be usefull to compare my generated code with Devito's
def write_devito_operator_code(op, nt, dt, c):
    with open(f"{paths.GENERATED_CODE_DIR}/Devito_grau2_nt_{nt}_dt_{dt}_c_{c}.c", "w") as file:
        orig_stdout = sys.stdout
        sys.stdout = file
        print(op.ccode)
        sys.stdout = orig_stdout


# second order (our wave equation)

nt = 100  # Number of timesteps
dt = 0.2 * 2. / 20  # Timestep size (sigma=0.2)
c = 1  # Value for c

# ideally the grid should come from a proper model
grid = Grid(shape=(21, 21), extent=(1., 1.))

u = TimeFunction(name='u', grid=grid, space_order=2, time_order=2) # later increase space_order

pde = (1 / c*c) * u.dt2 - u.laplace
stencil = Eq(u.forward, solve(pde, u.forward))
#op = Operator(stencil)
#op(time=nt+1, dt=dt)

#write_devito_operator_code(op, nt, dt, c)

p = devito_parser.Parser(stencil)
#sympy_stencil = p.transform_expression()
#print(ccode(sympy_stencil.rhs, assign_to=sympy_stencil.lhs)) # print C version of stencil
code_body = p.get_C_code()
print(code_body)

code = generate_solver(code_body)


from examples.cfd import init_smooth, plot_field

# We can now set the initial condition and plot it
init_smooth(field=u.data[0], dx=grid.spacing[0], dy=grid.spacing[1])
init_smooth(field=u.data[1], dx=grid.spacing[0], dy=grid.spacing[1])

#plot_field(u.data[0])

import numpy as np
d = np.array(u.data)

# with open('test.txt', 'w') as outfile:
#     # Any line starting with "#" will be ignored by numpy.loadtxt
#     outfile.write('# Array shape: {0}\n'.format(d.shape))
    
#     for data_slice in d:
#         np.savetxt(outfile, data_slice)
#         outfile.write('# New slice\n')

data = ccode(d)
data = data.replace('[', '{')
data = data.replace(']', '}')

pde_info = {
    "dt": dt,
    "step_x": grid.extent[0] / (grid.shape[0] - 1),
    "step_y": grid.extent[1] / (grid.shape[1] - 1),
    "u_data": data,
    "u_shape": u.shape,
    "max_time": nt+1, # or nt?
    "min_time": 1, # or 0?
    "max_x": (grid.shape[0] - 1),
    "min_x": 0,
    "max_y": (grid.shape[1] - 1),
    "min_y": 0
}
template.render_template(pde_info, code=code)
