from odoo import models,fields
from odoo import api

class niveau(models.Model):
    _name="niveau"
    

    id_niveau=fields.Integer("Id niveau",
    default=lambda self: self.env['ir.sequence'].next_by_code('increment_your_field'))
    name=fields.Char("Nom du niveau")
    matiere_ids = fields.Many2many(
        string='matieres',
        comodel_name='matiere',
        relation='matiere_niveau_rel',
        column1='id_matiere',
        column2='id_niveau',
    )
    
    devoir_ids = fields.One2many(
        string='devoirs',
        comodel_name='devoir',
        inverse_name='id_devoir',
    )
    
    etudiants_ids = fields.One2many(
        string='etudiants',
        comodel_name='etudiant',
        inverse_name='id_etudiant',
        
    )

    etudiants_count = fields.Integer(default=2)
   # fields.Integer(string='etudiant count', compute='_compute_student_count')
    
   # @api.depends('etudiants_ids')
   # def _compute_student_count(self):
   #     for record in self:
   #         record.etudiants_count = len(record.etudiants_ids)
    
    
    
    