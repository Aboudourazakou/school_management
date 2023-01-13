from odoo import models,fields

class tuteur(models.Model):
    _name="tuteur"
    
    _inherit = ['personne']
    id_tuteur=fields.Integer("Id du parent"),
    
    etudiant_ids = fields.One2many(
        string='etudiants',
        comodel_name='etudiant',
        inverse_name='id_etudiant',
    )
    

    