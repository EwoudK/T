from Loose import Evolve
from StartingValues import SpinValues, Actors
from System import System
from Tree import Tree

Test = System(Actors, SpinValues, Hamiltonian_to_use='B')
tree_start = Test
Actors[0].tree = Tree(tree_start, Actors[0].name)

TEST = Evolve(Test, Actors[0])

# print(TEST)
Actors[0].tree.print(counter=100)

for child in tree_start.children:
    rf = child.children
    for ch in rf:
        rt = ch.children
        print(child, rt)
# print(tree_start, tree_start.children)
