import sys
import paths
import devito_parser
import ccode_generator
import template_renderer
from devito import Grid, TimeFunction, Eq, Operator, solve

# This function will be usefull to compare my generated code with Devito's
def write_devito_operator_code(op, nt, dt, c):
    with open(f"{paths.GENERATED_CODE_DIR}/Devito_grau2_nt_{nt}_dt_{dt}_c_{c}.c", "w") as file:
        orig_stdout = sys.stdout
        sys.stdout = file
        print(op.ccode)
        sys.stdout = orig_stdout


# Define problem: second order wave equation
nt = 100  # Number of timesteps
dt = 0.2 * 2. / 20  # Timestep size (sigma=0.2)
c = 1  # Value for c

grid = Grid(shape=(21, 21), extent=(1., 1.))
u = TimeFunction(name='u', grid=grid, space_order=2, time_order=2)

pde = (1 / c*c) * u.dt2 - u.laplace
stencil = Eq(u.forward, solve(pde, u.forward))

# Initialize problem data (initial condition)
from examples.cfd import init_smooth, plot_field
init_smooth(field=u.data[0], dx=grid.spacing[0], dy=grid.spacing[1])
init_smooth(field=u.data[1], dx=grid.spacing[0], dy=grid.spacing[1])


#op = Operator(stencil)
#op(time=nt+1, dt=dt)

#write_devito_operator_code(op, nt, dt, c)

# Tranlate DSL
parser = devito_parser.Parser(stencil)
sympy_stencil = parser.transform_expression()

# Generate solver code
generator = ccode_generator.Generator(sympy_stencil)
code = generator.generate_solver()

# Render template
renderer = template_renderer.Renderer(u, dt, nt, code)
renderer.render_template()
