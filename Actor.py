import Tree
import json
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

        self.print_energy_degeneracy()

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

    def print_energy_degeneracy(self):

        filtered = self.tree.filtered

        gains = np.array([config.gain.sum() for config in filtered])
        np.savetxt('DegeneracyData/Total/gainhist.csv', gains, header='gains', comments='', fmt="%d", delimiter=",")

        individual_gains = np.array([config.gain[self.index] for config in filtered])
        np.savetxt('DegeneracyData/Individual/gainhist{}.csv'.format(self.name), individual_gains, header='gains', comments='',
                   fmt="%d", delimiter=",")

        gain_dict = {}
        for config in filtered:
            gain = config.gain.sum()

            if gain in gain_dict:
                gain_dict[gain].append(config.config.tolist())
            else:
                gain_dict[gain] = [config.config.tolist()]
        with open('DegeneracyData/Total/gainstoconfigs.json', 'w') as fp:
            json.dump(gain_dict, fp=fp, sort_keys=True, indent=4)

        individual_gain_dict = {}
        for config in filtered:
            individual_gain = config.gain[self.index]

            if individual_gain in individual_gain_dict:
                individual_gain_dict[individual_gain].append(config.config.tolist())
            else:
                individual_gain_dict[individual_gain] = [config.config.tolist()]
        with open('DegeneracyData/Individual/gainstoconfigs{}.json'.format(self.name), 'w') as fp:
            json.dump(individual_gain_dict, fp=fp, sort_keys=True, indent=4)


England = Actor('England', 0, -1)
France = Actor('France', 1, -1)
Spain = Actor('Spain', 2, -1)
Prussia = Actor('Prussia', 3, -1)

Actors = [England, France, Spain, Prussia]
