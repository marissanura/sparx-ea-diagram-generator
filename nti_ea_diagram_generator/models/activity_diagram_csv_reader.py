from xml.etree.ElementTree import ( Element, SubElement )
from odoo.exceptions import ValidationError
import uuid
import re

from .csv_reader import CSVReader

class ADCSVReader(CSVReader):

    def generate_tree(self, folder_hierarchy):
        global num_of_fh, num_of_line, list_of_node, fh
        
        fh = folder_hierarchy
        num_of_fh = len(fh)
        num_of_line = len(self.reader) - 1
        self.root = Element('ActivityDiagram')

        list_of_node = [self.root]
        self.generate_use_case(0,1)

        return self.root
    
    def generate_use_case(self, fol_hierarchy, lines):
        try:                
            if re.match(fh[fol_hierarchy], self.reader[lines][0]):

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
            raise ValidationError(("There's mismatch regex in UC ID at line " + str(lines)))
    
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