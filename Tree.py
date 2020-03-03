import json


class Tree:

    def __init__(self, start, name):

        self.name = name

        self.start = start
        self.layers = []

    def __repr__(self):

        self.toJson(self.name)

        return ''

    def toJson(self, name):

        with open('TreeData/{}.json'.format(name), 'w') as fp:
            json.dump(self.start, fp=fp, default=lambda x: x.toJson(), sort_keys=True, indent=4)
