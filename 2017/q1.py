from gurobipy import *

# Sets
sections = ["A", "B", "C", "D"]
S = range(len(sections))

# Data
packages = [70, 90, 100, 110, 120, 130, 150, 180, 210, 220, 250, 280, 340, 350, 400]
P = range(len(packages))
MAX_SEC_WEIGHT = 1000
MIN_PACKAGES_SECTION = 3

m = Model()

# Vars
# For a section if it is carrying a certain payload
payload = {}
for s in S:
    for p in P:
        payload[s, p] = m.addVar(vtype=GRB.BINARY)

# Objective (none)

# Constraints
def calcWeight(section):
    return quicksum(packages[p] * payload[section, p] for p in P)

m.addConstr(calcWeight(0) == calcWeight(3))
m.addConstr(calcWeight(1) == calcWeight(2))

#m.addConstr(quicksum(payload[s, p] for p in P for s in S) == len(packages))

for s in S:
    m.addConstr(calcWeight(s) <= MAX_SEC_WEIGHT)
    m.addConstr(quicksum(payload[s, p] for p in P) >= MIN_PACKAGES_SECTION)

for p in P:
    m.addConstr(quicksum(payload[s, p] for s in S) == 1)


m.optimize()

for s in S:
    print(sections[s])
    for p in P:
        if payload[s, p].x:
            print(p, packages[p])
