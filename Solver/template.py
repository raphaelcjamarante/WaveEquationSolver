import paths
from jinja2 import Environment, FileSystemLoader


def render_template(pde, code):
    env = Environment(loader=FileSystemLoader(paths.TEMPLATES_DIR))
    template = env.get_template("sympy.c.j2")

    with open(f"{paths.GENERATED_CODE_DIR}/sympy.c", "w") as file:
        file.write(template.render(pde=pde, code=code))

# c_program = c_template.format(code=p.doprint([rhs_of_odes, jac_of_odes]))
# print(c_program)

# with open('run.c', 'w') as f:
#     f.write(c_program)
