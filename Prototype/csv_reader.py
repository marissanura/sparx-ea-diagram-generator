from abc import abstractmethod
import csv
import errno
from os import strerror

class CSVReader():
    def __init__(self, file):
        self.file = file
        self.get_file()

    def get_file(self):
        try:
            with open(self.file, mode="r", encoding="utf-8-sig") as f:
                self.reader = [row for row in csv.reader(f, delimiter = ";")]
                return self.reader
        except IOError as err:
            print("I/O error({0}): {1}".format(errno, strerror))
        return

    @abstractmethod
    def generate_tree(self):
        pass