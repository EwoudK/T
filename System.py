import numpy as np
from itertools import permutations


class System:

    def __init__(self, actors, spinvalues, Hamiltonian_to_use='B', prob=None, M=None, prefactor=1):

        self.actors = actors
        self.spinvalues = spinvalues
        self.Dim = self.actors.size
        self.H = Hamiltonian_to_use
        self.prefactor = prefactor

        if prob is None:
            self.prob = np.ones(self.Dim)
        else:
            self.prob = prob

        if M is None:
            self.M = np.zeros(self.Dim)
        else:
            self.M = M

        self.benefits = self.Hamiltonian()

        self.parent = None
        self.children = None

    def __repr__(self):

        temp = str(self.spinvalues)
        return temp

    def __getitem__(self, key):

        return self.spinvalues[key]

    def __setitem__(self, key, value):

        self.spinvalues[key] = value
        self.benefits = self.Hamiltonian()

    def __eq__(self, other):

        return np.array_equal(self.spinvalues, other.spinvalues)

    def Hamiltonian(self):

        H = np.zeros(self.Dim)
        indices = [x for x in range(0, self.Dim)]
        for index1, index2 in permutations(indices, 2):

            actor1 = self.actors[index1]
            actor2 = self.actors[index2]

            spin1 = self.spinvalues[index1]
            spin2 = self.spinvalues[index2]

            propensity = actor1.propensities[index2]

            if self.H == 'B':

                H[index1] += 0.5*(spin1*spin2)*propensity

            elif self.H == 'G':

                gpropensity = self.prefactor*actor1.gpropensities[index2]
                H[index1] += 0.5*(spin1*spin2)*(propensity + actor1.belonging*actor2.belonging*gpropensity)

            elif self.H == 'V':
                gpropensities = actor1.gpropensities[:, index2]
                gbenefit = self.prefactor*np.einsum('i,i,i->', actor1.belonging, actor2.belonging, gpropensities)
                H[index1] += 0.5*(spin1*spin2)*(propensity + gbenefit)

        H += np.einsum('i,i->i', self.spinvalues, self.M)
        return H

    def copy(self):

        temp_spins = np.copy(self.spinvalues)
        temp_prob = np.copy(self.prob)
        temp_M = np.copy(self.M)
        temp_prefactor = self.prefactor

        new = System(self.actors, temp_spins, self.H, temp_prob, temp_M, temp_prefactor)
        return new

    def flip(self, index):

        temp_spins = np.copy(self.spinvalues)
        temp_prob = np.copy(self.prob)
        temp_M = np.copy(self.M)
        temp_prefactor = self.prefactor

        temp_spins[index] *= -1
        new = System(self.actors, temp_spins, self.H, temp_prob, temp_M, temp_prefactor)
        return new

    def diplomacy(self, index, strength):

        self.M[index] += strength
        self.benefits = self.Hamiltonian()

    def toJson(self, tree=False):
        if self.children is None:
            return {
                'config': self.spinvalues.tolist(),
                'gain': self.benefits.tolist()
                    }
        elif tree:
            return {
                'children': [child.toJson(tree=True) for child in self.children],
                'config': self.spinvalues.tolist(),
                'gain': self.benefits.tolist()
            }

        else:
            return {
                'children': [self.children.toJson()],
                'config': self.spinvalues.tolist(),
                'gain': self.benefits.tolist()
            }
