import json
import numpy as np


def make_tree_layer(start, actor_to_start):
    flip = start.flip(actor_to_start)

    choice_nodes = [start, flip]
    temp_config_nodes = np.zeros((2, start.Dim), dtype=object)
    start.children = np.zeros(2 * start.Dim, dtype=object)

    test_index = 0
    for i, choice in enumerate(choice_nodes):
        j = 0

        copy = choice.copy().invert()
        copy.flip(actor_to_start)
        copy.parent = start

        temp_config_nodes[i][j] = copy
        start.children[test_index] = copy
        test_index += 1

        for actor in start.actors:
            if actor != actor_to_start:
                j += 1

                new_config = choice.flip(actor)
                new_config.parent = start
                start.children[test_index] = new_config

                test_index += 1

                temp_config_nodes[i][j] = new_config

    temp_config_nodes = temp_config_nodes.flatten()

    return temp_config_nodes


def filter_tree(config_set):

    temp = list(config_set)
    filtered = set(temp)
    return filtered


def path_integral(actor, actor_index):

    layer = actor.tree.layers[actor.rationality].flatten()
    row = len(layer)
    if actor.rationality != -1:
        print(actor.rationality)
        col = actor.rationality
    else:
        col = len(actor.tree.layers)

    paths = np.zeros((row, col))

    for j, child in enumerate(layer):

        coeff = np.power(child.Dim, 2)
        index = -1
        j_temp = j // coeff

        parent = child.parent
        while parent is not None:

            paths[j][index] = child.gain[actor_index]

            index -= 1
            j_temp //= coeff

            child = parent
            parent = child.parent
            if parent is None:
                paths[j][index] = child.gain[actor_index]

    PathIntegral_to_csv(col, paths, actor.name)

    max_gain = paths[:, -1].max()
    gain = np.array([x for i, x in enumerate(paths) if paths[:, -1][i] == max_gain])

    max_path = gain.sum(axis=1).max()
    target_index = np.random.choice(np.where(paths.sum(axis=1) == max_path)[0])

    return max_gain, target_index


def PathIntegral_to_csv(col, paths, name):
    string = ''
    for i in range(col+1):
        string += 'config{}, '.format(i)
    string = string[:-2]

    np.savetxt(fname='PathIntegralData/paths{}.csv'.format(name), X=paths, header=string, comments='', fmt="%d", delimiter=",")


def move_up(config, start_config):

    child = config
    parent = child.parent

    while not parent == start_config:
        child = parent
        parent = child.parent

    return child


def config_to_Json(start, name='config'):

    with open('EvolutionData/{}.json'.format(name), 'w') as fp:
        json.dump(start, fp=fp, default=lambda x: x.toJson_part_two(), sort_keys=True, indent=4)


def write_evolution(start):
    child = start
    parent = child.parent
    while parent is not None:
        child = parent
        parent = child.parent
    config_to_Json(child)
