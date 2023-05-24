from .activity_diagram_csv_reader import ADCSVReader
from .activity_diagram_xml_writer import ADXMLWriter
from odoo.addons.nti_ea_diagram_generator.models.generator import Generator
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ActivityDiagramGenerator(models.Model):
    _name = 'activity.generator'
    _description = 'Activity Diagram Generator'
    _rec_name = 'module_name'
    _inherit = "diagram.generator"
    
    def generate_diagram(self):
        csv_reader = ADCSVReader(self.use_case_structure)
        csv_writer = ADXMLWriter()

        super().generate(csv_reader, csv_writer)
