domains = {
    'X1': list(range(0, 16)),  # 0 a 15
    'X2': list(range(0, 11)),  # 0 a 10
    'X3': list(range(0, 26)),  # 0 a 25
    'X4': list(range(0, 5)),   # 0 a 4
    'X5': list(range(0, 31))   # 0 a 30
}

constraints = {
    ('X1',): lambda X1: X1 <= 15,
    ('X2',): lambda X2: X2 <= 10,
    ('X3',): lambda X3: X3 <= 25,
    ('X4',): lambda X4: X4 <= 4,
    ('X5',): lambda X5: X5 <= 30,
    ('X1', 'X2'): lambda x1, x2: 194 * x1 + 320 * x2 <= 3800,
    ('X2', 'X1'): lambda x2, x1: 194 * x1 + 320 * x2 <= 3800,
    ('X3', 'X4'): lambda x3, x4: 68 * x3 + 113 * x4 <= 2800,
    ('X4', 'X3'): lambda x4, x3: 68 * x3 + 113 * x4 <= 2800,
    ('X3', 'X5'): lambda x3, x5: 68 * x3 + 17 * x5 <= 3500,
    ('X5', 'X3'): lambda x5, x3: 68 * x3 + 17 * x5 <= 3500
}

def revise(x, y):
    revised = False
    x_domain = domains[x][:]
    y_domain = domains[y] if y in domains else []
    all_constraints = [
        constraint for constraint in constraints if len(constraint) == 2 and constraint[0] == x and constraint[1] == y]
    for x_value in x_domain:
        satisfies = False
        for y_value in y_domain:
            for constraint in all_constraints:
                constraint_func = constraints[constraint]
                if constraint_func(x_value, y_value):
                    satisfies = True
        if not satisfies:
            domains[x].remove(x_value)
            revised = True
    return revised

def ac3(arcs):
    queue = arcs[:]
    while queue:
        (x, y) = queue.pop(0)
        revised = revise(x, y)
        if revised:
            neighbors = [neighbor for neighbor in arcs if neighbor[1] == x]
            queue = queue + neighbors

arcs = [
    ('X1', 'X2'), ('X2', 'X1'),  # Restricción: 194x1 + 320x2 ≤ 3800
    ('X3', 'X4'), ('X4', 'X3'),  # Restricción: 68x3 + 113x4 ≤ 2800
    ('X3', 'X5'), ('X5', 'X3')   # Restricción: 68x3 + 17x5 ≤ 3500
]

ac3(arcs)

print(domains)