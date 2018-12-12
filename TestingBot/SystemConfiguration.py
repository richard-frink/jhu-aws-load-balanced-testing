import TestingBot.FileReader as fr

class SystemConfiguration:
    def getalgos(self):
        lines = self.filereader.readfile()
        algos = []
        for line in lines:
            algos.append(line.split(" "))
        return algos

    def __init__(self, filename):
        self.filereader = fr(filename)
        self.sortingalgos = self.getalgos()
