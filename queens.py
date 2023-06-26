
from constraints import LessThan, NotEqual
from solve import enumerate

N = 12


def main():
    
    global N

    # one variable per column, value is line index
    var_names = [f"x{i}" for i in range(N)]
    domains = [list(range(N)) for _ in range(N)]
    variables = dict(zip(var_names, domains))

    constraints = []
    for i in range(N):
        for j in range(i+1, N):
            constraints.append(
                NotEqual(f"x{i}", f"x{j}")
            )
            constraints.append(
                NotEqual(f"x{i}", f"x{j}", c=(j-i))
            )
            constraints.append(
                NotEqual(f"x{i}", f"x{j}", c=-(j-i))
            )

    # symetry breaking
    variables['constant'] = {int(N/2)}
    constraints.append(
        LessThan('x0', 'constant')
    )
    
    print(enumerate(variables, constraints))

if __name__ == '__main__':
    main()