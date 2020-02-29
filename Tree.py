import json
import webbrowser


class Tree:

    def __init__(self, start):

        self.start = start
        self.layers = []

    def __repr__(self):

        self.toJson('data')

        webbrowser.open('http://localhost:63342/HolyGuacomolyRecipy/Data/Tree.html?_ijt=bjorkm50chacd96tsgdjve15uu')

        return ''

    def toJson(self, name):

        with open('Data/{}.json'.format(name), 'w') as fp:
            json.dump(self.start, fp=fp, default=lambda x: x.toJson(), sort_keys=True, indent=4)
