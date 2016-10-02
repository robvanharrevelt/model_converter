import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from mdl_lex import tokens
import equations
from equations import Equation, Reference, BinOp, UnOp, FunctionCall, \
                      IfExpression, IF_EXPR
import symtab

# Build the parser

# define the precedence and associativity
precedence = (
    ('left', 'AND', 'OR'),
    ('left', 'GT', 'GE', 'LT', 'LE', 'EQUAL', 'NE'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'POWER'),
    ('right', 'UMINUS'),   # Unary minus and plus operator
)


def p_statements(p):
    """statements : statement
                  | statements statement"""

def p_statement(p):
    """statement : equation
                 | parameters"""

def p_equation(p):
    """equation : EQ_TYPE NAME EQUAL expression STOP"""
    p[0] = Equation(p[2], p[1], p[4])

def p_expression(p):
    """expression : number
                  | variable
                  | binop
                  | unop
                  | group
                  | func_call
                  | if_expr"""
    p[0] = p[1]

def p_variable(p):
    """variable : NAME
                | NAME LBRACKET signed_integer RBRACKET"""
    if len(p) == 2:
        p[0] = Reference(p[1], 0)
    else:
        p[0] = Reference(p[1], p[3])

def p_sign(p):
    """sign : PLUS
            | MINUS"""
    p[0] = p[1]

def p_signed_integer(p):
    """signed_integer : INTEGER
                      | sign INTEGER"""
    if len(p) == 3:
        if p[1] == '-':
            p[0] = -p[2]
        else:
            p[0] = p[2]
    else:
        p[0] = p[1]

def p_number(p):
    """number : INTEGER
              | FLOAT"""
    p[0] = p[1]

def p_signed_number(p):
    """signed_number : number
                     | sign number"""
    if len(p) == 3 and p[1] == '-':
        p[0] = -p[2]
    else:
        p[0] = p[1]

def p_unop(p):
    """unop : sign expression %prec UMINUS"""
    p[0] = UnOp(p[1], p[2])

def p_binop(p):
    """binop : expression PLUS expression
             | expression MINUS expression
             | expression TIMES expression
             | expression DIVIDE expression
             | expression POWER expression
             | expression GT expression
             | expression GE expression
             | expression LE expression
             | expression LT expression
             | expression EQUAL expression
             | expression NE expression
             | expression AND expression
             | expression OR expression"""
    p[0] = BinOp(p[2], p[1], p[3])

def p_group(p):
    """ group : LPAREN expression RPAREN"""
    p[0] = p[2]

def p_func_call(p):
    # currently only functions with one argument allowed
    """ func_call : NAME LPAREN p_actuals RPAREN"""
    p[0] = FunctionCall(p[1], p[3])


def p_actuals(p):
    # actual argument of a function call
    """ p_actuals : expression
                  | p_actuals COMMA expression"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])

def p_if_expr(p):
    """ if_expr : if_conditions ELSE expression ENDIF"""
    p[0] = p[1]

    # add the else part to the correct place in the tree
    expr = p[0]
    while expr.else_expression != None:
        expr = expr.else_expression
    expr.add_else_expression(p[3])

def p_if_conditions(p):
    """ if_conditions : if_then
                      | if_then elseif_sequence"""
    p[0] = p[1]
    if len(p) == 3:
        p[0].add_else_expression(p[2])

def p_if_then(p):
    """ if_then : IF expression THEN expression"""
    p[0] = IfExpression(p[2], p[4])

def p_elseif_sequence(p):
    """ elseif_sequence : elseif
                        | elseif_sequence elseif"""
    p[0] = p[1]
    if len(p) == 3:
        expr = p[0]
        while expr.else_expression != None:
            expr = expr.else_expression
        expr.add_else_expression(p[2])

def p_elseif(p):
    """ elseif : ELSEIF expression THEN expression"""
    p[0] = IfExpression(p[2], p[4])


def p_parameters(p):
    """parameters : PARAM parameter_list STOP"""
    pass

def p_parameter_list(p):
    """parameter_list : parameter
                      | parameter_list parameter"""

def p_parameter(p):
    """parameter : NAME signed_number"""
    p[0] = symtab.install_parameter(p[1], p[2])

# Error rule for syntax errors
def p_error(p):
    if p is not None:
        print ("Line %s, illegal token %s" % (p.lineno, p.value))
        parser.errok()
    else:
        print('Unexpected end of input');

parser = yacc.yacc(tabmodule='mdlcompiler_parsetab')
