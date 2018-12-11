class FileReader:
    def __init__(self, filename):
        self.file = filename

    def readfile(self):
        with open(self.file) as f:
            return f.readlines()

    def readfile(self, file):
        with open(file) as f:
            return f.readlines()

