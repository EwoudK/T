import Tree
import numpy as np
from System import System
from Loose import path_integral, move_up, make_tree_layer, filter_tree


class Actor:

    def __init__(self, name, index, rationality):

        self.name = name
        self.index = index
        self.rationality = rationality

        self.tree = None

        self.highest = 0

    def __eq__(self, other):

        if type(other) == int:
            return self.index == other

        elif type(other) == Actor:
            return self.index == other.index

    def construct_tree(self, start_config, counter=1):

        start_config_copy = np.copy(start_config.config)
        start_copy = System(start_config_copy)

        self.tree = Tree.Tree(start_copy, self.name)

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

        self.tree.print(counter)

        return filtered_configs

    def decide(self, start_config, new_config):

        max_gain, max_index = path_integral(self)
        if max_gain > self.highest:
            self.highest = max_gain

        config = self.tree.layers[-1].flatten()[max_index]
        branch = move_up(config, start_config)

        if self.highest == start_config.gain[self.index]:
            new_config[self.index] = start_config[self.index]

        elif branch[self.index] == start_config[self.index]:
            new_config[self.index] = start_config[self.index]

        else:
            new_config[self.index] = branch[self.index]


England = Actor('England', 0, -1)
France = Actor('France', 1, -1)
Spain = Actor('Spain', 2, -1)
Prussia = Actor('Prussia', 3, -1)

Actors = [England, France, Spain, Prussia]
