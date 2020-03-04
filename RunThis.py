import cProfile
import numpy as np
from Actor import Actor
from System import System
from Loose import config_to_Json

Propensities = np.array([[0, 1, 2, 1], [1, 0, 3, 1], [2, 3, 0, 1], [1, 1, 1, 0]])

England = Actor('England', 0, -1)
France = Actor('France', 1, -1)
Spain = Actor('Spain', 2, -1)
Prussia = Actor('Prussia', 3, -1)

actors = [England, France, Spain, Prussia]

Start = System([-1, 1, -1, 1])
New = System([1, 1, 1, 1])
local_optimum_counter = 0
for blank in range(10):

    New = System([1, 1, 1, 1])
    for actor in actors:

        actor.construct_tree(Start, blank)
        actor.decide(Start, New)

    New.gain = New.hamiltonian(Propensities)

    if New == Start:
        local_optimum_counter += 1

    if New == Start and local_optimum_counter > 1:
        randie = np.random.choice(actors)
        New = New.flip(randie)
        local_optimum_counter = 0
        print('forced flip')

    New.parent = Start
    Start.children = New

    Start = New

child = New
parent = child.parent
while parent is not None:
    child = parent
    parent = child.parent

config_to_Json(child)

print('done')
