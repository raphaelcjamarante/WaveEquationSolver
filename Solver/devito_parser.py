from sympy.codegen.ast import *
from sympy.abc import u
from sympy.core.relational import Eq
from sympy.core.symbol import Symbol
import re

class Parser:
    """ This class is dedicated to translate a Devito symbolic expression into a SymPy symbolic expression.
        Passed function can have any name; it will be translated into 'u'
    """
    def __init__(self, equation):
        self.expression = str(equation)
        self.free_symbols = [str(symbol) for symbol in equation.free_symbols]

        # Finds functions with the name previously defined
        self.function_pattern = re.compile(f'{equation.lhs.name}\((.*?)\)')

        # Finds decimal point numbers
        self.float_pattern = re.compile("\d+\.\d+")

        # Finds any word, but we compare it to free symbols
        self.free_symbol_pattern = re.compile("\w+")


    def parameters_indexing(self, parameters):
        """ The n-dim array that represents the problem is divided in the number of steps of each dimension.
            To access each element of the array, the indexes should be integers, so we substitute the step markers for 1
        """
        step_markers = ["dt", "h_x", "h_y"]
        for step in step_markers:
            parameters = parameters.replace(step, '1')
        return parameters

    def replace_functions(self, match):
        """ Substitute functions in the format f(t,x,y) for the symbolic representation of their array
            counterpart f[t][x][y] (but with the name changed to 'u'), that is, Element('u', 'txy')
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

    def translate_expression(self):
        """ Transform a Devito expression in a SymPy expression by calling the transformations in the correct order """
        transform = self.function_pattern.sub(self.replace_functions, self.expression)
        transform = self.free_symbol_pattern.sub(self.replace_free_symbols, transform)
        transform = self.float_pattern.sub(self.replace_floats, transform)
        return eval(transform)
