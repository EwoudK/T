import cProfile
import numpy as np
import matplotlib.pyplot as plt

from Propensities import Propensities
from Actor import Actors
from System import System, Start
from Loose import config_to_Json

plt.style.use('fivethirtyeight')
kleur = plt.rcParams['axes.prop_cycle'].by_key()['color']


def Simulation(start, actors):
    local_optimum_counter = 0
    filtered = []

    for blank in range(20):
        new = System([0, 0, 0, 0])
        for actor in actors:

            filtered = actor.construct_tree(start, blank)
            actor.decide(start, new)

        new.gain = new.hamiltonian(Propensities)

        if new == start:
            local_optimum_counter += 1
        else:
            local_optimum_counter = 0

        if local_optimum_counter > 3:
            break

        new.parent = start
        start.children = new

        start = new

    child = start
    parent = child.parent
    while parent is not None:
        child = parent
        parent = child.parent
    config_to_Json(child)

    return start, filtered


New, Filtered = Simulation(Start, Actors)

gains = [config.gain for config in Filtered]
summed_gains = [gain.sum() for gain in gains]

gains = np.array(gains)
tmp = gains.flatten()
verzameling = []
for i in range(4):
    verzameling.append(gains[:, i])

bin_max, bin_min = tmp.max(), tmp.min()
bin_range = int(bin_max - bin_min)

fig = plt.figure()
plt.hist(verzameling[0], bins=bin_range)

bin_max, bin_min = max(summed_gains), min(summed_gains)
bin_range = int(bin_max - bin_min)

fig1 = plt.figure()
plt.hist(summed_gains)
plt.show()

print('done')
