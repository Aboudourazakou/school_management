from odoo import models,fields

class compte(models.Model):
    _name="compte"
   
    
   
    id_compte = fields.Integer(
        string='id_compte',
    )
    
    password = fields.Char(
        string='password',
    )

    
    login = fields.Char(
        string='login',
    )

    
   
    enseignant_id = fields.Many2one(
        string='enseignant',
        comodel_name='enseignant',
        ondelete='restrict',
    )
    etudiant_id = fields.Many2one(
        string='etudiant',
        comodel_name='etudiant',
        ondelete='restrict',
    )
    cle_secrete=fields.Char("Cle secrete")
    
    
    
    
    
    

  
    