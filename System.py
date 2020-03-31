import numpy as np
import json


class System:

    def __init__(self, config, actors):

        if type(config) == list:
            self.config = np.array(config)
        elif type(config) == np.ndarray:
            self.config = config

        self.Dim = self.config.size
        self.actors = actors

        self.parent = None
        self.children = None

        self.gain = self.hamiltonian()

    def __repr__(self):

        temp = str(self.config)
        return temp

    def __getitem__(self, key):

        return self.config[key]

    def __setitem__(self, key, value):

        self.config[key] = value
        self.gain = self.hamiltonian()

    def __mul__(self, other):

        temp_config_array = np.copy(self.config)
        temp_config_array *= other

        temp_system = System(temp_config_array, self.actors)
        return temp_system

    def __rmul__(self, other):

        temp_config_array = np.copy(self.config)
        temp_config_array *= other

        temp_system = System(temp_config_array, self.actors)
        return temp_system

    def __eq__(self, other):

        return np.array_equal(self.config, other.config)

    def __hash__(self):
        return hash(self.config.tostring())

    def copy(self):
        temp_config = np.copy(self.config)
        temp = System(temp_config, self.actors)
        return temp

    def invert(self):

        temp = self*-1

        new_config = temp

        return new_config

    def flip(self, actor):

        temp_config_array = np.copy(self.config)
        temp_system = System(temp_config_array, self.actors)
        index = self.actors.index(actor)

        temp_system[index] *= -1

        return temp_system

    def hamiltonian(self):

        h = np.zeros(self.Dim)
        for i, actor in enumerate(self.actors):
            temp = 0
            for j, other in enumerate(self.actors):
                temp += 0.5*(self[i]*self[j]*(actor.propensities[j] + actor.belonging*other.belonging*10))
                h[i] = temp

        return h

    def toJson(self):
        if self.children is None:
            return {
                'config': self.config.tolist(),
                'gain': self.gain.tolist()
                    }
        else:
            return {
                'children': [child.toJson() for child in self.children],
                'config': self.config.tolist(),
                'gain': self.gain.tolist()
            }

    def toJson_part_two(self):

        if self.children is None:
            return {
                'config': self.config.tolist(),
                'gain': self.gain.tolist()
                    }
        else:

            return {
                'children': [self.children.toJson_part_two()],
                'config': self.config.tolist(),
                'gain': self.gain.tolist()
            }

    # noinspection PyTypeChecker
    def print_energy_degeneracy(self):

        filtered = self.actors[0].tree.filtered

        gains = np.array([config.gain.sum() for config in filtered])
        np.savetxt('DegeneracyData/Total/gainhist.csv', gains, header='gains', comments='', fmt="%d", delimiter=",")

        for i, actor in self.actors:
            individual_gains = np.array([config.gain[i] for config in filtered])
            np.savetxt('DegeneracyData/Individual/gainhist{}.csv'.format(actor.name), individual_gains, header='gains',
                       comments='', fmt="%d", delimiter=",")

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
        for i, actor in self.actors:
            for config in filtered:
                individual_gain = config.gain[i]

                if individual_gain in individual_gain_dict:
                    individual_gain_dict[individual_gain].append(config.config.tolist())
                else:
                    individual_gain_dict[individual_gain] = [config.config.tolist()]

            with open('DegeneracyData/Individual/gainstoconfigs{}.json'.format(actor.name), 'w') as fp:
                json.dump(individual_gain_dict, fp=fp, sort_keys=True, indent=4)

