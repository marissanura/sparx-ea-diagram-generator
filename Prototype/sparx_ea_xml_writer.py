from xml.dom import minidom
from xml_writer import XMLWriter
from xml.etree import ElementTree
from xml.etree.ElementTree import (Element, SubElement)

class SparxEAXMLWriter(XMLWriter):

    def csv_tree_to_xml(self):
        self.init_template()
        print(self.tree)
        for elem in self.tree.iter():
            print(elem.tag, elem.attrib.get('name'))
    
    def init_template(self):
        ElementTree.register_namespace('xmi', "http://schema.omg.org/spec/XMI/2.1")
        ElementTree.register_namespace('uml', "http://schema.omg.org/spec/UML/2.1")
        ElementTree.register_namespace('thecustomprofile', "http://www.sparxsystems.com/profiles/thecustomprofile/1.0")
        tree = ElementTree.parse('template.xml')
        self.xml_tree = tree.getroot()

        global model, elements, connectors, diagrams
        
        model = self.xml_tree[1]
        elements = self.xml_tree[2][0]
        connectors = self.xml_tree[2][1]
        diagrams = self.xml_tree[2][2]
    
    # override
    def tostring(self):
        return ElementTree.tostring(self.xml_tree, encoding='unicode', method='xml')
    
    def write(self, filename):
        xmlstr = minidom.parseString(ElementTree.tostring(self.xml_tree)).toprettyxml(indent="   ") 
        with open(filename, "w") as f:
            f.write(xmlstr)
    
    def add_package(self, parent, data):
        package = self.add_packaged_element(parent, {"xmi:type":"uml:Package", "xmi:id":data.id, "name":data.name})
        return package
    
    def add_boundary(self, parent, parent_ucd, data):
        self.add_subelement(parent, 'packagedElement', {"xmi:type":"uml:Class", "xmi:id":data.id, "name":data.name})
        self.add_subelement(elements, 'element', {"xmi:idref":data.id, "xmi:type":"uml:Boundary", "name":data.name})
        self.add_subelement(parent_ucd, 'element', {"geometry":"Left=132;Top=24;Right=419;Bottom=590;", "subject":data.id})
    
    def add_use_case(self, parent, parent_ucd, data):
        self.add_packaged_element(parent, data)
        
    
    def add_element_tag(self, data_package, data):
        element = self.add_element(elements, 'element', {"xmi:idref":data.id, "xmi:type":("uml:" + data.type), "name": data.name})

        self.add_subelement(element, 'model', {"package":data_package})
        self.add_subelement(element, 'properties', {"sType":data.type})

    def add_packaged_element(self, parent, data):
        packagedElement = self.add_subelement(parent, 'packagedElement', data)
        return packagedElement
    
    def add_connectors(self, id_connector, start, end):
        connector = self.add_element('connector', {"xmi:idref":id_connector})

        source = self.add_subelement(connector, 'source', {"xmi:idref":start.id})
        self.add_subelement(source, 'model', {"type": start.type, "name": start.name})
        target = self.add_subelement(connector, 'target', {"xmi:idref":end.id})
        self.add_subelement(target, 'model', {"type": end.type, "name": end.name})

        connectors.append(connector)
    
    def add_element(self, tag_name, val_set):
        element = Element(tag_name)
        for val in val_set: element.set(val, val_set.get(val))

        return element
    
    def add_subelement(self, element, tag_name, val_set):
        subelement = SubElement(element, tag_name)
        for val in val_set: subelement.set(val, val_set.get(val))

        return subelement