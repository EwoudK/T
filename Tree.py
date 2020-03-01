import json


class Tree:

    def __init__(self, start):

        self.start = start
        self.layers = []

    def __repr__(self, plot=False):

        self.toJson('data')

        return ''

    def toJson(self, name):

        with open('TreeData/{}.json'.format(name), 'w') as fp:
            json.dump(self.start, fp=fp, default=lambda x: x.toJson(), sort_keys=True, indent=4)
