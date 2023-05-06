from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import ( Element, SubElement )
from odoo.exceptions import ValidationError
import uuid
import re

from .csv_reader import CSVReader

class ADCSVReader(CSVReader):

    def __init__(self, file):
        super().__init__(file)

    def generate_tree(self):
        global actors

        self.root = Element(self.reader[0][0])
        actors = self.reader[1]
        self.root.set('lanes', ', '.join(actors)) 

        self.generate_activity_diagram(2)

        return self.root
    
    def generate_activity_diagram(self, lines):
        if 'end' in self.reader[lines]:
           self.add_element('end', 'end', self.get_lane(self.reader[lines]))
           return True
        elif('start' in self.reader[lines]):
           self.add_element('start', 'start', self.get_lane(self.reader[lines]))
        else:
            lane = self.get_lane(self.reader[lines])
            self.add_element('activity', self.reader[lines][lane], lane)
    
    def add_element(self, element, name, lane):
        temp = Element(element)
        temp.set('name', name)
        temp.set('lane', lane)

        self.root.append(temp)

        return temp
    
    def get_lane(lines):
        index = 0

        while (lines[index] == ''):
            index += 1

        return index