from odoo import models,fields

class Participation(models.Model):
  _name="participation"
  id_etudiant=fields.Integer("Id de l'etudiant")
  
  id_seance = fields.Many2one(
      string='seance',
      comodel_name='seance',
      ondelete='restrict',
  )
  