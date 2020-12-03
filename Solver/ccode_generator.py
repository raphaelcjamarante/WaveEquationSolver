from sympy import ccode, symbols, Range
from sympy.codegen.ast import *
from sympy.codegen.rewriting import create_expand_pow_optimization
import re

class Generator:

    def __init__(self, stencil, dimensions):
        self.stencil = stencil
        self.dimensions = dimensions

        self.time_access_pattern = re.compile('u\[(.*?)\]')
        #self.pow_pattern = re.compile('pow\(.*?\)')

        self.expand_opt = create_expand_pow_optimization(2)

    def replace_time_access(self, match):
        """ Substitute time dimension access on the vector for its modulo in order to optimize memory use:
            u[t+1][x][y] becomes u[(t+1)%3][x][y]. We use three points in time during each iteration: last, current, next
        """
        parameters = match.group(1)
        return f"u[({parameters})%3]"

    # def replace_exponents(self, match):
    #     """ Substitute pow exponents for their expanded symbolic version """
    #     exponent = match.group(0)
    #     return "(" + repr(self.expand_opt(eval(exponent))) + ")"

    def declarate_variables_same_type(self, symbols, var_type):
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
        # code = self.pow_pattern.sub(self.replace_exponents, code)
        return code

    def generate_solver(self):
        """ Generates solver of the wave equation in C code """
        declarations = self.declarate_variables_same_type(['t', 'x', 'y', 'z'], integer)

        t, x, y, z = symbols('t, x, y, z', integer=True)
        dt, h_x, h_y, h_z = symbols('dt, h_x, h_y, h_z', real=True)
        time_m, time_M, x_m, x_M, y_m, y_M, z_m, z_M = symbols('time_m, time_M, x_m, x_M, y_m, y_M, z_m, z_M', integer=True)

        body = self.get_stencil_code()
        if self.dimensions == 3:
            for_z = For(z, Range(z_m, z_M, 1), [body])
            for_y = For(y, Range(y_m, y_M, 1), [for_z])
        elif self.dimensions == 2:
            for_y = For(y, Range(y_m, y_M, 1), [body])

        for_x = For(x, Range(x_m, x_M, 1), [for_y])
        for_time = For(t, Range(time_m, time_M, 1), [for_x])

        code = CodeBlock(*declarations, for_time)

        return ccode(code)
