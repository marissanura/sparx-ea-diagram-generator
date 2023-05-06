from xml.dom import minidom
from xml.etree import ElementTree
from xml.etree.ElementTree import (Element, SubElement)
from xml_writer import XMLWriter

class ADXMLWriter(XMLWriter):
    def csv_tree_to_xml(self):
        self.init_template()

        global root_package
        
        root_package = self.add_packaged_element(model, {"xmi:type":"uml:Package", "xmi:id":"root", "name":"Activity Diagram"})
        package_element = self.add_subelement(elements, "element", {"xmi:idref": "root", "xmi:type":"uml:Package", "name":"Activity Diagram"})
        self.add_subelement(package_element, "model", {"package": "root"})
        self.add_subelement(package_element, "properties", {"sType":"Package"})

        self.add_folder_element(root_package)
    
    def init_template(self):
        ElementTree.register_namespace('xmi', "http://schema.omg.org/spec/XMI/2.1")
        ElementTree.register_namespace('uml', "http://schema.omg.org/spec/UML/2.1")
        ElementTree.register_namespace('BPMN2.0', "http://www.sparxsystems.com/profiles/BPMN2.0/1.5")
        tree = ElementTree.parse('template.xml')
        self.xml_tree = tree.getroot()

        global model, elements, connectors, diagrams
        
        model = self.xml_tree[1]
        elements = self.xml_tree[2][0]
        connectors = self.xml_tree[2][1]
        diagrams = self.xml_tree[2][2]    

    def add_folder_element(self, parent):
        print(self.tree)
        ad_package = self.add_packaged_element(parent, {"xmi:type":"uml:Package", "xmi:id":"ad_diagram", "name": self.tree.get("name")})
        activity = self.add_packaged_element(ad_package, {"xmi:type":"uml:Activity", "xmi:id":"activity_diagram", "name":"EA_Activity1"})
        package_element = self.add_subelement(elements, "element", {"xmi:idref": "ad_diagram", "xmi:type":"uml:Package", "name": self.tree.get("name")})
        self.add_subelement(package_element, "model", {"package": "root"})
        self.add_subelement(package_element, "properties", {"sType":"Package"})
        self.add_pool(activity, self.tree)

        self.add_diagram(activity)
    
    def add_pool(self, parent, node):
        pool = self.add_subelement(parent, "group", {"xmi:type":"uml:ActivityPartition", "xmi:id": "pool", "name": node.get("name")})

        pool_element = self.add_subelement(elements, "element", {"xmi:idref": "pool", "xmi:type":"uml:ActivityPartition", "name": node.get("name")})
        self.add_subelement(pool_element, "model", {"package": "ad_diagram"})
        self.add_subelement(pool_element, "properties", {"sType":"ActivityPartition", "stereotype":"Pool"})
        tag = self.add_subelement(pool_element, "tags", {})
        self.add_subelement(tag, "tag", {"xmi:id": "blackboxpool", "name":"blackBoxPool", "value":"false#NOTES#Values: true,false\nDefault: false\n", "modelElement": node.get("name")})
        self.add_subelement(tag, "tag", {"xmi:id":"participant", "name":"participantMultiplicity", "value":"false#NOTES#Values: true,false\nDefault: false\n", "modelElement": node.get("name")})

        lanes = list(str(node.get('lanes')).split(", "))
        lane_index = 0
        for l in lanes:
            lane = self.add_lane(pool, l)
            self.add_node_lane(pool, lane, node, lane_index)

            lane_index += 1

    def add_lane(self, parent, node):
        lane = self.add_subelement(parent, "subpartition", {"xmi:type":"uml:ActivityPartition", "xmi:id": node, "name": node})
        lane_element = self.add_subelement(elements, "element", {"xmi:idref": node, "xmi:type":"uml:ActivityPartition", "name": node})
        self.add_subelement(lane_element, "model", {"package": "ad_diagram", "owner":"pool"})
        self.add_subelement(lane_element, "properties", {"sType":"ActivityPartition", "stereotype":"Lane"})
        return lane

    def add_node_lane(self, pool, parent, node, lane_index):
        lane_nodes = node.findall("lane" + str(lane_index))
        lanes = list(str(node.get('lanes')).split(", "))

        for activity in lane_nodes:
            # print(activity.get("name"))
            if (activity.get("name") != "end" and activity.get("name") != "start"):
                print(activity.get("name"))
                self.add_subelement(parent, "node", {"xmi:idref": activity.get("id")})
                self.add_packaged_element(pool, {"xmi:type":"uml:Activity", "xmi:id":activity.get("id"), "name":activity.get("name")})            
                lane_element = self.add_subelement(elements, "element", {"xmi:idref": activity.get("id"), "xmi:type":"uml:Activity", "name": activity.get("name")})
                self.add_subelement(lane_element, "model", {"package": "ad_diagram", "owner": lanes[int(activity.get("lane"))]})
                self.add_subelement(lane_element, "properties", {"sType":"Activity", "stereotype":"Activity"})
            elif (activity.get("name") == "end"):
                self.add_subelement(parent, "node", {"xmi:idref": activity.get("id")})
                self.add_subelement(pool, "node", {"xmi:type":"uml:SendSignalAction", "xmi:id":activity.get("id"), "name":" "})
                lane_element = self.add_subelement(elements, "element", {"xmi:idref": activity.get("id"), "xmi:type":"uml:Event", "name": activity.get("name")})
                self.add_subelement(lane_element, "model", {"package": "ad_diagram", "owner": lanes[int(activity.get("lane"))]})
                self.add_subelement(lane_element, "properties", {"sType":"Event", "stereotype":"StartEvent"})
            elif (activity.get("name") == "start"):
                self.add_subelement(parent, "node", {"xmi:idref": activity.get("id")})
                self.add_subelement(pool, "node", {"xmi:type":"uml:SendSignalAction", "xmi:id":activity.get("id"), "name":" "})
                lane_element = self.add_subelement(elements, "element", {"xmi:idref": activity.get("id"), "xmi:type":"uml:Event", "name": activity.get("name")})
                self.add_subelement(lane_element, "model", {"package": "ad_diagram", "owner":lanes[int(activity.get("lane"))]})
                self.add_subelement(lane_element, "properties", {"sType":"Event", "stereotype":"EndEvent"})

    def add_diagram(self, parent):
        diagram = self.add_subelement(diagrams, "diagram", {"xmi:id":"diagram"})
        self.add_subelement(diagram, "model", {"package": "ad_diagram", "owner": "ad_diagram"})
        self.add_subelement(diagram, "properties", {"name": parent.get("name"), "type":"Analysis"})
        self.add_subelement(diagram, "style2", {"value":"MDGDgm=BPMN2.0::Business Process;"})

        self.add_diagram_element(diagram)

    def add_diagram_element(self, parent):
        elements = self.add_subelement(parent, "elements", {})
        lanes = list(str(self.tree.get('lanes')).split(", "))
        lane_nodes = list(self.tree)

        height = len(lanes) * 120
        width = len(self.tree) * 140
        self.add_subelement(elements, "element", {"geometry":"Left=20;Top=20;Right=" + str(20 + width) + ";Bottom=" + str(20 + height) +";", "subject":"pool"})

        top = 20
        bottom = 150 + top
        for l in lanes:
            self.add_subelement(elements, "element", {"geometry":"Left=40;Top=" + str(top) +";Right=" + str(20 + width) + ";Bottom=" + str(bottom) + ";", "subject": l })
            top = bottom
            bottom = 150 + top
        
        left = 70
        for node in lane_nodes:
            if (node.get("name") != "end" and node.get("name") != "start"):
                top = 20 + (150 * int(node.get("lane"))) + 30
                bottom = top + 60
                right = left + 110
                self.add_subelement(elements, "element", {"geometry":"Left=" + str(left) + ";Top=" + str(top) + ";Right=" + str(right) + ";Bottom=" + str(bottom) + ";", "subject": node.get("id") })
                left = right + 20
            else:
                top = 20 + (150 * int(node.get("lane"))) + 45
                bottom = top + 30
                right = left + 30
                self.add_subelement(elements, "element", {"geometry":"Left=" + str(left) + ";Top=" + str(top) + ";Right=" + str(right) + ";Bottom=" + str(bottom) + ";", "subject": node.get("id") })
                left = right + 20
    
    def add_packaged_element(self, parent, data):
        packagedElement = self.add_subelement(parent, "packagedElement", data)
        return packagedElement
    
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