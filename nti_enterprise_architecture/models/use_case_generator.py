# -*- coding: utf-8 -*-

import base64
import binascii
import re
import tempfile
import csv
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class UseCaseGenerator(models.Model):
    _name = 'use.case.generator'
    _description = 'Use Case Generator'
    _rec_name = 'module_name'

    module_name = fields.Char(required=True)
    project_id = fields.Many2one(
        comodel_name='project.project',
        string="Project"
    )
    description = fields.Text(string='Description')
    use_case_structure = fields.Binary(string='Use Case Structure')
    use_case_structure_filename = fields.Char()
    generated_structure = fields.Binary(string='Generated Structure')
    generated_structure_filename = fields.Char()

    @api.constrains('use_case_structure_filename')
    def _check_filename(self):
        if self.use_case_structure:
            if not self.use_case_structure_filename:
                raise ValidationError(("There is no file"))
            else:
                # Check the file's extension
                tmp = self.use_case_structure_filename.split('.')
                ext = tmp[len(tmp)-1]
                if ext != 'csv':
                    raise ValidationError(("The file must be a csv file"))

    def generate_structure(self):
        uc = []
        ad = []
        uid = []
        navcell = []
        elements = []
        diagram = []
        d = []

        def print_header():
            output_structure.write(b"""<?xml version="1.0" encoding="windows-1252"?>
        <xmi:XMI xmi:version="2.1" xmlns:uml="http://schema.omg.org/spec/UML/2.1" xmlns:xmi="http://schema.omg.org/spec/XMI/2.1" xmlns:thecustomprofile="http://www.sparxsystems.com/profiles/thecustomprofile/1.0">
            <xmi:Documentation exporter="Enterprise Architect" exporterVersion="6.5" exporterID="1554"/>
            <uml:Model xmi:type="uml:Model" name="EA_Model" >
            """)

        def write_root(name):
            uc.append("""<packagedElement xmi:type="uml:Package" xmi:id="rf" name="{name}" >
                    <packagedElement xmi:type="uml:Class" xmi:id="uc_r" name="Use Case Diagram - {name}" />
            """.format(name=name))

            elements.append("""    		<element xmi:idref="uc_r" xmi:type="uml:Boundary" name="Use Case Diagram - {name}" scope="public">
                        <model ea_eleType="element"/>
                        <properties sType="Boundary"/>
                    </element>
            """.format(name=name))

            diagram.append("""    		<diagram xmi:id="d_uc_r">
                        <model owner="rf"/>
                        <properties name="UC - {name}" type="Use Case"/>
                    </diagram>
            """.format(name=name))

        def write_subfolder(id, name):
            uc.append("""    		<packagedElement xmi:type="uml:Package" xmi:id="sf_{id}" name="UC - {name}" >
                        <packagedElement xmi:type="uml:UseCase" xmi:id="uc_sf_{id}" name="{name}" />
            """.format(id=id, name=name))

            ad.append("""    		<packagedElement xmi:type="uml:Package" xmi:id="ad_sf_{id}" name="AD - {name}" >
            """.format(id=id, name=name))

            uid.append("""    		<packagedElement xmi:type="uml:Package" xmi:id="uid_sf_{id}" name="UID - {name}" >
            """.format(id=id, name=name))

            diagram.append("""    		<diagram xmi:id="d_uc_sf_{id}">
                        <model owner="sf_{id}" parent="uc_sf_{id}"/>
                        <properties name="{name}" type="Use Case"/>
                    </diagram>
            """.format(id=id, name=name))

        def close_tag(tag):
            close_tag = """</{close_tag}>""".format(close_tag=tag)
            output_structure.write(close_tag.encode('ascii'))

        def write_folder(id, name):
            uc.append("""<packagedElement xmi:type="uml:Package" xmi:id="f_uc_{id}" name="UC - {name}" >
                                <packagedElement xmi:type="uml:UseCase" xmi:id="uc_{id}" name="{name}" >
                                    <nestedClassifier xmi:type="uml:Class" xmi:id="l_ad_{id}" />
                                    <nestedClassifier xmi:type="uml:Class" xmi:id="l_uid_{id}" />
                                </packagedElement>
                            </packagedElement>
            """.format(id=id, name=name))

            ad.append("""           <packagedElement xmi:type="uml:Package" xmi:id="f_ad_{id}" name="AD - {name}" />
            """.format(id=id, name=name))

            uid.append("""          <packagedElement xmi:type="uml:Package" xmi:id="f_uid_{id}" name="UID - {name}" />
            """.format(id=id, name=name))

            elements.append("""    		<element xmi:idref="l_ad_{id}" xmi:type="uml:Text" >
                        <model owner="f_uc_{id}" ea_eleType="element"/>
                        <properties sType="Text" nType="82" alias="AD - {name}" stereotype="NavigationCell"/>
                        <style appearance="BackColor=-1;BorderColor=-1;BorderWidth=-1;FontColor=-1;VSwimLanes=1;HSwimLanes=1;BorderStyle=0;" styleex="NID=2-43;"/>
                        <extendedProperties diagram="d_ad_{id}"/>
                    </element>
                    <element xmi:idref="l_uid_{id}" xmi:type="uml:Text" >
                        <model owner="f_uc_{id}" ea_eleType="element"/>
                        <style appearance="BackColor=-1;BorderColor=-1;BorderWidth=-1;FontColor=-1;VSwimLanes=1;HSwimLanes=1;BorderStyle=0;" styleex="NID=2-27;"/>
                        <properties sType="Text" nType="82" alias="UID - {name}" stereotype="NavigationCell"/>
                        <extendedProperties diagram="d_uid_{id}"/>
                    </element>
            """.format(id=id, name=name))

            diagram.append("""    		<diagram xmi:id="d_ad_{id}">
                        <model owner="f_ad_{id}"/>
                        <properties name="AD - {name}" type="Analysis"/>
                        <style2 value="MDGDgm=BPMN2.0::Business Process;"/>
                        <extendedProperties/>
                    </diagram>
                    <diagram xmi:id="d_uc_f_{id}">
                        <model owner="f_uc_{id}" parent="uc_{id}"/>
                        <properties name="{name}" type="Use Case"/>
                        <elements>
                            <element geometry="Left=19;Top=22;Right=189;Bottom=137;" subject="l_ad_{id}" style="font=Calibri;fontsz=140;bold=0;black=0;italic=0;ul=0;charset=0;pitch=0;DUID=20D60F07;"/>
                            <element geometry="Left=232;Top=22;Right=402;Bottom=137;" subject="l_uid_{id}" style="font=Calibri;fontsz=140;bold=0;black=0;italic=0;ul=0;charset=0;pitch=0;DUID=EEC8258D;"/>
                        </elements>
                    </diagram>
                    <diagram xmi:id="d_uid_{id}">
                        <model owner="f_uid_{id}"/>
                        <properties name="UID - {name}" type="Custom"/>
                        <style2 value="MDGDgm=Wireframing::Webpage Wireframe;Whiteboard=1;"/>
                        <extendedProperties/>
                    </diagram>
            """.format(id=id, name=name))

            navcell.append("""    	<thecustomprofile:NavigationCell base_Class="l_ad_{id}"/>
                <thecustomprofile:NavigationCell base_Class="l_uid_{id}"/>
            """.format(id=id, name=name))

        def write_body():
            print(d)
            i = 0
            subfolder = 0
            folder = 0
            while (i < len(d)):
                if (d[i][0] != ''):
                    write_root(d[i][0])
                elif (d[i][1] != ''):
                    if (subfolder != 0):
                        uc.append("""</packagedElement>
                        """)
                        ad.append("""</packagedElement>
                        """)
                        uid.append("""</packagedElement>
                        """)
                    write_subfolder(subfolder, d[i][1])

                    subfolder += 1
                elif (d[i][2] != ''):
                    write_folder(folder, d[i][2])
                    folder += 1

                i += 1

            uc.append("""</packagedElement>""")
            ad.append("""</packagedElement>""")
            uid.append("""</packagedElement>
            </packagedElement>
            """)

        def print_body():
            write_body()

            for u in uc:
                output_structure.write(u.encode('ascii'))

            for a in ad:
                output_structure.write(a.encode('ascii'))

            for ui in uid:
                output_structure.write(ui.encode('ascii'))

            for n in navcell:
                output_structure.write(n.encode('ascii'))

            output_structure.write(b"""
            </uml:Model>
            <xmi:Extension extender="Enterprise Architect" extenderID="6.5">
                <elements>
            """)

            for e in elements:
                output_structure.write(e.encode('ascii'))

            output_structure.write(b"""
            </elements>
            <diagrams>
            """)

            for d in diagram:
                output_structure.write(d.encode('ascii'))

            output_structure.write(b"""
            </diagrams>
            </xmi:Extension>
        """)

        temp = base64.b64decode(self.use_case_structure)
        lines = temp.decode('utf-8-sig').splitlines()
        for line in lines:
            res = line.split(";")
            d.append(res)
        print(d)

        output_structure = tempfile.NamedTemporaryFile(
            delete=False, suffix=".xml")
        print_header()
        print_body()
        close_tag("xmi:XMI")

        output_structure.seek(0)
        b64_output_structure = base64.b64encode(output_structure.read())
        tmp = self.use_case_structure_filename.split('.')
        self.write({
            'generated_structure': b64_output_structure,
            'generated_structure_filename':  tmp[0] + '.xml'
        })
