from gurobipy import *
import random

# 100 candidate sites
S = range(100)
random.seed(20)

# Drill cost at each site
DrillCost = [random.randint(15000, 60000) for s in S]

# 30 groups with between 5 and 10 elements in every group
Group = [sorted(random.sample(S, random.randint(5, 10))) for i in range(30)]
G = range(len(Group))
print(DrillCost)
print(Group)

PENALTY = 10000

m = Model()

# Vars
# If a site is chosen
Site = {}
# How many sites chosen in this group
Groups = {}
for s in S:
    Site[s] = m.addVar(vtype=GRB.BINARY)

for g in G:
    Groups[g] = m.addVar()

# Helpers
def siteCost(v, s):
    return v * DrillCost[s]

def penaltyCost(v):
    if v == 2:
        return 10000
    return 0


# Obj (sum of site costs + sum of penalties)
m.setObjective(quicksum(siteCost(Site[s], s) for s in S) + quicksum(penaltyCost(Groups[g]) for g in G), GRB.MINIMIZE)

# Constraints
m.addConstr(quicksum(Site[s] for s in S) == 20)

for g in G:
    m.addConstr(quicksum(Site[s] for s in Group[g]) <= 2)
    m.addConstr(quicksum(Site[s] for s in Group[g]) == Groups[g])

m.optimize()

# Results
total = 0
for s in S:
    total += siteCost(Site[s].x, s)
    if Site[s].x:
        print(s)
print(total)
# for g in G:
#     total += penaltyCost(Groups[g])
# print(total)
