from abc import abstractmethod
from xml.etree import ElementTree

class XMLWriter():

    def __init__(self, tree):
        self.tree = tree
    
    @abstractmethod
    def csv_tree_to_xml(self):
        pass

    def tostring(self):
        return ElementTree.tostring(self.tree, encoding='unicode', method='xml')