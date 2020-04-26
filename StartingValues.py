import json
import numpy as np
from Actor import Actor
from Loose import sort

temp_array = []
with open('StartValues-4.json') as f:
    data = json.load(f)

NAMES = data['Actors'].keys()
for NAME in NAMES:
    RAT, BEL, PROP, GPROP = data['Actors'][NAME].values()

    if type(BEL) is list:
        BEL = np.array(BEL)
        GPROP = np.array(GPROP)

    temp_actor = Actor(NAME, RAT, BEL, PROP, GPROP)
    temp_array.append(temp_actor)

temp_array.sort(key=sort, reverse=True)
Actors = np.array(temp_array)
SpinValues = np.ones(len(Actors))
