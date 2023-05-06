from .use_case_csv_reader import UCCSVReader
from .use_case_xml_writer import UCXMLWriter
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class UseCaseGenerator(models.Model):
    _name = 'activity.generator'
    _description = 'Activity Diagram Generator'
    _rec_name = 'module_name'
    _inherit = "diagram.generator"

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
        actors = self.get_group_actor()
        folder_hierarcy = self.get_hierarchy_folder()
        csv_reader = UCCSVReader(self.use_case_structure, folder_hierarcy)
        csv_writer = UCXMLWriter(actors)

        super().generate(csv_reader, csv_writer)
    
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
