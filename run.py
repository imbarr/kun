from collections import defaultdict
import re


def to_network(bipartial):
    x, y = len(bipartial), len(bipartial[0])
    result = [[False for _ in range(y + x + 2)] for _ in range(y + x + 2)]
    for i, line in enumerate(bipartial):
        for j, is_present in enumerate(line):
            if is_present:
                result[i][x + j] = True
    source = x + y
    sink = x + y + 1
    for i in range(x):
        result[source][i] = True
    for i in range(y):
        result[x + i][sink] = True

    return result, source, sink


def augmenting_path(network, source, sink, flow):
    stack = [source]
    old = {source}
    while stack:
        current = stack.pop()
        for next in range(len(network)):
            forward = network[current][next] and flow[(current, next)] < 1
            backward = network[next][current] and flow[(next, current)] > 0
            if (forward or backward) and next not in old:
                stack.append(current)
                stack.append(next)
                old.add(next)
                if next == sink:
                    return stack
                break


def ford_fulkerson(network, source, sink):
    flow = defaultdict(lambda: 0)
    path = augmenting_path(network, source, sink, flow)
    while path is not None:
        for a, b in zip(path, path[1:]):
            if network[a][b]:
                flow[(a, b)] += 1
            else:
                flow[(b, a)] -= 1
        path = augmenting_path(network, source, sink, flow)
    return flow


with open('input.txt', 'r') as f:
    x, y = map(int, next(f).split(' '))
    bipartial = [[i == '1' for i in re.findall(r'[10]', next(f))] for _ in range(x)]

    flow = ford_fulkerson(*to_network(bipartial))
    matching = set()
    for a in range(x):
        for b in range(x, x + y):
            if flow[(a, b)] == 1:
                matching.add((a, b - x))

    with open('output.txt', 'w') as f:
        if len(matching) == x:
            matrix = [['0' for _ in range(x)] for _ in range(y)]
            for a, b in matching:
                matrix[a][b] = '1'
            f.write('\n'.join(map(' '.join, matrix)))
        else:
            f.write(str(min(set(range(x)) - {edge[0] for edge in matching}) + 1))
