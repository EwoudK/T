import numpy as np
import json

Propensities = np.array([[0, -1, -2, 1], [-1, 0, -3, 1], [-2, -3, 0, 1], [1, 1, 1, 0]])


class System:

    def __init__(self, config):

        self.config = np.array(config)
        self.Dim = self.config.size

        self.parent = None
        self.children = None

        self.gain = self.hamiltonian(propensities=Propensities)

    def __repr__(self):

        temp = str(self.config)
        return temp

    def __getitem__(self, key):

        return self.config[key]

    def __setitem__(self, key, value):

        self.config[key] = value

    def __mul__(self, other):

        temp = np.copy(self.config)
        temp *= other
        return System(temp)

    def __rmul__(self, other):

        temp = np.copy(self.config)
        temp *= other
        return System(temp)

    def __eq__(self, other):

        return np.array_equal(self.config, other.config)

    def __hash__(self):
        return hash(self.config.tostring())

    def invert(self):

        temp = np.copy(self.config)
        temp *= -1

        new_config = System(temp)

        return new_config

    def flip(self, actor):

        temp = np.copy(self.config)

        if type(actor) == int:
            temp[actor] *= -1

        else:
            temp[actor.index] *= -1

        new_config = System(temp)

        return new_config

    def hamiltonian(self, propensities):

        h = np.zeros(self.Dim)

        transpose = self.config.reshape((-1, 1))
        for i in range(self.Dim):
            temp = np.zeros(self.Dim)
            temp[i] = self[i]
            h[i] = temp.dot(propensities).dot(transpose)[0]

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


def config_to_Json(start, name='config'):

    with open('EvolutionData/{}.json'.format(name), 'w') as fp:
        json.dump(start, fp=fp, default=lambda x: x.toJson_part_two(), sort_keys=True, indent=4)
