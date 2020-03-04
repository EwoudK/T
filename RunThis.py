import cProfile
import numpy as np
from Actor import Actor
from System import System
from Loose import config_to_Json

Propensities = np.array([[0, -1, -2, 1], [-1, 0, -3, 1], [-2, -3, 0, 1], [1, 1, 1, 0]])

England = Actor('England', 0, -1)
Spain = Actor('Spain', 1, -1)
France = Actor('France', 2, -1)
Prussia = Actor('Prussia', 3, -1)

actors = [England, Spain, France, Prussia]

Start = System([1, 1, 1, 1])
New = System([1, 1, 1, 1])
for blank in range(6):

    New = System([1, 1, 1, 1])
    for actor in actors:

        actor.construct_tree(Start)
        actor.decide(Start, New)

    New.gain = New.hamiltonian(Propensities)

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
