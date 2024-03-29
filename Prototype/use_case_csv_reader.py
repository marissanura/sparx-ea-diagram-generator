from xml.dom import minidom
from xml.etree import ElementTree
from csv_reader import CSVReader
from xml.etree.ElementTree import ( Element, SubElement )
import uuid
import re

class UCCSVReader(CSVReader):

    def generate_tree(self, folder_hierarchy):
        global num_of_fh, num_of_line, list_of_node, fh
        
        fh = folder_hierarchy
        print(fh)
        num_of_fh = len(fh)
        num_of_line = len(self.reader) - 1
        self.root = Element('UseCaseDiagram')

        list_of_node = [self.root]
        self.generate_use_case(0,1)

        xmlstr = minidom.parseString(ElementTree.tostring(self.root)).toprettyxml(indent="   ") 
        with open("xml_tree.xml", "w") as f:
            f.write(xmlstr)

        return self.root
    
    def generate_use_case(self, fol_hierarchy, lines):
        try:
            if re.match(fh[fol_hierarchy], self.reader[lines][0]):
                print(fol_hierarchy)
                print(lines)
                print(len(list_of_node))
                print()
                temp_node = self.add_element(list_of_node[fol_hierarchy], self.reader[lines])
                if (fol_hierarchy != (num_of_fh - 1)): self.add_line_of_node(temp_node, fol_hierarchy) 
                if lines < num_of_line:
                    lines = lines + 1
                    self.generate_use_case(fol_hierarchy, lines)
                else:
                    return True
            else:
                fol_hierarchy = 0 if (fol_hierarchy == (num_of_fh - 1)) else (fol_hierarchy + 1)
                self.generate_use_case(fol_hierarchy, lines)
        except RecursionError:
            print("There's mismatch regex in UC ID")
    
    def add_element(self, parent, data):
        temp = Element(data[0] if (data[0] != '') else (data[1].replace(" ", "")))
        temp.set('id', str(uuid.uuid4()))
        temp.set('name', data[1])
        temp.set('actor', data[2])
        temp.set('ket', data[3])

        parent.append(temp)

        return temp
    
    def add_line_of_node(self, temp_node, fol_hierarchy):
        if ((len(list_of_node)-1) > fol_hierarchy):
            list_of_node[fol_hierarchy + 1] = temp_node
        else: (list_of_node.append(temp_node))