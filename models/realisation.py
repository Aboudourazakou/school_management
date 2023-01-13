from odoo import models,fields

class realisation(models.Model):
    _name="realisation"
    etudiant_id=fields.Integer("Id de l'etudiant")
    attachment_id=fields.Integer("Id de l'attachement")
    
    devoir_id = fields.Many2one(
        string='devoir',
        comodel_name='devoir',
        ondelete='restrict',
    )
    
    
    date = fields.Datetime(
        string='date',
        default=fields.Datetime.now,
    )
    