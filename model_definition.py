import io
import numpy as np
import equations
from equations import Expression, BINOP, REFERENCE, UNOP, FUNC_CALL, IF_EXPR
import symtab
import equations
import mdl_yacc
import mdl_lex
import os
import shutil
import subprocess
import imp
import sys
import warnings

_operator_precedence = {'&' : 1, '|' : 1, '>' : 2, '>=' : 2, '<' : 2, '<=' : 2,
                        '=' : 2, '!=' : 2, '+' : 3, '-' : 3, '*' : 4, '/' : 4,
                        '**' : 5}


_python_functions = {'exp' : 'np.exp', 'sqrt' : 'np.sqrt', 'log' : 'np.log',
                     'nint' : 'round', 'abs' : 'abs',
                     'max' : 'max', 'min' : 'min'}
_c_functions = {'exp' : 'exp', 'sqrt' : 'sqrt', 'log' : 'log',
                'nint' : 'round', 'abs' : 'fabs',
                'max' : 'max', 'min' : 'min'}
_r_functions = {'exp' : 'exp', 'sqrt' : 'sqrt', 'log' : 'log',
                'nint' : 'round', 'abs' : 'abs',
                'max' : 'max', 'min' : 'min'}
_python_logical_operators = {'&' : ' and ', '|' : ' or '}
_c_logical_operators = {'&' : '&&', '|' : '||'}

def _get_index(name, dict):
    if name in dict:
        i = dict[name]
    else:
        i = len(dict)
        dict[name] = i
    return i

class ModelDefinition(object):

    def __eq__(self, other):
        return (self.name, self.location) == (other.name, other.location)

    def __init__(self, filename, output_type):
        self.filename =  filename
        self.output_type = output_type

        # initialise symbol table and list of equations
        symtab.init()
        equations.init()

        # parse the model file
        model_file = open(self.filename, 'r')
        text = model_file.read()
        model_file.close()
        mdl_yacc.parser.parse(text, lexer = mdl_lex.lexer)

        # generate python-code for the model
        self.endo_dict = {}
        self.exo_dict = {}
        self.lag_dict = {}
        self.par_dict = {}
        self.frmls = []
        self.maxlag = 0
        self.maxlead = 0
        self.equations = self._generate_equations(equations.equations)

        # now take the inverse of the dictionaries dictionaries
        self.endo_dict = {self.endo_dict[k] : k for k in self.endo_dict}
        self.exo_dict = {self.exo_dict[k] : k for k in self.exo_dict}
        self.lag_dict = {self.lag_dict[k] : k for k in self.lag_dict}
        self.par_dict = {self.par_dict[k] : k for k in self.par_dict}

        self.variables = list(symtab.variables.keys())
        self.variables.sort()

        self.endo_indices = np.empty(len(self.endo_dict), dtype = 'int32')
        for (key, value) in self.endo_dict.items():
            self.endo_indices[key] = self.variables.index(value)

        self.exo_indices = np.empty(len(self.exo_dict), dtype = 'int32')
        for (key, value) in self.exo_dict.items():
            self.exo_indices[key] = self.variables.index(value)

        self.lag_indices = []
        for (key, value) in self.lag_dict.items():
            (var, offset) = value
            index = self.variables.index(var)
            self.lag_indices.append((index, offset))

        self.frml_indices = [self.variables.index(x) for x in self.frmls]

        self.parameter_values = np.empty(len(self.par_dict))
        for i in self.par_dict.keys():
            self.parameter_values[i] = symtab.parameters[self.par_dict[i]].value

        if self.output_type == "C":
            self._write_c_code()
        elif self.output_type == "Python":
            self._write_python_code()
        elif self.output_type == "R":
            self._write_r_code()
        else:
            raise RuntimeError("Illegal output type %s\n", self.output_type)


    def __str__(self):
        output = io.StringIO()
        output.write("ModelDefinition\n")
        output.write("Filename =  %s\n" % self.filename)
        output.write("Number of endogenous variables: %d\n" % len(self.endo_dict))
        output.write("Number of exogenous variables: %d\n" % len(self.exo_dict))
        output.write("Number of frmls: %d\n" % len(self.frmls))
        output.write("Maximum lag: %d\n" % self.maxlag)
        output.write("Maximum lead: %d\n" % self.maxlead)
        description  = output.getvalue()
        output.close()
        return description

    def __repr__(self):
        output = io.StringIO()
        output.write("ModelDefinition\n")
        output.write("Filename =  %s\n" % self.filename)
        output.write("Number of endogenous variables: %d\n" % len(self.endo_dict))
        output.write("Number of exogenous variables: %d\n" % len(self.exo_dict))
        output.write("Number of frmls: %d\n" % len(self.frmls))
        output.write("Maximum lag: %d\n" % self.maxlag)
        output.write("Maximum lead: %d\n" % self.maxlead)
        output.write("Endogenous variables:\n%r\n" % self.endo_dict)
        output.write("Exogenous variables:\n%r\n" % self.endo_dict)
        output.write("Frmls:\n%r\n" % self.frmls)
        output.write("Lags/leads:\n %r\n" % self.lag_dict)
        output.write("Code:\n%s" % self.code)
        output.write("Variables:\n%r\n" % self.variables)
        output.write("Endo indices:\n%r\n" % self.endo_indices)
        output.write("Exo indices:\n%r\n" % self.exo_indices)
        output.write("Lag indices:\n%r\n" % self.lag_indices)
        output.write("Frml indices:\n%r\n" % self.frml_indices)
        description  = output.getvalue()
        output.close()
        return description

    def _get_endo_index(self, name):
        if self.output_type == "R":
            return _get_index(name, self.endo_dict) + 1
        else:
            return _get_index(name, self.endo_dict)

    def _get_exo_index(self, name):
        if self.output_type == "R":
            return _get_index(name, self.exo_dict) + 1
        else:
            return _get_index(name, self.exo_dict)

    def _get_par_index(self, name):
        if self.output_type == "R":
            return _get_index(name, self.par_dict) + 1
        else:
            return _get_index(name, self.par_dict)

    def _get_lag_index(self, name, offset):
        lag_var = (name, offset)
        if self.output_type == "R":
            return _get_index(lag_var, self.lag_dict) + 1
        else:
            return _get_index(lag_var, self.lag_dict)

    def _generate_equations(self, equations):
        ret = []
        for eq in equations:
            endo_index = self._get_endo_index(eq.lhs)
            is_frml = eq.eq_type == "frml"
            self._output = io.StringIO()
            self._output_expr(eq.rhs)
            rhs = self._output.getvalue()
            self._output.close()
            lhs = 'x[%d]' % endo_index
            if is_frml:
                frml_index = len(self.frmls)
                self.frmls.append(eq.lhs)
            else:
                frml_index = -1
            ret.append((eq.lhs, frml_index, lhs, rhs))
        return ret

    def _write_c_code(self):
        """
        Write c code for the model equations
        """

        filename = os.path.splitext(self.filename)[0] + ".c"
        output = open(filename, 'w')
        output.write("""
#include <math.h>
#define max(A, B) ((A) > (B) ? (A) : (B))
#define min(A, B) ((A) < (B) ? (A) : (B))
void run_model_c(double* x, double* x2, double *z, double *d, double* a,
                 int* fix, double* fixval, double *p) {
""")
        if len(self.frmls) > 0:
            output.write("    double rhs;\n")
        for (lhs_name, frml_index, lhs, rhs) in self.equations:
            if frml_index >= 0:
                output.write("    rhs = %s;\n" % rhs)
                output.write("    if (fix[%d]) {\n" % frml_index)
                output.write("        %s = fixval[%d];\n" % (lhs, frml_index))
                output.write("        a[%d] = %s - rhs;\n" % (frml_index, lhs))
                output.write("    } else {\n")
                output.write("        %s = rhs + a[%d];\n    }\n" % (lhs, frml_index))
            else:
                output.write("    %s = %s;\n" % (lhs, rhs))
        output.write("}")
        output.close()

    def _write_python_code(self):
        """
        Generate pure Python code for the current model.
        :return the generated Python code
        """
        filename = os.path.splitext(self.filename)[0] + ".py"
        output = open(filename, 'w')
        output.write("""
def run_model_py(x, x2, z, d, a, fix, fixval, p):
""")
        for (lhs_name, frml_index, lhs, rhs) in self.equations:
            if frml_index >= 0:
                output.write("    rhs = %s\n" % rhs)
                output.write("    if fix[%d]:\n" % frml_index)
                output.write("        %s = fixval[%d]\n" % (lhs, frml_index))
                output.write("        a[%d] = %s-rhs\n" % (frml_index, lhs))
                output.write("    else:\n")
                output.write("        %s = rhs + a[%d]\n" % (lhs, frml_index))
            else:
                output.write("    %s = %s\n" % (lhs, rhs))
        output.close()

    def _write_r_code(self):
        """
        Write R code for the model equations
        """

        filename = os.path.splitext(self.filename)[0] + ".R"
        output = open(filename, 'w')
        output.write("""
run_model_r <- function(x, x2, z, d, a, fix, fixval, p) {
""")
        for (lhs_name, frml_index, lhs, rhs) in self.equations:
            if frml_index >= 0:
                output.write("    rhs <- %s;\n" % rhs)
                output.write("    if (fix[%d]) {\n" % (frml_index + 1))
                output.write("        %s <- fixval[%d];\n" % (lhs, 
                                                              frml_index + 1))
                output.write("        a[%d] <- %s - rhs;\n" % (frml_index + 1, lhs))
                output.write("    } else {\n")
                output.write("        %s <- rhs + a[%d];\n    }\n" % (lhs,
                    frml_index + 1))
            else:
                output.write("    %s <- %s;\n" % (lhs, rhs))
        output.write("}")
        output.close()


    def _output_reference(self, refr):
        if refr.is_param:
            self._output.write("p[%d]" % self._get_par_index(refr.name))
        elif refr.offset != 0:
            self._output.write("d[%d]" % self._get_lag_index(refr.name,
                                                             refr.offset))
            if refr.offset < 0:
                self.maxlag = max(self.maxlag, -refr.offset)
            else:
                self.maxlead = max(self.maxlead, refr.offset)
        else:
            var = refr.var
            if var.is_endo:
                self._output.write("x2[%d]" % self._get_endo_index(refr.name))
            else:
                self._output.write("z[%d]" % self._get_exo_index(refr.name))

    def _output_expr(self, expr):
        if isinstance(expr, Expression):
            if expr.type == BINOP:
                self._output_binop(expr)
            elif expr.type == REFERENCE:
                self._output_reference(expr)
            elif expr.type == IF_EXPR:
                self._output_if_expr(expr)
            elif expr.type == UNOP:
                self._output_unop(expr)
            elif expr.type == FUNC_CALL:
                self._output_func_call(expr)
        else:
            # expr is a numerical constant
            self._output.write(repr(float(expr)))


    def _output_operand(self, operator, is_right, expr):
        """
        Output an operand of a binary or unary operator. Parentheses are
        added if necessary
        :param expr: the expression of the operand
        :return: None
        """

        # check if parentheses around the expression are required
        if  not isinstance(expr, Expression) or expr.type != BINOP:
            add_par = False
        elif operator == "**":
            # always use parantheses for clarity
            add_par = True
        else:
            p_op   = _operator_precedence[operator]
            p_next = _operator_precedence[expr.operator]
            if p_op > p_next:
                add_par = True
            elif p_op == p_next and (operator == "-" or operator == "/"):
                add_par = is_right
            else:
                add_par = False

        if add_par:
            self._output.write("(")
        self._output_expr(expr)
        if add_par:
            self._output.write(")")

    def _output_unop(self, expr):
        if (expr.operator == "+"):
            self._output_expr(expr.operand)
        else:
            self._output.write(expr.operator)
            self._output_operand(expr.operator, True, expr.operand)

    def _output_binop(self, expr):
        if self.output_type == "C" and expr.operator == '**':
            self._output.write("pow(")
            self._output_expr(expr.left)
            self._output.write(',')
            self._output_expr(expr.right)
            self._output.write(')')
        else:
            self._output_operand(expr.operator, False, expr.left)
            if expr.operator == '=':
                op = '=='
            elif expr.operator == '&' or expr.operator == '|':
                if self.output_type  == "C" or self.output_type  == "R" :
                    op = _c_logical_operators[expr.operator]
                else:
                    op = _python_logical_operators[expr.operator]
            else:
                op = expr.operator
            self._output.write(op)
            self._output_operand(expr.operator, True, expr.right)

    def _output_func_call(self, expr):
        if self.output_type == "C":
            self._output.write(_c_functions[expr.function])
        elif self.output_type == "Python":
            self._output.write(_python_functions[expr.function])
        else:
            self._output.write(_r_functions[expr.function])
        # todo: check if the number of arguments is compatible with
        # function definition
        # todo: currently, max and min are only implemented for 2 arguments
        self._output.write("(")
        for i in range(len(expr.arguments)):
            self._output_expr(expr.arguments[i])
            if i < len(expr.arguments) - 1:
                self._output.write(",")
        self._output.write(")")


    def _output_if_expr(self, expr):
        self._output.write("(")
        if self.output_type == "C":
            self._output_expr(expr.condition)
            self._output.write(" ? ")
            self._output_expr(expr.true_expression)
            self._output.write(" : ")
            self._output_expr(expr.else_expression)
        elif self.output_type == "Python":
            self._output_expr(expr.true_expression)
            self._output.write("if ")
            self._output_expr(expr.condition)
            self._output.write(" else ")
            self._output_expr(expr.else_expression)
        elif self.output_type == "R":
            self._output_expr(expr.true_expression)
            self._output.write("if (")
            self._output_expr(expr.condition)
            self._output.write(") else (")
            self._output_expr(expr.else_expression)
        self._output.write(")")

    def __getstate__(self):
        """Return state values to be pickled."""
        state = self.__dict__.copy()

        # Remove the unpicklable entries.
        if 'code_mod' in state.keys():
            del state['code_mod']
        if '_output' in state.keys():
             del state['_output']
        return state


    def __setstate__(self, state):
        """Restore state from the unpickled state values."""

        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)
