from odoo import models,fields

class Seance(models.Model):
    _name="seance"
    
    date = fields.Datetime(
        string='date',
        default=fields.Datetime.now,
    )
    nom=fields.Char("Nom de la seance")
    niveau_id=fields.Integer("Niveau")

    
    matiere_id = fields.Many2one(
        string='matiere',
        comodel_name='matiere',
        ondelete='restrict',
    )
    