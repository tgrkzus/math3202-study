from collections import namedtuple

seasons = [155, 120, 140, 100, 155]

State = namedtuple('State', 'employees')


def operators(t, s):
    thisSeasonOverCost = (s.employees - seasons[t]) * 2000
    if t == 4:
        return thisSeasonOverCost
    else:
        results = []
        if s.employees <= seasons[t + 1] + 1:
            possibles = range(s.employees, seasons[t + 1] + 1)
        else:
            possibles = range(seasons[t + 1] + 1, s.employees)
        print(possibles)
        for nextOperators in possibles:
            newState = State(nextOperators)
            hireCost = (nextOperators - s.employees)**2 * 200
            results.append(thisSeasonOverCost + hireCost + operators(t + 1, newState))
        return max(results)



# STart with 155 employees
print(operators(0, State(155)))