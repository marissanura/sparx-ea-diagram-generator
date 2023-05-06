import base64
import tempfile
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Generator(models.AbstractModel):
    _name = 'diagram.generator'
    _description = 'Diagram Generator'

    module_name = fields.Char(required=True, string='Project Name')
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
    
    def generate(self, csv_reader, xml_writer):
        try:
            use_case_tree = csv_reader.generate_tree()
            xml_writer.csv_tree_to_xml(use_case_tree)

            xml_string = xml_writer.write()
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
            print("Terdapat kesalahan pada pembacaan dan penerjemahan CSV ke XML\n" + str(AE))
