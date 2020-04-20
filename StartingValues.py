import numpy as np
from System import System
from Actor import Actor

One = Actor('USA', 0,     [0, 1, 1], belonging=1)
Two = Actor('UK', 0,      [1, 0, 1], belonging=-1)
Three = Actor('France', 0, [1, 1, 0], belonging=-1)

Actors = [One, Two, Three]

Start = System(np.ones(len(Actors)), Actors)
