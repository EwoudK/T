import json
import numpy as np
from Actor import Actor

temp_array = []
with open('StartValues-5.json') as f:
    data = json.load(f)

NAMES = data['Actors'].keys()
for NAME in NAMES:
    RAT, BEL, PROP, GPROP = data['Actors'][NAME].values()

    if type(BEL) is list:
        BEL = np.array(BEL)
        GPROP = np.array(GPROP)

    temp_actor = Actor(NAME, RAT, BEL, PROP, GPROP)
    temp_array.append(temp_actor)

Actors = np.array(temp_array)
SpinValues = np.ones(len(Actors))
