from collections import namedtuple

# Last draw, grid [tl, tr, bl, br]
State = namedtuple('State', ['drawn', 'grid'])


def calcResult(state):
    top = 10 * state.grid[0] + state.grid[1]
    bot = 10 * state.grid[2] + state.grid[3]
    return top * bot


def getPossibleCards(state):
    used = list(state.grid)
    used.append(state.drawn)
    return [x for x in range(10) if x not in used]

results = {}

def cards(t, s):
    result = 0
    possibles = getPossibleCards(s)
    targets = [x for x in range(len(s.grid)) if s.grid[x] == -1]
    if t == 3:
        for a in targets:
            s.grid[a] = s.drawn
            result = (calcResult(s), a)
    else:
        paths = []
        for a in targets:
            v = 0
            for c in possibles:
                newGrid = list(s.grid)
                newGrid[a] = s.drawn
                nextState = State(c, newGrid)
                v += (1 / len(possibles)) * cards(t + 1, nextState)[0]
            paths.append((v, a))
        result = min(paths)
    return result

print(cards(0, State(7, [-1, -1, -1, -1])))
