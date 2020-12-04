import paths
import numpy as np
from sympy import ccode
from jinja2 import Environment, FileSystemLoader

class Renderer:
    def __init__(self, u, dt, time, solver):
        self.u = u
        self.dt = dt
        self.time = time
        self.solver = solver

    def get_data(self):
        """ Gets problem data and substitutes symbols so the data array with data can be initialized """
        data = np.array(self.u.data)
        data = ccode(data)
        data = data.replace('[', '{')
        data = data.replace(']', '}')
        return data

    def get_solver_parameters(self):
        """ Gets the parameters necessary to run the solver """
        return {
                    "dt": self.dt,
                    "step_x": self.u.grid.extent[0] / (self.u.grid.shape[0] - 1),
                    "step_y": self.u.grid.extent[1] / (self.u.grid.shape[1] - 1),
                    #"step_z": self.u.grid.extent[2] / (self.u.grid.shape[2] - 1) if len(self.u.grid.dimensions) == 3 else 1,
                    "u_data": self.get_data(),
                    "u_shape": self.u.shape,
                    "max_time": self.time + 1,
                    "min_time": 1,
                    "max_x": (self.u.grid.shape[0] - 1),
                    "min_x": 2,
                    "max_y": (self.u.grid.shape[1] - 1),
                    "min_y": 2,
                    #"max_z": (self.u.grid.shape[2] - 1) if len(self.u.grid.dimensions) == 3 else 0,
                    #"min_z": 2
                }

    def render_template(self):
        """ Renders the template """
        env = Environment(loader=FileSystemLoader(paths.TEMPLATES_DIR))
        template = env.get_template("solver.c.j2")

        with open(f"{paths.GENERATED_CODE_DIR}/solver.c", "w") as file:
            file.write(template.render(params=self.get_solver_parameters(), solver=self.solver))
