from odoo import models, fields, api
from odoo.exceptions import ValidationError


class GroupActor(models.Model):
    _name = 'group.actor'
    _description = 'Group Actor'
    _rec_name = 'group_name'

    group_name = fields.Char(required=True, string='Group Name')
    actor_ids = fields.One2many(
        comodel_name='actor',
        inverse_name='actor_id',
        string='List Actor',
        required=True,
    )

    group_actor_ids = fields.One2many(
        comodel_name='use.case.generator',
        inverse_name='group_actor_id',
        string='Group Actor',
    )

    @api.constrains('actor_ids')
    def _check_actor(self):
        if len(self.actor_ids) < 1:
            raise ValidationError(("There is no List Actor"))

class Actor(models.Model):
    _name = "actor"

    actor_name = fields.Char(string='Actor Name', required=True)
    type = fields.Selection([("s","System"),("ns","Non System")], string='Type', required=True)
    actor_id = fields.Many2one(
        comodel_name='group.actor',
        string='Actor',
    )