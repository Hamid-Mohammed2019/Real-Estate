from odoo import models,fields

class PropertyHeistery(models.Model):
    _name='property.heistery'
    _description='property heistry record'

    user_id=fields.Many2one('res.users')
    property_id=fields.Many2one('property.property')
    old_state=fields.Char()
    new_state=fields.Char()

