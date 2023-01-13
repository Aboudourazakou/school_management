
from odoo import models,fields

class personne(models.Model):
    _name="personne"
    name=fields.Char("Nom",required=True)
    prenom=fields.Char("Prenom",required=True)
    telephone=fields.Char("Telephone")
    email=fields.Char("Email")
    photo=fields.Binary(string="Photo de profile",max_width=10,max_height=10)
    
    compte_ids = fields.One2many(
        string='compte',
        comodel_name='compte',
        inverse_name='id_compte',
    )
    