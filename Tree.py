import json
import os


class Tree:

    def __init__(self, start, name):

        self.name = name

        self.start = start
        self.layers = []

        self.filtered = []

    def print(self, counter):

        self.toJson(self.name, counter)

    def toJson(self, name, counter):

        new_path = r'Data/TreeData/{}/'.format(name)
        if not os.path.exists(new_path):
            os.makedirs(new_path)

        with open('Data/TreeData/{}/Tree{}.json'.format(name, counter), 'w') as fp:
            json.dump(self.start, fp=fp, default=lambda x: x.toJson(tree=True), sort_keys=True, indent=4)