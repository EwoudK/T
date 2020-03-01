import cProfile
from Actor import Actor, path_integral
import System as System

England = Actor('England', 0, -1)
Spain = Actor('Spain', 1, -1)
France = Actor('France', 2, -1)
Spain1 = Actor('Spain', 1, -1)
France1 = Actor('France', 2, -1)

Start = System.System([1, 1, 1, 1])

England.construct_tree(Start)
print(England.tree)

gain = path_integral(England)

print('done')
