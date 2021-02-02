# Solve Tower of Hanoi puzzle.
# Return sequence of turns for N disks on the tower A

def get_turns(n, source='A', dist='C', aux='B', turns=[]):
    if n == 1:
        turns.append((source, dist))
        return turns
    get_turns(n-1, source, aux, dist, turns)
    turns.append((source, dist))
    get_turns(n-1, aux, dist, source, turns)
    return turns


state = {'A': 3, 'B': 0, 'C': 0}
TURNS = get_turns(state['A'])
print(f"All {len(TURNS)} turns:")
for source, dist in TURNS:
    print(f'move disk from {source} to {dist}')
    state[source] -= 1
    state[dist] += 1
    print(state)
