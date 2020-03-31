import Tree
import numpy as np
from Loose import path_integral, move_up, make_tree_layer, filter_tree


class Actor:

    def __init__(self, name, rationality, propensities, belonging):

        self.name = name
        self.rationality = rationality
        self.propensities = propensities
        self.belonging = belonging

        self.tree = None

        self.highest = 0

    def construct_tree(self, start_config, counter=1):

        start_copy = start_config.copy()
        self.tree = Tree.Tree(start_copy, self.name)

        num_config = np.power(2, start_copy.Dim)

        start_array = np.full(1, start_copy, dtype=object)

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

    def decide(self, start_config, new_config):
        index = start_config.actors.index(self)
        max_gain, target_index = path_integral(self, index)

        if max_gain > self.highest:
            self.highest = max_gain

        config = self.tree.layers[self.rationality].flatten()[target_index]
        branch = move_up(config, start_config)

        if self.highest == start_config.gain[index]:
            new_config[index] = start_config[index]

        elif start_config.gain[index] == max_gain*-1:
            chance = np.random.random()
            if chance > 0.3:
                new_config[index] = start_config[index]*-1
            else:
                new_config[index] = start_config[index]

        else:
            new_config[index] = branch[index]
