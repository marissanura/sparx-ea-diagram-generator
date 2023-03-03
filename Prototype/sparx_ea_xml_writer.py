from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import (Element, SubElement)
from xml_writer import XMLWriter

class SparxEAXMLWriter(XMLWriter):
    actor = {"Administrator":"ADM", "User":"USR", "Creator":"CRE", "Reviewer":"REV", "Viewer":"VIE", "Approver":"APP"}

    def csv_tree_to_xml(self):
        self.init_template()
        root_package = self.add_packaged_element(model, {"xmi:type":"uml:Package", "xmi:id":"root", "name":self.tree.tag})
        if len(list(self.tree)) > 0: self.tree_traverse(root_package, self.tree, self.tree[0], 0)

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

    def tree_traverse(self, parent_package, parent, node, index):
        print(parent, node.attrib.get('name'), index)
        curr_package = self.add_package(parent_package, {"id":node.attrib.get('id'), "name":node.attrib.get('name')})
        self.add_folder_element(curr_package, node)

        if len(list(node)) > 0: self.tree_traverse(curr_package, node, node[0], 0)
        if len(list(parent)) - 1 > index: self.tree_traverse(parent_package, parent, parent[index + 1], index+1)
    
    def add_folder_element(self, curr_package, node, isFL=False, isLeaf=False):
        use_case = self.add_use_case(curr_package, {"name":curr_package.attrib.get('name')})
        use_case_diagram = self.add_use_case_diagram(curr_package.attrib.get('xmi:id'), use_case.attrib.get('xmi:id'), {"name":curr_package.attrib.get('name')})
        element_diagram = self.add_subelement(use_case_diagram, 'elements')
        self.add_boundary(curr_package, element_diagram, {"id": curr_package.attrib.get('xmi:id'), "name": curr_package.attrib.get('name')})
        self.add_diagram_element(element_diagram, node)
      
    def add_package(self, parent, data):
        package = self.add_packaged_element(parent, {"xmi:type":"uml:Package", "xmi:id":data.get('id'), "name":data.get('name')})
        el_boundary = self.add_subelement(elements, 'element', {"xmi:idref":data.get('id'), "xmi:type":"uml:Package", "name":data.get('name')})
        self.add_subelement(el_boundary, "model", {"package":parent.attrib.get('xmi:id')})
        self.add_subelement(el_boundary, "properties", {"name": data.get('name'), "sType":"Package"})
        return package
    
    def add_boundary(self, parent, parent_ucd, data):
        self.add_subelement(parent, 'packagedElement', {"xmi:type":"uml:Class", "xmi:id":"B_" + data.get('id'), "name":data.get('name')})
        el_boundary = self.add_subelement(elements, 'element', {"xmi:idref":"B_" + data.get('id'), "xmi:type":"uml:Boundary", "name":data.get('name')})
        self.add_subelement(el_boundary, "model", {"package":parent.attrib.get('xmi:id')})
        self.add_subelement(el_boundary, "properties", {"name": data.get('name'), "sType":"Boundary"})
        self.add_subelement(parent_ucd, 'element', {"geometry":"Left=200;Top=60;Right=600;Bottom=600;", "subject":"B_" + data.get('id')})
    
    def add_use_case_diagram(self, package, diagram_owner, data):
        diagram = self.add_subelement(diagrams, "diagram", {"xmi:id":("d_" + package)})
        self.add_subelement(diagram, "model", {"package":package, "owner":package, "parent":diagram_owner})
        self.add_subelement(diagram, "properties", {"name": data.get('name'), "type":"Use Case"})
        self.add_subelement(diagram, "style1", {"value":"HideParents=0;"})
        
        return diagram

    def add_use_case(self, parent, data):
        use_case = self.add_subelement(parent, 'packagedElement', {"xmi:type":"uml:UseCase", "xmi:id":"UC_" + parent.attrib.get('xmi:id'), "name":data.get('name')})
        el_use_case = self.add_subelement(elements, 'element', {"xmi:idref":"UC_" + parent.attrib.get('xmi:id'), "xmi:type":"uml:UseCase", "name":data.get('name')})
        self.add_subelement(el_use_case, "model", {"package":parent.attrib.get('xmi:id')})
        self.add_subelement(el_use_case, "properties", {"name": data.get('name'), "sType":"UseCase"})
        self.add_subelement(el_use_case, "extendedProperties", {"diagram":"d_" + parent.attrib.get('xmi:id')})

        return use_case
    
    def add_diagram_element(self, use_case_diagram, node):
        top = 80
        bottom = top + 100
        id = node.attrib.get('id')
        for uc in list(node):
            self.add_subelement(use_case_diagram, 'element', {"geometry":"Left=200;Top=" + str(top) + ";Right=600;Bottom=" + str(bottom) + ";", "subject":"UC_" + uc.get('id')})
            top = top + 100
            bottom = bottom + 100

    # def add_element_tag(self, data_package, data):
        #  element = self.add_element(elements, 'element', {"xmi:idref":data.id, "xmi:type":("uml:" + data.type), "name": data.name})
        # self.add_subelement(element, 'model', {"package":data_package})
        # self.add_subelement(element, 'properties', {"sType":data.type})

    def add_packaged_element(self, parent, data):
        packagedElement = self.add_subelement(parent, "packagedElement", data)
        return packagedElement
    
    # def add_connectors(self, id_connector, start, end):
    #     connector = self.add_element('connector', {"xmi:idref":id_connector})

    #     source = self.add_subelement(connector, 'source', {"xmi:idref":start.id})
    #     self.add_subelement(source, 'model', {"type": start.type, "name": start.name})
    #     target = self.add_subelement(connector, 'target', {"xmi:idref":end.id})
    #     self.add_subelement(target, 'model', {"type": end.type, "name": end.name})

    #     connectors.append(connector)
    
    def add_element(self, tag_name, val_set):
        element = Element(tag_name)
        for val in val_set: element.set(val, val_set.get(val))

        return element
    
    def add_subelement(self, element, tag_name, val_set={}):
        subelement = SubElement(element, tag_name)
        for val in val_set: subelement.set(val, val_set.get(val))

        return subelement    
    
    def tostring(self):
        return ElementTree.tostring(self.xml_tree, encoding='unicode', method='xml')
    
    def write(self, filename):
        xmlstr = minidom.parseString(ElementTree.tostring(self.xml_tree)).toprettyxml(indent="   ") 
        with open(filename, "w") as f:
            f.write(xmlstr)