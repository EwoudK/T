import Tree
import numpy as np
from Loose import Evolve, move_up


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
                print(self, 'immediate max')
                target = flipped
                return target

            elif no_change.benefits[index] == self.max:
                print(self, 'immediate max')
                target = no_change
                return target

            # else:
            #     print(self, 'no immediate max')
            #     configs_seen = []
            #     target = None
            #     while target is None:
            #
            #         if temp.size == 0:
            #
            #             if flipped.benefits[index] > no_change.benefits[index]:
            #                 return flipped
            #
            #             else:
            #                 return no_change
            #
            #         new_children = []
            #         for child in temp:
            #             partial_new_children = []
            #
            #             config_to_consider = child.copy()
            #             new_configs = Extended_Rationality(config_to_consider, self)
            #
            #             for config in new_configs:
            #                 if config.benefits[index] == self.max:
            #                     print('max found')
            #                     print(config)
            #                     target = move_up(config)
            #
            #                 elif config in configs_seen:
            #                     print('already seen')
            #                     config_flipped = config.flip(index)
            #                     config.parent = child
            #
            #                     partial_new_children.append(config)
            #                     partial_new_children.append(config_flipped)
            #                     pass
            #
            #                 else:
            #                     configs_seen.append(config)
            #
            #                     config.parent = child
            #
            #                     new_children.append(config)
            #                     partial_new_children.append(config)
            #
            #                     config_flipped = config.flip(index)
            #                     config_flipped.parent = child
            #
            #                     new_children.append(config_flipped)
            #                     partial_new_children.append(config_flipped)
            #
            #             child.children = np.array(partial_new_children)
            #
            #         new_children_array = np.array(new_children)
            #         temp = new_children_array
            #
            #     return target
            else:
                print(self, 'no immediate max')
                seen = []
                configs_to_consider = [tree_start]

                target = None
                while target is None:
                    new_to_consider = []

                    if len(configs_to_consider) == 0:
                        # TODO
                        # attaining maximal benefit is impossible
                        # return highest immediate benefit
                        target = flipped

                    for config in configs_to_consider:
                        if config not in seen:

                            # returns array of possible new_configs config can transition into
                            children = Evolve(config, self)

                            # check if children contains config with max benefit
                            # add children to [new_to_consider]
                            prob = 0
                            for child_config in children:
                                if child_config.benefits[index] == self.max:
                                    if child_config.prob[index] > prob:
                                        prob = child_config.prob[index]
                                        target = child_config
                                else:
                                    new_to_consider.append(child_config)

                            # finally, put config and config_flipped in [seen]
                            seen.append(config)

                        else:
                            pass

                    configs_to_consider[:] = new_to_consider[:]

                return target

    def decide(self, target, index, new):

        if self.rationality == 0:

            flipped, no_change = target

            if flipped.benefits[index] > no_change.benefits[index]:
                print(self, 'flips')
                new[index] = flipped[index]

            elif flipped.benefits[index] == no_change.benefits[index]:
                chance = np.random.random()
                if chance >= 0.5:
                    print(self, 'random flips')
                    new[index] = flipped[index]
                else:
                    print(self, 'does not random flip')

            else:
                print(self, 'does not flip')

        elif self.rationality == -1:
            print(self, 'chooses coalition represented by: ', target[index])
            new[index] = target[index]
