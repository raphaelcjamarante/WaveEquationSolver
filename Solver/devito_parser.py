from sympy import ccode
from sympy.codegen.ast import *
from sympy.core.relational import Eq
from sympy.core.symbol import Symbol
from sympy.abc import u # TODO: accept different function names
from sympy.codegen.rewriting import create_expand_pow_optimization
import re

class Parser:
    """ This class is dedicated to transform a Devito symbolic expression into a SymPy symbolic expression
    """
    def __init__(self, expression):
        self.expression = str(expression)
        self.free_symbols = [str(symbol) for symbol in expression.free_symbols]

        self.function_pattern = re.compile('u\((.*?)\)')  # TODO: accept different function names
        self.float_pattern = re.compile("\d+\.\d+")
        self.free_symbol_pattern = re.compile("\w+") # actually this can find any word, but we compare it to free symbols
        self.time_access_pattern = re.compile('u\[(.*?)\]')
        #self.pow_pattern = re.compile('pow\(.*?\)')

        self.expand_opt = create_expand_pow_optimization(2)

    def parameters_indexing(self, parameters):
        """ The n-dim array that represents the problem is divided in the number of steps of each dimension.
            To access each element of the array, the indexes should be integers, so we substitute the step markers for 1
        """
        step_markers = ["dt", "h_x", "h_y"]
        for step in step_markers:
            parameters = parameters.replace(step, '1')
        return parameters

    def replace_functions(self, match):
        """ Substitute functions in the format u(t,x,y) for the symbolic representation
            of their array counterpart u[t][x][y], that is, Element('u', 'txy')
        """
        parameters = match.group(1)  # group(1) gets only the params, not the whole function
        parameters = self.parameters_indexing(parameters)
        elem = Element('u', parameters.split(', '))
        return str(elem)

    def replace_free_symbols(self, match):
        """ Substitute words that should be symbols for their symbolic representation Symbol('word') """
        word = match.group(0)
        if word in self.free_symbols:
            return f"Symbol('{word}')"
        return word

    def replace_floats(self, match):
        """ Substitute float numbers (must have at least one decimal) for their symbolic representation Float(X.X) """
        number = match.group(0)
        return f"Float({number})"

    def replace_time_access(self, match):
        """ Substitute time dimension access on the vector for its modulo in order to save memory: 
            u[t+1][x][y] becomes u[(t+1)%3][x][y]. We use three points in time: last, current, next
        """
        parameters = match.group(1)
        return f"u[({parameters})%3]"

    # def replace_exponents(self, match):
    #     """ Substitute pow exponents for their expanded symbolic version """
    #     exponent = match.group(0)
    #     return "(" + repr(self.expand_opt(eval(exponent))) + ")"

    def transform_expression(self):
        """ Transform a Devito expression in a SymPy expression by calling the transformations in the correct order """
        transform = self.function_pattern.sub(self.replace_functions, self.expression)
        transform = self.free_symbol_pattern.sub(self.replace_free_symbols, transform)
        transform = self.float_pattern.sub(self.replace_floats, transform)
        return eval(transform)

    def get_C_code(self):
        """ Get C code representing the stencil indexing with memory optimization """
        sympy_stencil = self.transform_expression()
        code = ccode(sympy_stencil.rhs, assign_to=sympy_stencil.lhs)
        code = self.time_access_pattern.sub(self.replace_time_access, code)
        #code = self.pow_pattern.sub(self.replace_exponents, code)

        return code
