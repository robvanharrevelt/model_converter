parameters = {}
variables = {}

def init():
    global parameters
    global variables

    parameters = {}
    variables = {}

class Variable(object):
    def __init__(self, max_lag, max_lead):
        self.is_endo = False   # for the time being assume the variable
                               # is exogenous
        self.offset_range = (max_lag, max_lead)
    def __repr__(self):
       return "Variable{offset_range = %r, is_endo = %r}" %  \
                            (self.offset_range, self.is_endo)

class Parameter(object):
    def __init__(self, value):
      self.value = value
    def __repr__(self):
        return "Parameter{Value = %s}" % self.value

def install_parameter(name, value):
    ''' Add a new parameter to the parameter symbol table.
        TODO: give error if name already installed
        in the symbol table. Also give an error if name
        is present in the variables symbol table.'''
    parameters[name.lower()] = Parameter(value)


def check_reference(name, offset, is_lhs):
    '''Check if the reference with the specified name is a parameter
     or variable. Update the variable reference table if possible'''
     
    name = name.lower()
    if name in parameters:
        par = parameters[name]
        return (True, par)
    else:
        return (False, check_variable(name, offset, is_lhs))

def check_variable(name, offset, is_lhs):
    if not name in variables:
        var = Variable(0, 0)
        variables[name] = var
        var.is_endo = is_lhs
    else:
        var = variables[name]
        var.is_endo = var.is_endo or is_lhs

    (max_lag, max_lead) = var.offset_range
    if offset < 0:
        max_lag = min(max_lag, offset)
    elif offset > 0:
        max_lead = max(max_lead, offset)
    var.offset_range = (max_lag, max_lead)
    return var

def print_parameters():
    print("Parameters in the symbol table:")
    print(parameters)
    print("")

def print_variables():
    print("Variables in the symbol table:")
    print(variables)
    print("")
