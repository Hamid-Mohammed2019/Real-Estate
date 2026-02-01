from odoo import models,fields,api

class Owner(models.Model):
    _name='owner.owner'
    _decription="Owner record"
    _inherit=['mail.thread','mail.activity.mixin']
    # ref=fields.char(default='new')
    ref=fields.Char(default='New' ,readonly=True)
    name=fields.Char()
    phone=fields.Char()
    Email=fields.Char()
    state=fields.Selection([
        ['draft','draft'],
        ['pending','pending'],
        ['sold','sold'],
        ['close','close']
    ], default='draft')
    property_ids=fields.One2many('property.property','owner_id')
    def action_draft(self):
        for rec in self:
            rec.state='draft'
    def action_pending(self):
        for rec in self:
            rec . state='pending'
    def action_sold(self):
        for rec in self:
            rec .state='sold'
    def action_closed(self):
        for rec in self:
            rec.state='close'
    @api.model
    def create(self,vals):
        result=super(Owner,self).create(vals)
        if result.ref=='New':
             result.ref= self.env['ir.sequence'].next_by_code('owner_seq')
             return result
        