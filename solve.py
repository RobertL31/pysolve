    
from constraints import LessThan, NotEqual


def create_decision(variables):
    var, dom = next(filter(lambda v: len(v[1]) > 1, variables.items()), (None, None))
    if var is not None:
        return var, min(dom)
    
    return (None, None)


def copy_domains(variables):
    return {var: dom.copy() for var, dom in variables.items()}


def propagate(variables, var, val, apply, constraint):
    c_variables = copy_domains(variables)
    c_variables[var] = [x for x in c_variables[var] if apply is (x == val)]
    return enumerate(c_variables, constraint)


def enumerate(variables, constraints):
    if not fix_point(variables, constraints):
        return 0
    
    var, val = create_decision(variables)
    if var is None:
        print(variables)
        return 1
    
    n = propagate(variables, var, val, True, constraints)
    n += propagate(variables, var, val, False, constraints)
    return n


def fix_point(variables, constraints):
    modified = True
    while modified:
        modified = False
        for c in constraints:
            filter_result = c.filter(variables)
            if filter_result is False:
                return False
            if filter_result is True:
                modified = True
    return True
    
    
def main():
    variables = {
        'x1': [1, 2, 3],
        'x2': [1, 2, 3],
        'x3': [1, 2, 3],
    }

    c1 = LessThan('x1', 'x2')
    c2 = NotEqual('x1', 'x3', 1)
    constraints = [c1, c2]
    
    print('sols : ', enumerate(variables, constraints))


if __name__ == '__main__':
    main()
    