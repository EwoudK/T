import numpy as np
from Propensities import Propensities


class System:

    def __init__(self, config):

        if type(config) == list:
            self.config = np.array(config)
        elif type(config) == np.ndarray:
            self.config = config
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
        self.gain = self.hamiltonian(propensities=Propensities)

    def __mul__(self, other):

        temp_config_array = np.copy(self.config)
        temp_config_array *= other

        temp_system = System(temp_config_array)
        return temp_system

    def __rmul__(self, other):

        temp_config_array = np.copy(self.config)
        temp_config_array *= other

        temp_system = System(temp_config_array)
        return temp_system

    def __eq__(self, other):

        return np.array_equal(self.config, other.config)

    def __hash__(self):
        return hash(self.config.tostring())

    def invert(self):

        # temp = np.copy(self.config)
        temp = self*-1

        new_config = temp

        return new_config

    def flip(self, actor):

        temp_config_array = np.copy(self.config)
        temp_system = System(temp_config_array)

        if type(actor) == int:
            temp_system[actor] *= -1

        else:
            temp_system[actor.index] *= -1

        return temp_system

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


Start = System([1, 1, 1])
