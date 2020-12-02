from sympy import *
from sympy.abc import h, u, t, x, y
from sympy.codegen.ast import *
from sympy.codegen.cnodes import sizeof, struct, CommaOperator
from sympy.codegen.cutils import render_as_source_file
from sympy.codegen.rewriting import create_expand_pow_optimization
import re
from sympy.core.sympify import sympify
from devito_parser import Parser

def write_sympy_code(expression):
    with open(f"{paths.GENERATED_CODE_DIR}/Sympy.c", "w") as file:
        orig_stdout = sys.stdout
        sys.stdout = file
        print(ccode(expression))
        sys.stdout = orig_stdout

class Generator:

    def __init__(self):
        pass

    # def generate_inner_loop(self):
    #     """ Creates the innermost loop of the pde resolution """
    #     pass

    # def generate_middle_loop(self):
    #     pass

    # def generate_outer_loop(self):
    #     pass

def declarate_variables_same_type(symbols, var_type):
    variables = []
    for s in symbols:
        new_symbol = Declaration(s)
        new_symbol.variable.type = var_type
        variables.append(new_symbol)
    return variables

def generate_solver(body):
    declarations = declarate_variables_same_type(['t', 'x', 'y'], integer)

    dt, h_x, h_y = symbols('dt, h_x, h_y', real=True)
    time_m, time_M, x_m, x_M, y_m, y_M = symbols('time_m, time_M, x_m, x_M, y_m, y_M', integer=True)

    for_y = For(y, Range(y_m + 2, y_M, 1), [body])
    for_x = For(x, Range(x_m + 2, x_M, 1), [for_y])
    for_time = For(t, Range(time_m, time_M, 1), [for_x])

    # kernel_prototype = FunctionPrototype(integer, 'Kernel', [dt, h_x, h_y, time_M, time_m, x_M, x_m, y_M, y_m])
    # kernel_return = Return(0)
    # kernel_function = FunctionDefinition.from_FunctionPrototype(kernel_prototype, [for_time, kernel_return])
    code = CodeBlock(*declarations, for_time)

    return ccode(code)


# Creating all necessary variables
# u = symbols('u') #function
# dt, h_x, h_y = symbols('dt, h_x, h_y', real=True)
# time, time_m, time_M, x, x_m, x_M, y, y_m, y_M = symbols('time, time_m, time_M, x, x_m, x_M, y, y_m, y_M', integer=True)
# # t0, t1, t2 = symbols('t:3', integer=True)


# # Creating expression that solves the pde
# #expand_opt = create_expand_pow_optimization(2)


# # Creating the loops that iterate and solve the pde
# for_y = For(y, Range(y_m, y_M, 1), [Assignment(sympy_stencil.lhs, sympy_stencil.rhs)])
# for_x = For(x, Range(x_m, x_M, 1), [for_y])
# for_time = For(time, Range(time_m, time_M, 1), [for_x])


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



#"Eq(Element(Symbol('u'), indices=(Add(Symbol('dt'), Symbol('t')), Symbol('x'), Symbol('y'))), Float(1.0)*Symbol('dt')**2*(-Float(2.0)*Element(Symbol('u'), indices=(Symbol('t'), Symbol('x'), Symbol('y')))/Symbol('h_y')**2 + Element(Symbol('u'), indices=(Symbol('t'), Symbol('x'), Add(Mul(Integer(-1), Symbol('h_y')), Symbol('y'))))/Symbol('h_y')**2 + Element(Symbol('u'), indices=(Symbol('t'), Symbol('x'), Add(Symbol('h_y'), Symbol('y'))))/Symbol('h_y')**2 - Float(2.0)*Element(Symbol('u'), indices=(Symbol('t'), Symbol('x'), Symbol('y')))/Symbol('h_x')**2 + Element(Symbol('u'), indices=(Symbol('t'), Add(Mul(Integer(-1), Symbol('h_x')), Symbol('x')), Symbol('y')))/Symbol('h_x')**2 + Element(Symbol('u'), indices=(Symbol('t'), Add(Symbol('h_x'), Symbol('x')), Symbol('y')))/Symbol('h_x')**2 + Float(2.0)*Element(Symbol('u'), indices=(Symbol('t'), Symbol('x'), Symbol('y')))/Symbol('dt')**2 - Float(1.0)*Element(Symbol('u'), indices=(Add(Mul(Integer(-1), Symbol('dt')), Symbol('t')), Symbol('x'), Symbol('y')))/Symbol('dt')**2))"
