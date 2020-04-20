import numpy as np
from System import System
from Actor import Actor

One = Actor('USA', -1,     [0, 1, 1, 1, -1], belonging=-1)
Two = Actor('UK', -1,      [1, 0, 1, 1, -1], belonging=-1)
Three = Actor('France', -1, [1, 1, 0, -1, -1], belonging=-1)
Four = Actor('DDR', -1,    [1, 1, -1, 0, -1], belonging=1)
Five = Actor('USSR', -1,    [-1, -1, -1, -1, 0], belonging=1)

Actors = [One, Two, Three]

Start = System(np.ones(len(Actors)), Actors)
