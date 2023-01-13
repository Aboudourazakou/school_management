
from odoo import http,models
from odoo.http import request;
import json
import datetime

import base64




class articleController(http.Controller):
    _inherit = "event.event"
    
#Publier article
    @http.route('/school_management/publish/article', website='True', type='http', auth="public",csrf=False)
    def get_publish_devoir_form(self,**kw):
       compte= request.env['compte'].search([('login','=', request.session.get('login'))],limit=1)
       matieres=request.env['matiere'].search([('enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
       niveaux=request.env['niveau'].search([('matiere_ids.enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
       devoirs=request.env['devoir'].search([('matiere_id.enseignant_id.name','=',compte.enseignant_id.name)])
       articles=request.env['article'].search([])
    
    

       
       person={
              "nom":compte.enseignant_id.name,
              "prenom":compte.enseignant_id.prenom,
              "email":compte.enseignant_id.email,
              "telephone":compte.enseignant_id.telephone,
              "matricule":compte.enseignant_id.matricule,
              "type":"enseignant",

            }
       return http.request.render('school_management.publish_article',{'user':person,"matieres":matieres,"niveaux":niveaux,'devoirs':devoirs,'nbrDev':len(devoirs),"matieres":matieres,"niveaux":niveaux,"nbreMatieres":len(matieres),"nbreNiveaux":len(niveaux),"articles":len(articles)})

    @http.route('/school_management/submit/article', website='True', type='http', auth="public",csrf=False)
    def submit_article(self,**kw):
      compte= request.env['compte'].search([('login','=', request.session.get('login'))],limit=1)
      Attachments = request.env['ir.attachment']
      attachment = kw['file'].read()

      form_data={
        "message":kw['message'],
        'enseignant_id':compte.enseignant_id.id,
        "file":base64.encodebytes(attachment),
      }

      name = kw.get('file').filename
      attachment_id = Attachments.sudo().create({
            'name':name,
            'res_name': name,
            'type': 'binary',   
            'res_id': form_data.get('id_devoir'),
            'datas': base64.encodebytes(attachment),
          })
      form_data['attachement_id'] = attachment_id
      request.env['article'].sudo().create(form_data)
      return request.redirect('/school_management/accueil')

    @http.route('/school_management/list/articles', website='True', type='http', auth="public",csrf=False)
    def list_articles(self,**kw):
        
        compte= request.env['compte'].search([('login','=', request.session.get('login'))],limit=1)
        if compte.enseignant_id.name is not False and compte.enseignant_id.prenom is not False:
            person={
              "id":compte.enseignant_id.id,
              "nom":compte.enseignant_id.name,
              "prenom":compte.enseignant_id.prenom,
              "email":compte.enseignant_id.email,
              "telephone":compte.enseignant_id.telephone,
              "matricule":compte.enseignant_id.matricule,
              "type":"enseignant",

            }
            articles=request.env['article'].search([])
            articles_published=request.env['article'].search([('enseignant_id','=',compte.enseignant_id.id)])
            devoirs=request.env['devoir'].search([('matiere_id.enseignant_id.name','=',compte.enseignant_id.name)])
            matieres=request.env['matiere'].search([('enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
            niveaux=request.env['niveau'].search([('matiere_ids.enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
            return http.request.render('school_management.list_articles',{'user':person,'devoirs':devoirs,'nbrDev':len(devoirs),"matieres":matieres,"niveaux":niveaux,"nbreMatieres":len(matieres),"nbreNiveaux":len(niveaux),"articles":articles,"article_published":len(articles_published)})
            
#End publier article
