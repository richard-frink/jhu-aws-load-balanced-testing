from testingapp.testing.DataAccess import FileReader


class SystemConfiguration:
    def getalgos(self):
        lines = self.filereader.readfile()
        algos = []
        for line in lines:
            algos.append(line.split(" "))
        return algos

    def __init__(self, filename):
        self.filereader = FileReader(filename)
        self.sortingalgos = self.getalgos()
