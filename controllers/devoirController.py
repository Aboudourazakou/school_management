from odoo import http,models
from odoo.http import request;
import json
import datetime

import base64




class devoirController(http.Controller):
    _inherit = "event.event"


    @http.route('/school_management/publish/devoir',website='True', type='http', auth="public",csrf=False)
    def publish_devoir(self,**kw):
          Attachments = request.env['ir.attachment']
          attachment = kw['file'].read()
          niveau=request.env['niveau'].search([('id','=',kw["niveau_id"])],limit=1)
          
          form_data={
            
            "date_delai":kw['date_delai'].replace('T',' '),
            "file":base64.encodebytes(attachment),
            "matiere_id":kw["matiere_id"],
            "niveau_id":kw["niveau_id"],
            "libelle":kw["libelle"],
            "message":kw["message"],
            "count_etudiant":len(niveau.etudiants_ids)
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
          request.env['devoir'].sudo().create(form_data)
          return request.redirect('/school_management/accueil')
    @http.route('/school_management/devoirs', website='True', type='http', auth="public",csrf=False)
    def go_devoir_page(self,**kw):

        compte= request.env['compte'].search([('login','=', request.session.get('login'))])
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
  
        return http.request.render('school_management.devoirs',{'user':person,"matieres":matieres,"niveaux":niveaux,'nbrDev':len(devoirs),"matieres":matieres,"niveaux":niveaux,"nbreMatieres":len(matieres),"nbreNiveaux":len(niveaux),"articles":len(articles)})


    

    @http.route('/school_management/submit/devoir/form', website='True', type='http', auth="public",csrf=False)
    def get_submit_devoir_form(self,**kw):
      
        compte= request.env['compte'].search([('login','=', request.session.get('login'))])
        devoirs=request.env['devoir'].search([('niveau_id.name','=',compte.etudiant_id.niveau_id.name)])
        matieres=request.env['matiere'].search([('niveau_ids.id','=',compte.etudiant_id.niveau_id.id)])
        niveau=request.env['niveau'].search([('id','=',compte.etudiant_id.niveau_id.id)],limit=1)


       
        person={
              "id":compte.etudiant_id.id,
              "nom":compte.etudiant_id.name,
              "prenom":compte.etudiant_id.prenom,
              "email":compte.etudiant_id.email,
              "telephone":compte.etudiant_id.telephone,
              "type":"etudiant",

            }
        return http.request.render('school_management.submit_devoir',{'user':person,"devoirs":devoirs,"matieres":matieres,"niveau":niveau})

    @http.route('/school_management/submit/devoir', website='True', type='http', auth="public",csrf=False)
    def submit_devoir_form(self,**kw):
          Attachments = request.env['ir.attachment']
          attachment = kw['file'].read()
          compte= request.env['compte'].search([('login','=', request.session.get('login'))])
          form_data={
            "etudiant_id":compte.etudiant_id.id,
            "devoir_id":kw["devoir_id"],
           
          }
          devoir = request.env['devoir'].browse(int(kw["devoir_id"]))
          devoir.write({'count_realisation': devoir.count_realisation+1})
          name = kw.get('file').filename
          attachment_id = Attachments.sudo().create({
            'name':name,
            'res_name': name,
            'type': 'binary',   
            'res_id': form_data.get('id_devoir'),
            'datas': base64.encodebytes(attachment),
          })
          form_data['attachment_id'] = attachment_id
          request.env['realisation'].sudo().create(form_data)
          return request.redirect('/school_management/submit/devoir/form?success=1')

    @http.route('/school_management/devoirs/soumis', website='True', type='http', auth="public",csrf=False)
    def get_devoirs_soumis(self,**kw):
      realisations=request.env['realisation'].search([('etudiant_id','=',request.params.get("etudiant"))])
      compte= request.env['compte'].search([('login','=', request.session.get('login'))])
      matieres=request.env['matiere'].search([('niveau_ids.id','=',compte.etudiant_id.niveau_id.id)])
      niveau=request.env['niveau'].search([('id','=',compte.etudiant_id.niveau_id.id)],limit=1)


      person={
              "id":compte.etudiant_id.id,
              "nom":compte.etudiant_id.name,
              "prenom":compte.etudiant_id.prenom,
              "email":compte.etudiant_id.email,
              "telephone":compte.etudiant_id.telephone,
              "type":"etudiant",

            }
      tri_realisation=[]
      for realisation in realisations:
         devoir=request.env['devoir'].search([('id','=',realisation.devoir_id.id)],limit=1)
         etudiant=request.env['etudiant'].search([('id','=',request.params.get("etudiant"))],limit=1)
         val=request.params.get("matiere")
         if(devoir.matiere_id.id==int(val)):
          
          real={
            "etudiant":etudiant.name+" "+etudiant.prenom,
            "date_soumission":realisation.date,
            "libelle_devoir":devoir.libelle,
            "delai_soumission":devoir.date_delai,
            "enseignant":devoir.matiere_id.enseignant_id.name+" "+devoir.matiere_id.enseignant_id.prenom,
            "attachment_id":realisation.attachment_id,
            
          }
          tri_realisation.append(real)
      
      return http.request.render('school_management.devoirs_soumis',{'user':person,"realisations":tri_realisation,"matieres":matieres,"niveau":niveau
      })


    @http.route('/school_management/etudiants/soumis/devoirs',website='True', type='http', auth="public",csrf=False)
    def get_etudiants_ayant_soumis_devoir(self,**kw):

      devoir=request.env['devoir'].search([('id','=',request.params.get('id'))],limit=1)
      etudiants=request.env['etudiant'].search([('niveau_id.id','=',devoir.niveau_id.id)])
      results=[]
      for etudiant in etudiants:
        realisation=request.env['realisation'].search(['&',('devoir_id.id','=',request.params.get('id')),('etudiant_id','=',etudiant.id)])
        if len(realisation)!=0:
          res={
            "nom":etudiant.name,
            "prenom":etudiant.prenom,
            "telephone":etudiant.telephone,
            'email':etudiant.email,
            "niveau":etudiant.niveau_id.name,
            "matiere":devoir.matiere_id.libelle,
            "echeance":devoir.date_delai,
            "date_soumis":realisation.date,
            "attachment":realisation.attachment_id
          }

          results.append(res)


      compte= request.env['compte'].search([('login','=', request.session.get('login'))])
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
            devoirs=request.env['devoir'].search([('matiere_id.enseignant_id.name','=',compte.enseignant_id.name)])
            matieres=request.env['matiere'].search([('enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
            niveaux=request.env['niveau'].search([('matiere_ids.enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
            return http.request.render('school_management.etudiants_ayant_soumis',{'user':person,'devoirs':devoirs,'nbrDev':len(devoirs),"matieres":matieres,"niveaux":niveaux,"nbreMatieres":len(matieres),"nbreNiveaux":len(niveaux),"results":results,"etudiants":etudiants})
            


    @http.route('/school_management/etudiants/nonsoumis/devoirs',website='True', type='http', auth="public",csrf=False)
    def get_etudiants_nayant_pas_soumis_devoir(self,**kw):

      devoir=request.env['devoir'].search([('id','=',request.params.get('id'))],
      limit=1
      )
      etudiants=request.env['etudiant'].search([('niveau_id.id','=',devoir.niveau_id.id)])
      results=[]
      
      for etudiant in etudiants:
        

        realisation=request.env['realisation'].search(['&',('devoir_id.id','=',request.params.get('id')),('etudiant_id','=',etudiant.id)])
        if len(realisation)==0:
          res={
           
            "nom":etudiant.name,
            "prenom":etudiant.prenom,
            "telephone":etudiant.telephone,
            'email':etudiant.email,
            "niveau":etudiant.niveau_id.name,
            "matiere":devoir.matiere_id.libelle,
            "echeance":devoir.date_delai,
           
          
          }

          results.append(res)


      compte= request.env['compte'].search([('login','=', request.session.get('login'))])
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
            devoirs=request.env['devoir'].search([('matiere_id.enseignant_id.name','=',compte.enseignant_id.name)])
            matieres=request.env['matiere'].search([('enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
            niveaux=request.env['niveau'].search([('matiere_ids.enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
            return http.request.render('school_management.etudiants_nayant_pas_soumis',{'user':person,'devoirs':devoirs,'nbrDev':len(devoirs),"matieres":matieres,"niveaux":niveaux,"nbreMatieres":len(matieres),"nbreNiveaux":len(niveaux),"results":results})
            


    @http.route('/school_management/get_create_seance_form', website='True', type='http', auth="public",csrf=False)
    def create_seance_form(self,**kw):
        compte= request.env['compte'].search([('login','=', request.session.get('login'))])
        matieres=request.env['matiere'].search([('enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
        niveaux=request.env['niveau'].search([('matiere_ids.enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
        articles_published=request.env['article'].search([('enseignant_id','=',compte.enseignant_id.id)])
       
        person={
              "nom":compte.enseignant_id.name,
              "prenom":compte.enseignant_id.prenom,
              "email":compte.enseignant_id.email,
              "telephone":compte.enseignant_id.telephone,
              "matricule":compte.enseignant_id.matricule,
              "type":"enseignant",

            }
        devoirs=request.env['devoir'].search([('matiere_id.enseignant_id.name','=',compte.enseignant_id.name)])
       
        return http.request.render('school_management.create_seance',{'user':person,"matieres":matieres,"niveaux":niveaux,"matieres":matieres,"niveaux":niveaux,"nbreMatieres":len(matieres),"nbreNiveaux":len(niveaux),"articles":len(articles_published),'nbrDev':len(devoirs)})

  

    
    






     


  
    
  
         
         
    
    

         

   
    
