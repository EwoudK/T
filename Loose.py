import json
import os
import numpy as np
from itertools import product
from numpy.random import default_rng
from numpy import where


def config_to_Json(start, name='config'):

    new_path = r'Data/EvolutionData/'.format(name)
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    with open('Data/EvolutionData/{}.json'.format(name), 'w') as fp:
        json.dump(start, fp=fp, default=lambda x: x.toJson(), sort_keys=True, indent=4)


# noinspection PyTypeChecker
def print_energy_degeneracy(system):

    paths = [r'Data/DegeneracyData/Total/', r'Data/DegeneracyData/Individual/']
    for new_path in paths:
        if not os.path.exists(new_path):
            os.makedirs(new_path)

    Dim = system.Dim
    filtered = []
    for spinvalue_set in product([-1, 1], repeat=Dim):
        copy = system.copy()
        copy[:] = np.array(spinvalue_set)
        filtered.append(copy)

    gains = np.array([config.benefits.sum() for config in filtered])
    np.savetxt('Data/DegeneracyData/Total/gainhist.csv', gains, header='gains', comments='', fmt="%1.1f", delimiter=",")

    for i, actor in enumerate(system.actors):
        individual_gains = np.array([config.benefits[i] for config in filtered])
        actor.max = max(individual_gains)
        np.savetxt('Data/DegeneracyData/Individual/gainhist{}.csv'.format(actor.name), individual_gains,
                   header='gains', comments='', fmt="%1.1f", delimiter=",")

    gain_dict = {}
    for config in filtered:
        gain = config.benefits.sum()

        if gain in gain_dict:
            gain_dict[gain].append(config.spinvalues.tolist())
        else:
            gain_dict[gain] = [config.spinvalues.tolist()]

    with open('Data/DegeneracyData/Total/gainstoconfigs.json', 'w') as fp:
        json.dump(gain_dict, fp=fp, sort_keys=True, indent=4)

    for i, actor in enumerate(system.actors):
        individual_gain_dict = {}
        for config in filtered:
            individual_gain = config.benefits[i]

            if individual_gain in individual_gain_dict:
                individual_gain_dict[individual_gain].append(config.spinvalues.tolist())
            else:
                individual_gain_dict[individual_gain] = [config.spinvalues.tolist()]

        with open('Data/DegeneracyData/Individual/gainstoconfigs{}.json'.format(actor.name), 'w') as fp:
            json.dump(individual_gain_dict, fp=fp, sort_keys=True, indent=4)


def chronological_update(new):

    for index, actor in enumerate(new.actors):
        target = actor.think(index, new)
        actor.decide(target, index, new)


def Evolve(config, extended_actor):

    index = np.where(config.actors == extended_actor)[0]

    flipped, no_change = config.flip(index), config.copy()

    flipped.parent, no_change.parent = config, config
    config.children = np.array([flipped, no_change])

    to_consider = [flipped, no_change]

    for actor_index, actor in enumerate(config.actors):
        if actor_index != index:
            new_to_consider = []

            for config_index, temp in enumerate(to_consider):
                temp_flipped, temp_no_change = temp.flip(actor_index), temp.copy()

                temp_flipped.prob[index], temp_no_change.prob[index] = temp.prob[index], temp.prob[index]
                temp_flipped.parent, temp_no_change.parent = temp, temp

                if temp_flipped.benefits[actor_index] == temp_no_change.benefits[actor_index]:
                    new_to_consider.append(temp_flipped)
                    temp_flipped.prob[index] *= 1/2

                    new_to_consider.append(temp_no_change)
                    temp_no_change.prob[index] *= 1/2

                    temp.children = np.array([temp_flipped, temp_no_change])

                elif temp_flipped.benefits[actor_index] > temp_no_change.benefits[actor_index]:
                    new_to_consider.append(temp_flipped)
                    t = np.array([temp_flipped])
                    temp.children = t

                else:
                    new_to_consider.append(temp_no_change)
                    temp.children = np.array([temp_no_change])

            to_consider[:] = new_to_consider[:]

    considered = np.array(to_consider)
    return considered

    # configs_to_consider = [first_to_consider]
    # new_temp = [first_to_consider]
    #
    # for index, actor in enumerate(first_to_consider.actors):
    #     if actor != extended_actor:
    #         for i, temp_config in enumerate(temp_configs):
    #             flipped, no_change = temp_config.flip(index), temp_config.copy()
    #
    #             if flipped.benefits[index] == no_change.benefits[index]:
    #                 # print('degeneracy encountered')
    #                 new_temp.append(flipped)
    #
    #             elif flipped.benefits[index] > no_change.benefits[index]:
    #                 # print(actor, 'flips it')
    #                 new_temp.pop(i)
    #                 new_temp.append(flipped)
    #
    #         temp_configs[:] = new_temp[:]
    #
    # temp_array = np.array(temp_configs)
    # return temp_array


def Simulation(test, update='chronological'):

    Counter = 0
    Local_optimum = 0
    while 1:

        if Local_optimum > 3:
            print('stable configuration found')
            break

        if Counter > 10:
            print('no stable configuration found')
            break

        new = test.copy()
        test.children = new
        new.parent = test

        if update == 'chronological':
            chronological_update(new)

        for actor in new.actors:
            actor.tree.print(counter=Counter)

        if new == test:
            Local_optimum += 1
        else:
            Local_optimum = 0

        test = new
        Counter += 1


def move_up(config):

    while config.parent is not None:
        config = config.parent
    return config
