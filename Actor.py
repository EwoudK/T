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

    def make_tree(self, start_config):

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

    def find_highest_gain(self):

        depth = 0

        if (self.rationality < 0) or (self.rationality > len(self.tree.layers)):
            depth = len(self.tree.layers)-1
        elif self.rationality < len(self.tree.layers):
            depth = self.rationality-1

        layer = self.tree.layers[depth]

        local_gain = 0
        way_to_go = None

        for sub_layer in layer:
            sorted_layer = sorted(sub_layer.tolist(), key=lambda x: x.gain[self.index], reverse=True)
            degenerate_configs = extract(self, sorted_layer)
            path_gain, choice = path_integral(self, degenerate_configs[0], len(degenerate_configs))
            if path_gain > local_gain:
                local_gain = path_gain
            way_to_go = choice

        return way_to_go

    def make_choice(self):

        choice = self.find_highest_gain()
        if choice[self.index] != self.tree.start[self.index]:
            print('flip')
        else:
            print('no flip')


England = Actor('England', 0, -1)
Spain = Actor('Spain', 1, -1)
France = Actor('France', 2, -1)
Actors = [England, Spain, France]


def filter_tree(config_set):

    temp = list(config_set)
    filtered = set(temp)
    return filtered


def compare(x, actor):

    return x.gain[actor.index]


def extract(actor, sorted_layer):

    degenerate_configs = [sorted_layer[0]]
    for elem in sorted_layer[1:]:
        if elem.gain[actor.index] != sorted_layer[0].gain[actor.index]:
            break

        else:
            degenerate_configs.append(elem)

    return degenerate_configs


def make_tree_layer(start, actor_to_start, actors=Actors):

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

        for other_actor in actors:
            if other_actor != actor_to_start:
                j += 1

                new_config = choice.flip(other_actor)
                new_config.parent = start
                start.children[test_index] = new_config

                test_index += 1

                temp_config_nodes[i][j] = new_config

    temp_config_nodes = temp_config_nodes.flatten()

    return temp_config_nodes


def path_integral(actor, leaf, degeneracy_leaf):

    choice = None
    total_gain = degeneracy_leaf*leaf.gain[actor.index]
    while leaf.parent is not None:
        total_gain += leaf.parent.gain[actor.index]
        leaf = leaf.parent
        if leaf.parent is not None:
            choice = leaf

    return total_gain, choice
