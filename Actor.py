import Tree
import numpy as np
from Loose import chronological_update_E, move_up


class Actor:

    def __init__(self, name, rationality, belonging, propensities, gpropensities):

        self.name = name

        self.rationality = rationality

        self.belonging = belonging
        self.propensities = propensities
        self.gpropensities = gpropensities

        self.tree = None
        self.max = 0

    def __repr__(self):

        return self.name

    def think(self, index, start):

        tree_start = start.copy()
        self.tree = Tree.Tree(tree_start, self.name)

        flipped = tree_start.flip(index)
        no_change = tree_start.copy()

        temp = np.array([flipped, no_change])

        tree_start.children = temp
        flipped.parent = tree_start
        no_change.parent = tree_start

        if self.rationality == 0:
            return temp

        elif self.rationality == -1:

            if flipped.benefits[index] == self.max:
                print('immediate max')
                target = flipped
                return target

            elif no_change.benefits[index] == self.max:
                print('immediate max')
                target = no_change
                return target

            else:
                print('no immediate max')
                target = None
                while target is None:
                    new_children = []
                    for child in temp:
                        config_to_consider = child.copy()
                        new_configs = chronological_update_E(config_to_consider, self)

                        child.children = new_configs
                        for config in new_configs:
                            config.parent = child
                            if config.benefits[index] > self.max:
                                # == self.max:
                                target = move_up(config)
                            else:
                                new_children.append(config)

                    new_children_array = np.array(new_children)

                    # if we do not do this check, an endless loop can form of a configuration that evolves into itself
                    # thus no maximal benefit is found
                    if (new_children_array == temp).all():
                        if flipped.benefits[index] > no_change.benefits[index]:
                            return flipped
                        else:
                            return no_change

                    else:
                        temp = new_children_array

                return target

    def decide(self, target, index, new):

        if self.rationality == 0:

            flipped, no_change = target

            if flipped.benefits[index] > no_change.benefits[index]:
                new[index] = flipped[index]

            elif flipped.benefits[index] == no_change.benefits[index]:
                chance = np.random.random()
                if chance >= 0.5:
                    new[index] = flipped[index]

        elif self.rationality == -1:
            new[index] = target[index]
