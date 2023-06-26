
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