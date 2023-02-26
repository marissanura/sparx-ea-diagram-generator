from xml_writer import XMLWriter
from xml.etree import ElementTree

class SparxEAXMLWriter(XMLWriter):

    def csv_tree_to_xml(self):
        self.init_template()
    
    def init_template(self):
        ElementTree.register_namespace('xmi', "http://schema.omg.org/spec/XMI/2.1")
        ElementTree.register_namespace('uml', "http://schema.omg.org/spec/UML/2.1")
        ElementTree.register_namespace('thecustomprofile', "http://www.sparxsystems.com/profiles/thecustomprofile/1.0")
        tree = ElementTree.parse('template.xml')
        self.xml_tree = tree.getroot()

        for listing in self.xml_tree.findall("listing"):
            self.model = listing.find('uml:Model')
            self.elements = listing.find('elements')
            self.connectors = listing.find('connectors')
            self.diagrams = listing.find('diagrams')
    
    # override
    def tostring(self):
        return ElementTree.tostring(self.xml_tree, encoding='unicode', method='xml')
    
    def write(self, filename):
        tree = ElementTree.ElementTree(self.xml_tree)
        tree.write(filename)