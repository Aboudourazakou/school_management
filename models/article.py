from odoo import models,fields

class article(models.Model):
    _name="article"
    
  
    attachement_id = fields.Integer("ID Attachement")
    file=fields.Binary("Fichier attache")
    
    message = fields.Char(
        string='message',
    )
    
    enseignant_id = fields.Many2one(
        string='enseignant',
        comodel_name='enseignant',
        ondelete='restrict',
    )

    date_publication = fields.Datetime(
        string='date_publication',
        default=fields.Datetime.now,
    )
    
    