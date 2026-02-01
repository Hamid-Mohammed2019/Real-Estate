from odoo import models ,fields,api 
from odoo.exceptions import ValidationError
class Property(models.Model):
     _name='property.property'
     _description='property record'
     _rec_name='Name'
     _inherit=['mail.thread','mail.activity.mixin']
     ref=fields.Char(default='New' ,readonly=True)
     Name=fields.Char(string='name property ', required=True ,size=10   )
     postCode=fields.Char(string='postCode')
     description=fields.Text(string='description')
     date_avilable=fields.Date(string='date_avilable')
     sealing_price=fields.Float(string='sealing_price')
     expted_sealing_date=fields.Date()
     is_late=fields.Boolean()
     expted_price=fields.Float(string='expted_price')
     bedrom= fields.Integer(string='bedrom')
     bathroom=fields.Integer(string='bathroom')
     living_area= fields.Integer(string='living_area') 
     facades  =fields.Integer(string='facades')
     garden=fields.Boolean()
     grach =fields.Boolean(string='grach') 
     garden_area =fields.Integer(string='garden_area')
     garden_dir =fields.Selection([
        ['north','North'],
        ['east','East'],
        ['west','West'],
        ['south','South'],
    ],default='north')
     property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('land', 'Land')
    ], required=True)
     images=fields.Binary(string='image of property')
     address=fields.Char(string='address property')
     state = fields.Selection([
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('rented', 'Rented'),
        ('sold', 'Sold'),
    ], default='available')

     line_ids=fields.One2many('property.line','property_id')
     owner_id=fields.Many2one('owner.owner')
    #  address=fields.Char(related='owner_id.address')
     phone=fields.Char(related='owner_id.phone')
    #  sql constrains
     sql_constrains=[('unique_name','unique(Name)','the name of property must be unique')]
    #  valdition to check bed rom grater than zero
     @api.constrains('bedrom')
     def _check_bedrom_grater_zero(self):
      for rec in self:
          if rec.bedrom==0:
              raise ValidationError(' place add valid number')
    # create record in database with 
     @api.model
     def create(self,vals):
         if vals.get('expted_price') > vals.get('sealing_price'):
             raise ValidationError('expted price cannot be grater sealing_price')
         return super(Property,self).create(vals)
     
     def action_draft(self):
         for rec in self:
             rec.create_record_history(rec.state,'draft')
             rec.state ='draft'
     def action_pending(self):
         for rec in self:
          rec.create_record_history(rec.state,'pending')
          rec.state='pending' 
 
     def action_Sold(self):
        for rec in self:
            rec.create_record_history(rec.state,'sold')
            rec.state='Sold' 
     def action_closed(self):
         for rec in self:
             rec.create_record_history(rec.state,'close')
             rec.state='close'
         
    #    #cron jop
     def check_expted_sealing_date(self):
         property_ids=self.search([])
         for rec in property_ids:
              if rec.expted_sealing_date and rec.expted_sealing_date < fields.date.today():
                 rec. is_late=True
             
        #genrate sequence property record
     def create(self,vals):
          result=super(Property,self).create(vals)
          if result.ref == 'New':
             result.ref= self.env['ir.sequence'].next_by_code('property_seq')
             return result
     def create_record_history(self,old_state, new_state):
       for rec in self:
        rec.env['property.heistery'].create({
            'user_id': rec.env.user.id,
            'property_id': rec.id,
            'old_state': old_state,
            'new_state': new_state,
        })
        
     active=fields.Boolean(default='active')
     def action_open_change_state_wizard(self):
  
          action = self.env['ir.actions.actions']._for_xml_id(
        'Real_estate.change_state_wizard_action' )
          action['context'] = { 'default_property_id': self.id
    }
          return action
      
    


#line property  
class propertyline (models.Model):
    _name='property.line'
    property_id=fields.Many2one('property.property')
    area=fields.Float()
    description=fields.Char()
        


     