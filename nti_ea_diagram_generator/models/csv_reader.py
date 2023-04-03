from abc import abstractmethod
import base64
import csv

class CSVReader():
    def __init__(self, file):
        temp = base64.b64decode(file)
        lines = temp.decode('utf-8-sig').splitlines()
        self.reader = []
        for line in lines:
            res = line.split(";")
            self.reader.append(res)

    @abstractmethod
    def generate_tree(self):
        pass