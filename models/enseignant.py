from odoo import models,fields

class enseignant(models.Model):
    _name="enseignant"
    
    _inherit = ['personne']
    id_enseignant=fields.Integer("Id de l'enseignant")
    matricule=fields.Char("Matricule du prof")
    
    matiere_ids = fields.One2many(
        string='matiere',
        comodel_name='matiere',
        inverse_name='id_matiere',
    )
    
    