from odoo import models,fields

class matiere(models.Model):
    _name="matiere"
    
    id_matiere=fields.Integer("Id de la matiere",
    default=lambda self: self.env['ir.sequence'].next_by_code('increment_your_field'))
    libelle=fields.Char("Libelle de la matiere")
    enseignant_id = fields.Many2one(
        string='enseignant',
        comodel_name='enseignant',
        ondelete='restrict',
    )

    niveau_ids = fields.Many2many(
        string='niveaux',
        comodel_name='niveau',
        relation='niveau_matiere_rel',
        column1='id_niveau',
        column2='id_matiere',
    )
    
    
    