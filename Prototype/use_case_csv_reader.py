from csv_reader import CSVReader
from xml.etree.ElementTree import ( Element, SubElement )
import re


class CSVReader(CSVReader):
    folder_hirarchy = ["SS-[0-9]{1,}","UC-[0-9]{1,}","\A\Z","UC-[0-9]{1,}-[0-9]{1,}"]

    def generate_tree(self):
        print(self.reader[1][0])
        self.root = Element('Application Use Case Diagram')
        
        self.generate_catalog_actor()
        self.generate_use_case()

        return self.root
    
    def generate_catalog_actor(self):
        actor = SubElement(self.root, 'Actor')
    
    def generate_use_case(self):
        use_case = SubElement(self.root, 'Use Case')
            