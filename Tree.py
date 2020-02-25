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
                partial_layer = Tree.make_tree_layer(config, actor_to_start=self)
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
        for sub_layer in layer:
            sorted_layer = sorted(sub_layer.tolist(), key=lambda x: x.gain[self.index], reverse=True)
            print(sorted_layer[0])


def filter_tree(config_set):

    temp = list(config_set)
    filtered = set(temp)
    return filtered


def compare(x, actor):

    return x.gain[actor.index]