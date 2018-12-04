class FileReader:
    def __init__(self, fileName):
        self.file = fileName

    def ReadFile(self):
        with open(self.file) as f:
            return f.readlines()

    def Readfile(self, file):
        with open(file) as f:
            return f.readlines()

