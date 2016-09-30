import ply.lex as lex

tokens = (
    "FLOAT",
    "INTEGER",
    "NAME",
    "EQUAL",
    "STOP",
    "POWER",
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    "LBRACKET",
    "RBRACKET",
    'GT',
    'GE',
    'LT',
    'LE',
    'NE',
    'AND',
    'OR',
    'COMMA'
)

reserved = {
   'frml'  : 'EQ_TYPE',
   'ident' : 'EQ_TYPE',
   'param' : 'PARAM',
   'if'    : 'IF',
   'then'  : 'THEN',
   'else'  : 'ELSE',
   'elseif': 'ELSEIF',
   'endif' : 'ENDIF',
}

tokens = tokens + tuple(set(reserved.values()))

def t_NAME(t):
    r"(?i)[A-Z][A-Z0-9_]*"
    t.value = t.value.lower()
    t.type = reserved.get(t.value, 'NAME')    # Check for reserved words
    return t

def t_POWER(t):
    r"\*\*"
    return t



t_EQUAL = '='
t_STOP = ';'
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_GT = r'>'
t_GE = r'>='
t_LT = r'<'
t_LE = r'<='
t_AND = r'&'
t_OR = r'\|'
t_COMMA = r','

def t_NE(t):
    # both C and Python use != as not equal operator
    r'\^='
    t.value = '!='
    return t

def t_COMMENT(t):
    r'\?.*'
    pass
    # No return value. Token discarded

def t_FLOAT(t):
    r"((\d+\.\d*|\.\d+)([eE][+-]?\d+)?)|(\d+[eE][+-]?\d+)"
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r"\d+"
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_error(t):
    raise(TypeError("Unknown text '%s'" % (t.value,)))

lexer = lex.lex()

#testen van de lexical analyser
# lex.input("""
# param c0 100
# frml a_wn = 0.2 + 4.212 * b_wn;
# ident b_wn = (c_wn + 1) * 2;
# """)
#
# for tok in iter(lex.token, None):
#    print(repr(tok.type), repr(tok.value))

