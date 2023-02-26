from xml.dom import minidom
from xml.etree import ElementTree
from csv_reader import CSVReader
from xml.etree.ElementTree import ( Element, SubElement )
import re


class CSVReader(CSVReader):
    fh = ["SS-[0-9]{1,}\Z","UC-[0-9]{1,}\Z","\A\Z","UC-[0-9]{1,}-[0-9]{1,}\Z"]

    def generate_tree(self):
        self.num_of_fh = len(self.fh)
        self.num_of_line = len(self.reader) - 1
        self.root = Element('UseCaseDiagram')

        self.list_of_node = []
        self.list_of_node.append(self.root)
        self.generate_use_case(0,1)

        xmlstr = minidom.parseString(ElementTree.tostring(self.root)).toprettyxml(indent="   ") 
        with open("xml_tree.xml", "w") as f:
            f.write(xmlstr)

        return self.root
    
    def generate_use_case(self, fol_hierarchy, lines):
        if re.match(self.fh[fol_hierarchy], self.reader[lines][0]):
            temp_node = self.add_element(self.list_of_node[fol_hierarchy], self.reader[lines])
            if (fol_hierarchy != (self.num_of_fh - 1)): self.add_line_of_node(temp_node, fol_hierarchy) 
            if lines < self.num_of_line:
                lines = lines + 1
                self.generate_use_case(fol_hierarchy, lines)
            else:
                return True
        else:
            fol_hierarchy = 0 if (fol_hierarchy == (self.num_of_fh - 1)) else (fol_hierarchy + 1)
            self.generate_use_case(fol_hierarchy, lines)
    
    def add_element(self, parent, data):
        temp = Element(data[0] if (data[0] != '') else (data[1].replace(" ", "")))
        temp.set('name', data[1])
        temp.set('actor', data[2])
        temp.set('ket', data[3])

        parent.append(temp)

        return temp
    
    def add_line_of_node(self, temp_node, fol_hierarchy):
        if ((len(self.list_of_node)-1) > fol_hierarchy):
            self.list_of_node[fol_hierarchy + 1] = temp_node
        else: (self.list_of_node.append(temp_node))