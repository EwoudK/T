import numpy as np
import Tree
import Actor as Actor
import System as System

England = Actor.Actor('England', 0, -1)
Spain = Actor.Actor('Spain', 1, -1)
France = Actor.Actor('France', 2, -1)
Prussia = Actor.Actor('Prussia', 3, -1)

Start = System.System(np.zeros(4).tolist())

England.make_tree(Start)

print(England.tree)

print('done')
