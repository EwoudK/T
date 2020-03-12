import cProfile
import numpy as np
from Actor import Actor
from System import System
from Loose import config_to_Json
import matplotlib.pyplot as plt

Propensities = np.array([[0, 1, 2, 1], [1, 0, 3, 1], [2, 3, 0, 1], [1, 1, 1, 0]])

England = Actor('England', 0, -1)
France = Actor('France', 1, -1)
Spain = Actor('Spain', 2, -1)
Prussia = Actor('Prussia', 3, -1)

Actors = [England, France, Spain, Prussia]

Start = System([-1, 1, -1, 1])


def unstable(start, actors):
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


New, Filtered = unstable(Start, Actors)

gains = [config.gain for config in Filtered]
summed_gains = [gain.sum() for gain in gains]

gains = np.array(gains)
gains = gains.flatten()

bin_max, bin_min = gains.max(), gains.min()
bin_range = int(bin_max - bin_min)

plt.hist(gains, bins=bin_range)
plt.show()

print('done')
