from odoo import models,fields

class etudiant(models.Model):
    _name="etudiant"
    
    _inherit = ['personne']
    id_etudiant=fields.Integer(readonly=True)
  
    age=fields.Integer("Age")
    
    niveau_id = fields.Many2one(
        string='niveau',
        comodel_name='niveau',
       
    )
    presence=fields.Integer("")
    
    
    tuteur_id = fields.Many2one(
        string='tuteur',
        comodel_name='tuteur',
        ondelete='restrict',
    )

    
    