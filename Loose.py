import numpy as np
from System import System


def make_tree_layer(start, actor_to_start):

    flip = start.flip(actor_to_start)

    choice_nodes = [start, flip]
    temp_config_nodes = np.zeros((2, start.Dim), dtype=object)
    start.children = np.zeros(2 * start.Dim, dtype=object)

    test_index = 0
    for i, choice in enumerate(choice_nodes):
        j = 0

        copy = System(choice.config)
        copy.parent = start

        temp_config_nodes[i][j] = copy
        start.children[test_index] = copy
        test_index += 1

        for index in range(start.Dim):
            if index != actor_to_start:
                j += 1

                new_config = choice.flip(index)
                new_config.parent = start
                start.children[test_index] = new_config

                test_index += 1

                temp_config_nodes[i][j] = new_config

    temp_config_nodes = temp_config_nodes.flatten()

    return temp_config_nodes


def filter_tree(config_set):

    temp = list(config_set)
    filtered = set(temp)
    return filtered


def find_degeneracies(actor):

    depth = 0
    if (actor.rationality < 0) or (actor.rationality > len(actor.tree.layers)):
        depth = len(actor.tree.layers)
    elif actor.rationality < len(actor.tree.layers):
        depth = actor.rationality

    degeneracy_books = [[{actor.tree.start: 1}]]
    for layer in actor.tree.layers[1:depth]:

        layer_list = []
        for sub_layer in layer:
            sorted_layer = sorted(sub_layer.tolist(), key=lambda x: x.gain[actor.index], reverse=True)
            config_degeneracies = count_degeneracy(actor, sorted_layer)
            layer_list.append(config_degeneracies)
        degeneracy_books.append(layer_list)

    return degeneracy_books


def count_degeneracy(actor, layer):

    config_count = {}

    elem = layer[0]
    count_j = 1

    length = len(layer)

    for i in range(1, length):
        next_elem = layer[i]
        if next_elem.gain[actor.index] != elem.gain[actor.index]:
            config_count[elem.gain[actor.index]] = count_j
            count_j = 1
            elem = next_elem
            if i == length-1:
                config_count[next_elem.gain[actor.index]] = count_j

        elif next_elem.gain[actor.index] == elem.gain[actor.index]:
            count_j += 1
            if i == length-1:
                config_count[elem.gain[actor.index]] = count_j

    return config_count


def path_integral(actor):

    degeneracy_books = find_degeneracies(actor)

    layer = actor.tree.layers[actor.rationality].flatten()
    row = len(layer)
    col = len(degeneracy_books) - 1

    deltas = np.zeros((row, col))
    paths = np.zeros((row, col+1))

    for j, child in enumerate(layer):

        coeff = np.power(child.Dim, 2)
        index = -1
        j_temp = j // coeff

        parent = child.parent
        while parent is not None:

            if len(degeneracy_books[index]) == 1:
                degeneracy_child = 1

            else:
                degeneracy_child = degeneracy_books[index][j_temp][child.gain[actor.index]]

            if len(degeneracy_books[index-1]) == 1:
                degeneracy_parent = 1

            else:
                degeneracy_parent = degeneracy_books[index-1][j_temp//coeff][parent.gain[actor.index]]

            delta = child.gain[actor.index]*degeneracy_child - parent.gain[actor.index]*degeneracy_parent
            deltas[j][index] = delta

            paths[j][index] = child.gain[actor.index]

            index -= 1
            j_temp //= coeff

            child = parent
            parent = child.parent
            if parent is None:
                paths[j][index] = child.gain[actor.index]

    PathIntegral_to_csv(col, paths)

    max_config = paths[-1].max()
    gain = np.array([x for i, x in enumerate(paths) if paths[i][-1] == max_config])
    summed_gain = gain.sum(axis=1)

    max_gain = gain.sum(axis=1).max()
    max_index = np.where(summed_gain == max_gain)

    return max_gain, max_index


def PathIntegral_to_csv(col, paths):
    string = ''
    for i in range(col+1):
        string += 'config{}, '.format(i)
    string = string[:-2]

    np.savetxt(fname='PathIntegralData/paths.csv', X=paths, header=string, comments='', fmt="%d", delimiter=",")


def move_up(config, start_config):

    child = config
    parent = child.parent

    while not parent == start_config:
        child = parent
        parent = child.parent

    return child