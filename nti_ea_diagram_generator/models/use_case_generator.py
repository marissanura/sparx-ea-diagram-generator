import base64
import tempfile
from .use_case_csv_reader import UCCSVReader
from .use_case_xml_writer import UCXMLWriter
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class UseCaseGenerator(models.Model):
    _name = 'use.case.generator'
    _description = 'Use Case Generator'
    _rec_name = 'module_name'

    module_name = fields.Char(required=True, string='Project Name')
    group_actor_id = fields.Many2one('group.actor', required=True, string='Group Actor')
    hierarchy_folder_id = fields.Many2one('hierarchy.folder', required=True, string='Hierarchy Folder')
    use_case_structure = fields.Binary(string='CSV File')
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
        datacsv = UCCSVReader(self.use_case_structure)
        actors = self.get_group_actor()
        folder_hierarcy = self.get_hierarchy_folder()

        try:
            use_case_tree = datacsv.generate_tree(folder_hierarcy)
            use_case = UCXMLWriter(use_case_tree, actors)

            xml_string = use_case.write()
            output = tempfile.NamedTemporaryFile(delete=False, suffix=".xml")
            output.write(xml_string.encode())

            output.seek(0)
            b64_output_structure = base64.b64encode(output.read())
            tmp = self.use_case_structure_filename.split('.')
            self.write({
                'generated_structure': b64_output_structure,
                'generated_structure_filename':  tmp[0] + '.xml'
            })
        except AttributeError as AE:
            print("Terdapat kesalahan pada pembacaan dan penerjemahan CSV ke XML")
    
    def get_group_actor(self):
        actors = {}
        for actor in list(self.group_actor_id.actor_ids):
            actors[actor.actor_name] = actor.type
        
        return actors
    
    def get_hierarchy_folder(self):
        hierarchy_folder = []
        for hierarchy in list(self.hierarchy_folder_id.folder_ids):
            hierarchy_folder.append(hierarchy.regex)
        
        return hierarchy_folder
