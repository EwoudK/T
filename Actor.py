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

    def find_degeneracies(self):

        depth = 0
        if (self.rationality < 0) or (self.rationality > len(self.tree.layers)):
            depth = len(self.tree.layers)
        elif self.rationality < len(self.tree.layers):
            depth = self.rationality

        degeneracy_books = [[{self.tree.start: 1}]]
        for layer in self.tree.layers[1:depth]:

            layer_list = []
            for sub_layer in layer:
                sorted_layer = sorted(sub_layer.tolist(), key=lambda x: x.gain[self.index], reverse=True)
                config_degeneracies = count_degeneracy(self, sorted_layer)
                layer_list.append(config_degeneracies)
            degeneracy_books.append(layer_list)

        return degeneracy_books

    def path_integral(self):

        degeneracy_books = self.find_degeneracies()
        layer = self.tree.layers[self.rationality].flatten()

        row = len(layer)
        col = len(self.tree.layers)-1

        paths = np.zeros((row, col))

        for j, child in enumerate(layer):
            index = -1
            gain = 0
            parent = child.parent

            j_temp = j // 6

            while parent is not None:

                j_next = j_temp // 6

                try:
                    degeneracy_child = degeneracy_books[index][j_temp][child]
                except KeyError:
                    inverse = child.invert()
                    degeneracy_child = degeneracy_books[index][j_temp][inverse]

                try:
                    degeneracy_parent = degeneracy_books[index - 1][j_next][parent]
                except KeyError:
                    inverse = parent.invert()
                    degeneracy_parent = degeneracy_books[index - 1][j_next][inverse]

                delta = child.gain[self.index] * degeneracy_child - parent.gain[self.index] * degeneracy_parent
                print(child.gain[self.index], parent.gain[self.index], degeneracy_child, degeneracy_parent, delta)
                paths[j][index] = delta

                parent = parent.parent
                index -= 1
                j_temp //= 6

                child = parent

        # print(paths)


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


def count_degeneracy(actor, layer):

    config_count = {}

    elem = layer[0]
    count_j = 1

    length = len(layer)

    for i in range(1, length):
        next_elem = layer[i]
        if next_elem.gain[actor.index] != elem.gain[actor.index]:
            config_count[elem] = count_j
            count_j = 1
            elem = next_elem
            if i == length-1:
                config_count[next_elem] = count_j

        elif next_elem.gain[actor.index] == elem.gain[actor.index]:
            count_j += 1
            if i == length-1:
                config_count[elem] = count_j

    return config_count
