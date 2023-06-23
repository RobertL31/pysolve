

class BinaryConstraint:
    
    def __init__(self, v1, v2, **kwargs):
        self.v1 = v1
        self.v2 = v2
        
        
class LessThan(BinaryConstraint):
    
    def __init__(self, v1, v2):
        super().__init__(v1, v2)

    
    def filter(self, variables):
        d1 = variables[self.v1]
        d2 = variables[self.v2]
        prefilter_size = len(d1) + len(d2)
        
        d1 = [value for value in d1 if value < max(d2)]
        postfilter_d1_size = len(d1)
        if postfilter_d1_size == 0:
            return False
        d2 = [value for value in d2 if value > min(d1)]
        postfilter_d2_size = len(d2)
        if postfilter_d2_size == 0:
            return False
        
        variables[self.v1] = d1
        variables[self.v2] = d2
        return prefilter_size - postfilter_d1_size - postfilter_d2_size > 0 or None
        
        
class NotEqual(BinaryConstraint):
    
    def __init__(self, v1, v2, c=0):
        super().__init__(v1, v2)
        self.c = c
        
        
    def filter(self, variables):
        d1 = variables[self.v1]
        d2 = variables[self.v2]
        prefilter_size = len(d1) + len(d2)
        
        if len(d2) == 1:
            d1 = [value for value in d1 if value != (d2[0] + self.c)]
            if len(d1) == 0:
                return False
        
        if len(d1) == 1:
            d2 = [value for value in d2 if value != (d1[0] - self.c)]
            if len(d2) == 0:
                return False
        
        variables[self.v1] = d1
        variables[self.v2] = d2
        
        return prefilter_size - len(d1) - len(d2) > 0 or None


        
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
    