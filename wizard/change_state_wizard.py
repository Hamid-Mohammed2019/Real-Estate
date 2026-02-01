from odoo import  fields, models

class changestate(models.TransientModel):
    _name = 'change.state'
    _description = 'change state record'

    
    property_id=fields.Many2one('property.property')
    state=fields.Selection([
        ['draft','draft'],
        ['pending','pending']
    ], default='draft') 
    reson=fields.Char()
    
    def action_confirm(self):
        print(' inside method')

