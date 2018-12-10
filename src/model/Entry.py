


class Entry(object):

    def __init__(self, _data):
        print("This is a base entry object")
        self.data = {}
        self.data = _data

    def printEntry(self):
        print("Printing data...")
        for e in self.data.keys():
            print(e, ' : ', self.data[e])

    