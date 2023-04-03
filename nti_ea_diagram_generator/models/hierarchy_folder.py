from odoo import models, fields

class HierarchyFolder(models.Model):
    _name = 'hierarchy.folder'
    _description = 'Hierarchy Folder'
    _rec_name = 'hierarchy_name'

    hierarchy_name = fields.Char(required=True)
    folder_ids = fields.One2many(
        comodel_name='folder',
        inverse_name='folder_id',
        string='Hierarchy Folder',
    )

    hierarchy_folder_ids = fields.One2many(
        comodel_name='use.case.generator',
        inverse_name='hierarchy_folder_id',
        string='Hierarchy Folder',
    )

class Folder(models.Model):
    _name = "folder"

    hierarchy = fields.Char(string='Hierarchy', required=True)
    regex = fields.Char(string='Regex', required=True)
    folder_id = fields.Many2one(
        comodel_name='hierarchy.folder',
        string='Hierarchy Folder',
    )