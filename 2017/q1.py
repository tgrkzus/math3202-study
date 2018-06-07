from gurobipy import *
import random

# Data and ranges
nHospitalSites = 30
nSuburbs = 55
MaxSuburbsPerHospital = 6
MaxPopulation = 500000

H = range(nHospitalSites)
S = range(nSuburbs)

random.seed(3)

FixedCost = [random.randint(5000000,10000000) for h in H]
Population = [random.randint(60000,90000) for s in S]

# Travel distance - multiply by population moved to get travel cost
Dist = [[random.randint(0,50) for s in S] for h in H]

# Set up model and set the gap on the answer to 0
m = Model()
m.setParam('MIPGap', 0)

# Vars
# If a suburb is allocated to a particular hospital
sub = {}
# If this hospital is being built
hos = {}
for h in H:
    hos[h] = m.addVar(vtype=GRB.BINARY)
    for s in S:
        sub[h, s] = m.addVar(vtype=GRB.BINARY)

# Obj
m.setObjective(quicksum(hos[h] * FixedCost[h] for h in H)
               + quicksum(sub[h, s] * Dist[h][s] for h in H for s in S))

# Constraints
for h in H:
    # Limit max suburbs per hospital
    m.addConstr(quicksum(sub[h, s] for s in S) <= MaxSuburbsPerHospital)
    # Limit the population served by a hospital
    m.addConstr(quicksum(sub[h, s] * Population[s] for s in S) <= MaxPopulation)
    # Ensure that if a hospital is serving that it is also built
    m.addConstr(quicksum(sub[h, s] for s in S) <= hos[h] * MaxSuburbsPerHospital)

for s in S:
    # Ensure that each suburb is served by exactly one hospital
    m.addConstr(quicksum(sub[h, s] for h in H) == 1)

m.optimize()

# Display results
totalBuild = 0
totalTransport = 0
for h in H:
    if hos[h].x:
        print("Building", h)
        totalBuild += hos[h].x * FixedCost[h]
        for s in S:
            if sub[h, s].x:
                # print("Serving", s)
                totalTransport += sub[h, s].x * Dist[h][s]
print("Result:")
print(totalBuild + totalTransport)
