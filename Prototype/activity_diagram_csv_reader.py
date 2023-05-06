from xml.dom import minidom
from xml.etree import ElementTree as ET
from csv_reader import CSVReader
import uuid

class ADCSVReader(CSVReader):

    def __init__(self, file):
        super().__init__(file)

    def generate_tree(self):
        global actors

        self.root = ET.Element("ActivityDiagram")
        self.root.set('name', self.reader[0][0])

        actors = self.reader[1]
        self.root.set('lanes', ', '.join(actors)) 

        self.generate_activity_diagram(2)

        xmlstr = minidom.parseString(ET.tostring(self.root)).toprettyxml(indent="   ") 
        with open("ad_xml_tree.xml", "w") as f:
            f.write(xmlstr)

        return self.root
    
    def generate_activity_diagram(self, lines):
        line = self.reader[lines]
        print(line)
        if 'end' in self.reader[lines]:
           self.add_element('end', self.get_lane(line), lines)
           return True
        elif('start' in self.reader[lines]):
           self.add_element('start', self.get_lane(line), lines)
           self.generate_activity_diagram(lines+1)
        else:
            lane = self.get_lane(line)
            self.add_element(line[lane], lane, lines)
            self.generate_activity_diagram(lines+1)
    
    def add_element(self, name, lane, lines):
        temp = ET.Element("lane" + str(lane))
        temp.set('id', str(lines))
        temp.set('name', name)
        temp.set('lane', str(lane))

        self.root.append(temp)

        return temp
    
    def get_lane(self, lines):
        index = 0

        while (lines[index] == ''):
            index += 1

        print(index)
        return index