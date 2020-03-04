import json


class Tree:

    def __init__(self, start, name):

        self.name = name

        self.start = start
        self.layers = []

    # def __repr__(self, counter=1):
    #
    #     self.toJson(self.name, counter)
    #
    #     return ''

    def print(self, counter):

        self.toJson(self.name, counter)

    def toJson(self, name, counter):

        with open('TreeData/{}/Tree{}.json'.format(name, counter), 'w') as fp:
            json.dump(self.start, fp=fp, default=lambda x: x.toJson(), sort_keys=True, indent=4)
