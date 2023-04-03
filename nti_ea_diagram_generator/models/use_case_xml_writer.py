import base64
import tempfile
from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import (Element, SubElement)

from .xml_writer import XMLWriter

class UCXMLWriter(XMLWriter):
    actor = {"Administrator":"ns", "User":"ns", "Creator":"ns", "Reviewer":"ns", "Viewer":"ns", "Approver":"ns", "Sistem 1":"s"}

    def csv_tree_to_xml(self):
        self.init_template()
        self.init_actor(self.tree, self.tree[0], 0)

        global root_package
        
        root_package = self.add_packaged_element(model, {"xmi:type":"uml:Package", "xmi:id":"root", "name":"Application use Case Diagram"})
        self.add_catalog_actor(root_package)
        use_case_package = self.add_packaged_element(root_package, {"xmi:type":"uml:Package", "xmi:id":"use_case_diagram", "name":"Use Case Diagram"})
        if len(list(self.tree)) > 0: self.tree_traverse(use_case_package, self.tree, self.tree[0], 0)
    
    def init_actor(self, parent, node, index):
        if len(list(node)) > 0: self.init_actor(node, node[0], 0)
        if parent.attrib.get('actor') == '' or parent.attrib.get('actor') == None:
            parent.set('actor', node.attrib.get('actor')) 
        else: 
            new_list = list(str(parent.attrib.get('actor')).split(", ")) + list(set(list(str(node.attrib.get('actor')).split(", "))) - set(list(str(parent.attrib.get('actor')).split(", "))))
            new_string = ', '.join(new_list)
            parent.set('actor', new_string)
        if len(list(parent)) - 1 > index: self.init_actor(parent, parent[index + 1], index+1)

    def init_template(self):
        ElementTree.register_namespace('xmi', "http://schema.omg.org/spec/XMI/2.1")
        ElementTree.register_namespace('uml', "http://schema.omg.org/spec/UML/2.1")
        ElementTree.register_namespace('thecustomprofile', "http://www.sparxsystems.com/profiles/thecustomprofile/1.0")
        tree = ElementTree.parse('/Users/marissanuramalia/Desktop/Coolyeah/Repositories/GitHub/sparx-ea-diagram-generator/nti_ea_diagram_generator/models/template.xml')
        self.xml_tree = tree.getroot()

        global model, elements, connectors, diagrams
        
        model = self.xml_tree[1]
        elements = self.xml_tree[2][0]
        connectors = self.xml_tree[2][1]
        diagrams = self.xml_tree[2][2]    

    def add_catalog_actor(self, package):
        catalog_actor = self.add_package(package, {"id":"catalog_actor_package", "name":"Actor"})
        use_case_diagram = self.add_use_case_diagram(catalog_actor.attrib.get('xmi:id'), catalog_actor.attrib.get('xmi:id'), {"name":catalog_actor.attrib.get('name')})
        element_diagram = self.add_subelement(use_case_diagram, 'elements')
        
        top = 50
        bottom = 140
        left = 50
        right = left + 45

        index = 1
        for actor in self.actor.keys():
            self.add_packaged_element(catalog_actor, {"xmi:type":"uml:Actor", "xmi:id":actor.replace(" ", ""), "name":actor})
            self.add_subelement(element_diagram, 'element', {"geometry":"Left=" + str(left) + ";Top=" + str(top) + ";Right=" + str(right) + ";Bottom=" + str(bottom) + ";", "subject":actor.replace(" ", "")}) if self.actor.get(actor) == "ns" else self.add_subelement(element_diagram, 'element', {"geometry":"Left=" + str(left) + ";Top=" + str(top) + ";Right=" + str(right) + ";Bottom=" + str(bottom) + ";", "subject":actor.replace(" ", ""), "style":"BCol=15453831;"}) 
            left += 60
            right += 60

            if (index % 5 == 0):
                left = 50
                right = left + 45
                top += 105
                bottom += 105
            
            index += 1

        length = 65 + (5 if len(self.actor) > 5 else len(self.actor)) * 60
        height = 50 + ((len(self.actor) / 5) + (1 if len(self.actor) % 5 > 0 else 0)) * 105
        self.add_boundary(catalog_actor, {"id": catalog_actor.attrib.get('xmi:id'), "name": catalog_actor.attrib.get('name')})
        self.add_subelement(element_diagram, 'element', {"geometry":"Left=20;Top=20;Right=" + str(length) + ";Bottom=" + str(height), "subject":"B_catalog_actor_package"})

    def tree_traverse(self, parent_package, parent, node, index):
        curr_package = self.add_package(parent_package, {"id":node.attrib.get('id'), "name":node.attrib.get('name')})
        self.add_folder_element(curr_package, node)

        if len(list(node)) > 0: self.tree_traverse(curr_package, node, node[0], 0)
        if len(list(parent)) - 1 > index: self.tree_traverse(parent_package, parent, parent[index + 1], index+1)
    
    def add_folder_element(self, curr_package, node):
        use_case = self.add_use_case(curr_package, {"name":curr_package.attrib.get('name')})
        use_case_diagram = self.add_use_case_diagram(curr_package.attrib.get('xmi:id'), use_case.attrib.get('xmi:id'), {"name":curr_package.attrib.get('name')})
        self.add_relation(curr_package, node)

        if len(list(node)) != 0:
            element_diagram = self.add_subelement(use_case_diagram, 'elements')
            self.add_boundary(curr_package, {"id": curr_package.attrib.get('xmi:id'), "name": curr_package.attrib.get('name')})
            self.add_diagram_element(element_diagram, node)
      
    def add_package(self, parent, data):
        package = self.add_packaged_element(parent, {"xmi:type":"uml:Package", "xmi:id":data.get('id'), "name":data.get('name')})
        el_boundary = self.add_subelement(elements, 'element', {"xmi:idref":data.get('id'), "xmi:type":"uml:Package", "name":data.get('name')})
        self.add_subelement(el_boundary, "model", {"package":parent.attrib.get('xmi:id')})
        self.add_subelement(el_boundary, "properties", {"name": data.get('name'), "sType":"Package"})
        return package
    
    def add_boundary(self, parent, data):
        self.add_subelement(parent, 'packagedElement', {"xmi:type":"uml:Class", "xmi:id":"B_" + data.get('id'), "name":data.get('name')})
        el_boundary = self.add_subelement(elements, 'element', {"xmi:idref":"B_" + data.get('id'), "xmi:type":"uml:Boundary", "name":data.get('name')})
        self.add_subelement(el_boundary, "model", {"package":parent.attrib.get('xmi:id')})
        self.add_subelement(el_boundary, "properties", {"name": data.get('name'), "sType":"Boundary"})
    
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
    
    def calculate_use_case_dimension(self, node):
        max_uc_name = ""
        for uc_name in list(node): max_uc_name = uc_name.get('name') if len(max_uc_name) < len(uc_name.get('name')) else max_uc_name
        x, y = 105, 70
        char_max = len(max_uc_name) - 40

        gap = 0
        while(char_max > 0):
            x += 15
            y += 10
            char_max -= (28 + gap)
            gap += 4 if (gap/2 == 0) else 6
        
        return x,y

    def add_diagram_element(self, use_case_diagram, node):
        x, y = self.calculate_use_case_dimension(node)
        
        actors = list(node.attrib.get('actor').split(", "))
        use_case = list(node)
        actor_gap = 15

        if (len(actors) > ((len(use_case) * 2) + 2)):
            top = 50 + ((x + 15)/2)
            height = top + ((len(use_case) - 1) * (y + 15)) + y + 30 + ((x + 15)/2)
            actor_gap = 15
        else:
            top = 50
            height = 50 + ((len(use_case) - 1) * (y + 15)) + y + 30
            actor_gap = 15 if (len(actors) >= len(use_case) or len(actors) == 1) else ((height - 20) - (90 * len(actors))) / (len(actors) - 1)

        a_top = 20
        a_bottom =  a_top + 90
        a_left = 20
        a_right = a_left + 45
        
        actor_pos = {}
        for actor in actors:
            self.add_subelement(use_case_diagram, 'element', {"geometry":"Left=" + str(a_left) + ";Top=" + str(a_top) + ";Right=" + str(a_right) + ";Bottom=" + str(a_bottom) + ";", "subject":actor.replace(" ", "")}) if self.actor.get(actor) == "ns" else self.add_subelement(use_case_diagram, 'element', {"geometry":"Left=" + str(a_left) + ";Top=" + str(a_top) + ";Right=" + str(a_right) + ";Bottom=" + str(a_bottom) + ";", "subject":actor.replace(" ", ""), "style":"BCol=15453831;"})
            actor_pos[actor] = 'l' if (a_left < (185 + (x/2))) else 'r'
            
            a_top = a_bottom + actor_gap
            a_bottom = a_top + 90

            if(a_bottom > height):
                if(a_left == (305 + x)):
                    a_left = 125 
                    a_right = a_left + 45
                    a_top = height + 20
                    a_bottom = a_top + 90
                elif(top > height + 20):
                    a_left = 200 + x
                    a_right = a_left + 45
                    a_top = height + 20
                    a_bottom = a_top + 90
                else:
                    a_left = 305 + x
                    a_right = a_left + 45
                    a_top = 20
                    a_bottom = a_top + y  

        bottom = top + y
        left = 185
        right = left + x

        self.add_subelement(use_case_diagram, 'element', {"geometry":"Left=125;Top=20;Right=" + str(125 + 120 + x) + ";Bottom=" + str(height) +  ";", "subject":"B_" + node.get('id')})

        for uc in list(node):
            self.add_subelement(use_case_diagram, 'element', {"geometry":"Left=" + str(left) + ";Top=" + str(top) + ";Right=" + str(right) + ";Bottom=" + str(bottom) + ";", "subject":"UC_" + uc.get('id')})
            top = bottom + 15
            bottom = top + y
            index = 1
            for actor in list(uc.get('actor').split(", ")):
                ex_actor = (-x/2) if actor_pos.get(actor) == 'l' else (x/2)
                self.add_subelement(use_case_diagram, 'element', {"geometry":"SX=0;SY=0;EX=" + str(ex_actor) +";EY=0;", "subject":"a" + str(index) + "_"+ uc.get('id')}) if self.actor.get(actor) == "ns" else self.add_subelement(use_case_diagram, 'element', {"geometry":"SX=" + str(ex_actor) + ";SY=0;EX=0;EY=0;", "subject":"u" + str(index) + "_"+ uc.get('id')})
                index = index + 1
            if uc.get('ket') != "":
                for ket in list(uc.attrib.get('ket').split(", ")):
                    lists = ket.split(' ')
                    if lists[0] == "generalization": self.add_subelement(use_case_diagram, 'element', {"geometry":"SX=0;SY=0;EX=0;EY=0;", "subject":"g" + str(index) + "_"+ uc.get('id')})
                    elif lists[0] == "extend": self.add_subelement(use_case_diagram, 'element', {"geometry":"SX=0;SY=0;EX=0;EY=0;", "subject":"e" + str(index) + "_"+ uc.get('id')})
                    elif lists[0] == "include": self.add_subelement(use_case_diagram, 'element', {"geometry":"SX=0;SY=0;EX=0;EY=0;", "subject":"i" + str(index) + "_"+ uc.get('id')})
                    index = index + 1

    def add_packaged_element(self, parent, data):
        packagedElement = self.add_subelement(parent, "packagedElement", data)
        return packagedElement
    
    def add_relation(self, curr_package, node):
        index = 1
        for actor in list(node.attrib.get('actor').split(", ")):
            self.add_association(curr_package, actor, index) if self.actor.get(actor) == "ns" else self.add_usage(curr_package, actor, index)
            index = index + 1
        
        if node.attrib.get('ket') != "": 
            for ket in list(node.attrib.get('ket').split(", ")):
                lists = ket.split(' ')
                for tag in self.tree.iter(str(lists[1])): target = tag
                if lists[0] == "generalization": self.add_generalization(curr_package, target, index)
                elif lists[0] == "extend": self.add_extend(curr_package, target, index)
                elif lists[0] == "include": self.add_include(curr_package, target, index)

    def add_association(self, curr_package, actor, index):
        association = self.add_packaged_element(curr_package, {"xmi:type":"uml:Association", "xmi:id":"a" + str(index) + "_" + curr_package.attrib.get('xmi:id') })
        self.add_subelement(association, 'memberEnd', {"xmi:idref":"src_" + association.attrib.get('xmi:id')})
        self.add_subelement(association, 'memberEnd', {"xmi:idref":"dst_" + association.attrib.get('xmi:id')})
        src = self.add_subelement(association, 'ownedEnd', {"xmi:type":"uml:Property", "xmi:id":"src_" + association.attrib.get('xmi:id'), "association":association.attrib.get('xmi:id')})
        self.add_subelement(src, 'type', {"xmi:idref": "UC_" + curr_package.attrib.get('xmi:id')})
        dst = self.add_subelement(association, 'ownedEnd', {"xmi:type":"uml:Property", "xmi:id":"dst_" + association.attrib.get('xmi:id'), "association":association.attrib.get('xmi:id')})
        self.add_subelement(dst, 'type', {"xmi:idref":actor.replace(" ", "")})

        self.add_connectors('association', association.attrib.get('xmi:id'), {"type":"UseCase", "id":curr_package.attrib.get('xmi:id'), "name":curr_package.attrib.get('name')}, {"type":"Actor", "id":actor.replace(" ", ""), "name":actor})
    
    def add_usage(self, curr_package, actor, index):
        usage = self.add_packaged_element(curr_package, {"xmi:type":"uml:Usage", "xmi:id":"u" + str(index) + "_" + curr_package.attrib.get('xmi:id'), "supplier":actor.replace(" ", ""), "client": "UC_" + curr_package.attrib.get('xmi:id')})
        self.add_connectors('usage', usage.attrib.get('xmi:id'), {"type":"UseCase", "id":"UC_" + curr_package.attrib.get('xmi:id'), "name":curr_package.attrib.get('name')}, {"type":"Actor", "id":actor.replace(" ", ""), "name":actor})
    
    def add_generalization(self, curr_package, node_target, index):
        generalization = self.add_subelement(curr_package, "generalization", {"xmi:type":"uml:Generalization", "xmi:id":"g" + str(index) + "_" + curr_package.attrib.get('xmi:id'), "general":"UC_" + node_target.attrib.get('id')})
        self.add_connectors('generalization', generalization.attrib.get('xmi:id'), {"type":"UseCase", "id":"UC_" + curr_package.attrib.get('xmi:id'), "name":curr_package.attrib.get('name')}, {"type":"UseCase", "id":"UC_" + node_target.attrib.get('id'), "name":node_target.attrib.get('name')})
    
    def add_extend(self, curr_package, node_target, index):
        extend = self.add_subelement(curr_package, "extend", {"xmi:type":"uml:Extend", "xmi:id":"e" + str(index) + "_" + curr_package.attrib.get('xmi:id'), "extendedCase":"UC_" + node_target.attrib.get('id')})
        self.add_connectors('extend', extend.attrib.get('xmi:id'), {"type":"UseCase", "id":"UC_" + curr_package.attrib.get('xmi:id'), "name":curr_package.attrib.get('name')}, {"type":"UseCase", "id":"UC_" + node_target.attrib.get('id'), "name":node_target.attrib.get('name')})
    
    def add_include(self, curr_package, node_target, index):
        include = self.add_packaged_element(curr_package, {"xmi:type":"uml:Include", "xmi:id":"i" + str(index) + "_" + curr_package.attrib.get('xmi:id'), "addition":"UC_" + node_target.attrib.get('id')})
        self.add_connectors('include', include.attrib.get('xmi:id'), {"type":"UseCase", "id":"UC_"+ curr_package.attrib.get('xmi:id'), "name":curr_package.attrib.get('name')}, {"type":"UseCase", "id":"UC_" + node_target.attrib.get('id'), "name":node_target.attrib.get('name')})
    
    def add_connectors(self, type, id_connector, start, end):
        connector = self.add_subelement(connectors, 'connector', {"xmi:idref":id_connector})

        source = self.add_subelement(connector, 'source', {"xmi:idref":start.get('id')})
        self.add_subelement(source, 'model', {"type": start.get('type'), "name": start.get('name')})
        target = self.add_subelement(connector, 'target', {"xmi:idref":end.get('id')})
        self.add_subelement(target, 'model', {"type": end.get('type'), "name": end.get('name')})

        if type == "include" or type == "extend":
            self.add_subelement(connector, 'properties', {"subtype":type.capitalize(), "stereotype":type, "direction":"Source -> Destination"})
        elif type == "usage":
            self.add_subelement(connector, 'properties', {"ea_type":"Usage", "direction":"Source -> Destination"})
    
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
    
    def write(self):
        xmlstr = minidom.parseString(ElementTree.tostring(self.xml_tree)).toprettyxml(indent="   ") 
        return xmlstr