import cProfile
import numpy as np
import matplotlib.pyplot as plt

from Actor import Actors
from System import System, Start
from Loose import write_evolution

plt.style.use('fivethirtyeight')
kleur = plt.rcParams['axes.prop_cycle'].by_key()['color']


def Simulation(start, actors):
    local_optimum_counter = 0
    counter = 0

    while local_optimum_counter < 10:

        new = System(np.zeros(start.Dim))
        for actor in actors:

            actor.construct_tree(start, counter)
            actor.decide(start, new)

        if new == start:
            local_optimum_counter += 1
        else:
            local_optimum_counter = 0

        new.parent = start
        start.children = new

        start = new

        counter += 1

        if counter == 20:
            local_optimum_counter = 11
            print('unstable system')

    print('stable configuration found')
    write_evolution(start)
    return start


# New = Simulation(Start, Actors)
Test = System(np.ones(Start.Dim))
print(Test, Test.gain)
NewTest = Test.invert()
print(NewTest, NewTest.gain)
NewTest = NewTest.flip(0)
print(NewTest, NewTest.gain)
NewTest = NewTest.flip(Actors[0])
print(NewTest, NewTest.gain)
NewTest[0] = 1
print(NewTest, NewTest.gain)
