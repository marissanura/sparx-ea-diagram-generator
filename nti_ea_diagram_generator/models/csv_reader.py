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
        
        print(self.reader)
    # def get_file(self):
    #     try:
    #         self.reader = [row for row in csv.reader(self.file, delimiter = ";")]
    #         return self.reader
    #     except IOError as err:
    #         print("I/O error({0})".format(err))
    #     return

    @abstractmethod
    def generate_tree(self):
        pass