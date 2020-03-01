import numpy as np
from System import System
import Tree


class Actor:

    def __init__(self, name, index, rationality):

        self.name = name
        self.index = index
        self.rationality = rationality

        self.tree = None

    def __eq__(self, other):

        if type(other) == int:
            return self.index == other

        elif type(other) == Actor:
            return self.index == other.index

    def construct_tree(self, start_config):

        start_config_copy = np.copy(start_config.config)
        start_copy = System(start_config_copy)

        self.tree = Tree.Tree(start_copy)

        num_config = np.power(2, start_copy.Dim)

        start_array = np.zeros(1, dtype=object)
        start_array[0] = start_copy

        prev_layer = start_array
        self.tree.layers.append(prev_layer)

        filtered_configs = set()

        while len(filtered_configs) != num_config:

            new_layer = np.zeros((prev_layer.size, 2 * start_copy.Dim), dtype=object)

            for k, config in enumerate(prev_layer):
                partial_layer = make_tree_layer(config, actor_to_start=self)
                new_layer[k][:] = partial_layer

            prev_layer = new_layer.flatten()

            self.tree.layers.append(new_layer)

            filtered_configs = filter_tree(prev_layer)

        self.tree.filtered = filtered_configs


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
    paths = np.zeros((row, col))

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
            paths[j][index] = delta

            index -= 1
            j_temp //= coeff

            child = parent
            parent = child.parent

    PathIntegral_to_csv(col, paths)

    gain = paths.sum(axis=1)
    return gain


def PathIntegral_to_csv(col, paths):
    string = ''
    for i in range(col):
        string += 'delta{}, '.format(i)
    string = string[:-2]

    np.savetxt(fname='PathIntegralData/paths.csv', X=paths, header=string, comments='', fmt="%d", delimiter=",")
