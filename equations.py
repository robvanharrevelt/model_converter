import symtab

REFERENCE = 1
BINOP = 2
UNOP = 3
FUNC_CALL = 4
IF_EXPR = 5

equations = []

def init():
    global equations
    equations = []

class Equation(object):
    def __init__(self, lhs, eq_type, rhs):
        self.lhs = lhs
        self.eq_type = eq_type
        self.rhs = rhs

        is_param, var = symtab.check_reference(self.lhs, 0, is_lhs = True)
        self.var = var
        # TODO: error if is_param = FALSE

        equations.append(self)

    def __repr__(self):
        return "Equation{Lhs = %s, Type = %s, Var = %r, Expression = %r}" %  \
                     (self.lhs, self.eq_type, self.var, self.rhs)

class Expression(object):
    def __init__(self, type):
        self.type = type

class Reference(Expression):
    """A reference to a variable or parameter"""

    def __init__(self, name, offset):
        Expression.__init__(self, REFERENCE)
        self.name = name
        self.offset = offset
        is_param, var = symtab.check_reference(self.name, self.offset,
                                               is_lhs = False)
        self.is_param = is_param
        self.var = var


    def __repr__(self):
        return "Reference{name = %s, is_param = %r, offset = %d, var = %r}" \
           % (self.name, self.is_param, self.offset, self.var)


class UnOp(Expression):
    def __init__(self, operator, operand):
        Expression.__init__(self, UNOP)
        self.operator = operator
        self.operand = operand
    def __repr__(self):
        return "UnOp{operator = %s, operand = %s}" % \
                   (self.operator, self.operand)

class BinOp(Expression):
    def __init__(self, operator, left, right):
        Expression.__init__(self, BINOP)
        self.operator = operator
        self.left = left
        self.right = right

    def __repr__(self):
        return "BinOp{Operator = %s, Left = %r, Right = %r}" \
                % (self.operator, self.left, self.right)

class FunctionCall(Expression):
    def __init__(self, function, arguments):
        Expression.__init__(self, FUNC_CALL)
        self.function = function
        self.arguments = arguments
    def __repr__(self):
        return "FunctionCall{function = %s, arguments = %r}" \
                % (self.function, self.arguments)

class IfExpression(Expression):
    def __init__(self, condition, true_expression):
        Expression.__init__(self, IF_EXPR)
        self.condition = condition
        self.true_expression = true_expression
        self.else_expression = None
    def add_else_expression(self, else_expression):
        self.else_expression = else_expression
    def __repr__(self):
        return "IfExpression{condition = %r, true_expression = %r," \
               "else_expression = %r}" % (self.condition, self.true_expression,
                                          self.else_expression)

def dump_equations():
    '''
    Print all equations to the screen (for debugging only)
    :return: none
    '''
    print("List of current equations")
    for equation in equations:
        print(equation)
    print("")
