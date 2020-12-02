from sympy import *
from sympy.abc import h, u, t, x, y
from sympy.codegen.ast import *
from sympy.codegen.cnodes import sizeof, struct, CommaOperator
from sympy.codegen.cutils import render_as_source_file
from sympy.codegen.rewriting import create_expand_pow_optimization
import re
from sympy.core.sympify import sympify

def write_sympy_code(expression):
    with open(f"{paths.GENERATED_CODE_DIR}/Sympy.c", "w") as file:
        orig_stdout = sys.stdout
        sys.stdout = file
        print(ccode(expression))
        sys.stdout = orig_stdout

class Generator:

    def __init__(self, stencil):
        self.stencil = stencil

        self.time_access_pattern = re.compile('u\[(.*?)\]')
        #self.pow_pattern = re.compile('pow\(.*?\)')

        self.expand_opt = create_expand_pow_optimization(2)

    # def generate_inner_loop(self):
    #     """ Creates the innermost loop of the pde resolution """
    #     pass

    # def generate_middle_loop(self):
    #     pass

    # def generate_outer_loop(self):
    #     pass

    def replace_time_access(self, match):
        """ Substitute time dimension access on the vector for its modulo in order to optimize memory use:
            u[t+1][x][y] becomes u[(t+1)%3][x][y]. We use three points in time each iteration: last, current, next
        """
        parameters = match.group(1)
        return f"u[({parameters})%3]"

    # def replace_exponents(self, match):
    #     """ Substitute pow exponents for their expanded symbolic version """
    #     exponent = match.group(0)
    #     return "(" + repr(self.expand_opt(eval(exponent))) + ")"

    def declarate_variables_same_type(symbols, var_type):
        """ Declaration of any number of variables of a specific type """
        variables = []
        for s in symbols:
            new_symbol = Declaration(s)
            new_symbol.variable.type = var_type
            variables.append(new_symbol)
        return variables

    def get_stencil_code(self):
        """ Get C code representing the stencil indexing with memory optimization """
        code = ccode(self.stencil.rhs, assign_to=self.stencil.lhs)
        code = self.time_access_pattern.sub(self.replace_time_access, code)
        #code = self.pow_pattern.sub(self.replace_exponents, code)

        return code


    def generate_solver():
        declarations = declarate_variables_same_type(['t', 'x', 'y'], integer)

        dt, h_x, h_y = symbols('dt, h_x, h_y', real=True)
        time_m, time_M, x_m, x_M, y_m, y_M = symbols('time_m, time_M, x_m, x_M, y_m, y_M', integer=True)

        body = get_stencil_code()
        for_y = For(y, Range(y_m, y_M, 1), [body])
        for_x = For(x, Range(x_m, x_M, 1), [for_y])
        for_time = For(t, Range(time_m, time_M, 1), [for_x])

        # kernel_prototype = FunctionPrototype(integer, 'Kernel', [dt, h_x, h_y, time_M, time_m, x_M, x_m, y_M, y_m])
        # kernel_return = Return(0)
        # kernel_function = FunctionDefinition.from_FunctionPrototype(kernel_prototype, [for_time, kernel_return])
        code = CodeBlock(*declarations, for_time)

        return ccode(code)





# # # ccode(expr, assign_to='u', type_aliases={real: float32})
# # # ccode(sizeof(float32))

# # # int Kernel(const float dt, const float h_x, const float h_y, struct dataobj *restrict u_vec, const int time_M, const int time_m, const int x_M, const int x_m, const int y_M, const int y_m)

# # # Creating the function that solves the pde
# kernel_prototype = FunctionPrototype(integer, 'Kernel', [dt, h_x, h_y, time_M, time_m, x_M, x_m, y_M, y_m])
# kernel_return = Return(0)
# kernel_function = FunctionDefinition.from_FunctionPrototype(kernel_prototype, [for_time, kernel_return])


# settings={"headers" : ["stdlib.h", "math.h", "<string.h>"]}
# render_as_source_file(kernel_function, settings=settings)

# # Creating the main, which calls the pde

# initializations = CodeBlock() # so far this only supports assignments


# kernel_call = FunctionCall('Kernel', 'dt step_x step_y max_time min_time max_x min_x max_y min_y'.split())

# use Pointer ?


# from sympy.utilities.codegen import codegen
# [(c_name, c_code), (h_name, c_header)] = codegen(("f", x+y*z), "C89", "test", header=False, empty=False)


