from odoo import models,fields

class devoir(models.Model):
   


    _name="devoir"

   
    
   

    id_devoir=fields.Integer("Id niveau",
    default=lambda self: self.env['ir.sequence'].next_by_code('increment_your_field'))
    libelle=fields.Char("Libelle du devoir")
    date_delai=fields.Datetime("Date d'echeance")
    file=fields.Binary("Fichier attache")
    attachement_id = fields.Integer("ID Attachement")
    file_id = fields.Integer(
        string='file_id',
    )
    
    message=fields.Char("message")
   
    date_publication = fields.Datetime(
        string='date_publication',
        default=fields.Datetime.now,
    )
    
    
    niveau_id = fields.Many2one(
        string='niveau',
        comodel_name='niveau',
       
    )

    

    realisation_ids = fields.One2many('realisation', 'devoir_id', string='Realisations')

   
    
    count_realisation =  fields.Integer(string='Devoirs soumis')
   
    
    
    #def _compute_realisation_ids(self):
    #    for record in self:
           
    #      record.count_realisation =len(self.env['realisation'].search([('devoir_id', '=', record.id)]))

    count_etudiant = fields.Integer(
        string='etudiants total',
        default=0
        
    )
    matiere_id = fields.Many2one('matiere', string='matiere')
    soumis = fields.Boolean(
        string='soumis',
        
        default=False
        
    )

    jour_restant = fields.Integer(
        
        default=0
        
    )
    
   
    
    
    