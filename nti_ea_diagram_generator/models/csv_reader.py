from abc import abstractmethod
import base64
from odoo.exceptions import ValidationError

class CSVReader(object):
    def __init__(self, file: bytes):
        temp = base64.b64decode(file)
        lines = temp.decode('utf-8-sig').splitlines()
        self.reader = []
        for line in lines:
            res = line.split(";")
            self.reader.append(res)
        
        print(self.reader)
        print(len(self.reader))
        
        if len(self.reader) <= 1: raise ValidationError(("The file is only containing 1 line, indicating the file is empty."))

    @abstractmethod
    def generate_tree(self):
        pass