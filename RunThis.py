import numpy as np
import Tree
import Actor as Actor
import System as System

England = Actor.Actor('England', 0, -1)
Spain = Actor.Actor('Spain', 1, -1)
France = Actor.Actor('France', 2, -1)

Start = System.System([1, 1, 1])

England.make_tree(Start)

choice = England.find_highest_gain()

England.make_choice()

print('done')
