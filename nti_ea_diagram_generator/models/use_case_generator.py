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
        datacsv = UCCSVReader(self.use_case_structure)
        folder_hierarcy = ["\ASS-[0-9]{1,}\Z","\AUC-[0-9]{1,}\Z","\A\Z","\AUC-[0-9]{1,}-[0-9]{1,}\Z"]

        try:
            use_case_tree = datacsv.generate_tree(folder_hierarcy)
            print(use_case_tree)
            use_case = UCXMLWriter(use_case_tree)

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