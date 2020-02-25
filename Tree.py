import json
import webbrowser
import numpy as np
from System import System
from Actor import Actor

England = Actor('England', 0, -1)
Spain = Actor('Spain', 1, -1)
France = Actor('France', 2, -1)
Actors = [England, Spain, France]


def make_tree_layer(start, actor_to_start, actors=Actors):

    flip = start.flip(actor_to_start)

    choice_nodes = [start, flip]
    temp_config_nodes = np.zeros((2, start.Dim), dtype=object)
    start.children = np.zeros(2 * start.Dim, dtype=object)

    test_index = 0
    for i, choice in enumerate(choice_nodes):
        j = 0

        copy = System(choice.config)
        copy.parent = start

        temp_config_nodes[i][j] = copy
        start.children[test_index] = copy
        test_index += 1

        for other_actor in actors:
            if other_actor != actor_to_start:
                j += 1

                new_config = choice.flip(other_actor)
                new_config.parent = start
                start.children[test_index] = new_config

                test_index += 1

                temp_config_nodes[i][j] = new_config

    temp_config_nodes = temp_config_nodes.flatten()

    return temp_config_nodes


class Tree:

    def __init__(self, start):

        self.start = start
        self.layers = []

    def __repr__(self):

        self.toJson('data')

        webbrowser.open('http://localhost:63342/HolyGuacomolyRecipy/Data/Tree.html?_ijt=nkod4jghvejfq84st6375snk7f')

        return ''

    def toJson(self, name):

        with open('Data/{}.json'.format(name), 'w') as fp:
            json.dump(self.start, fp=fp, default=lambda x: x.toJson(), sort_keys=True, indent=4)
