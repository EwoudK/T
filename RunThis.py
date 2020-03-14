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

    for blank in range(20):
        new = System([0, 0, 0, 0])
        for actor in actors:

            actor.construct_tree(start, blank)
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

    return start


New = Simulation(Start, Actors)

print('done')
