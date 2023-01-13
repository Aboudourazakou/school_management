
from odoo import http,models
from odoo.http import request;
import json
import datetime

import base64

class  main(http.Controller):
    
    _inherit = "event.event"
    def redirectUserToPreviousPage():
         return {
                'type': 'ir.actions.act_url',
                'url': '/school_management/getloginform?error=1',
                'target': 'self',
                }
          
  
    @http.route('/school_management/accueil', website='True', type='http', auth="public",csrf=False)
    def go_home_page(self,**kw):
        
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

            
            articles=request.env['article'].search([('enseignant_id','=',compte.enseignant_id.id)])
            devoirs=request.env['devoir'].search([('matiere_id.enseignant_id.name','=',compte.enseignant_id.name)])
            matieres=request.env['matiere'].search([('enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
            niveaux=request.env['niveau'].search([('matiere_ids.enseignant_id.id','=',compte.enseignant_id.id)])
            return http.request.render('school_management.home',{'user':person,'devoirs':devoirs,'nbrDev':len(devoirs),"matieres":matieres,"niveaux":niveaux,"nbreMatieres":len(matieres),"nbreNiveaux":len(niveaux),"articles":len(articles)})
            

        elif compte.etudiant_id.name is not False and compte.etudiant_id.prenom is not False:
           person={
              "id":compte.etudiant_id.id,
              "nom":compte.etudiant_id.name,
              "prenom":compte.etudiant_id.prenom,
              "email":compte.etudiant_id.email,
              "telephone":compte.etudiant_id.telephone,
              "type":"etudiant",

            }
           
           les_devoirs=request.env['devoir'].search([('niveau_id.name','=',compte.etudiant_id.niveau_id.name)])
           devoirs=[]
           for devoir in les_devoirs:
             diff=devoir.date_delai-devoir.date_publication
             devoir.jour_restant=diff.days
             devoirs.append(devoir)

           realisations=request.env['realisation'].search([('etudiant_id','=',compte.etudiant_id.id)])
           niveau=request.env['niveau'].search([('id','=',compte.etudiant_id.niveau_id.id)])

           devoirs_utilisateur=[]
           
           for devoir in devoirs:
            find=False
            devoir["soumis"]=False
          
            for realisation in realisations:
              if(devoir.id==realisation.devoir_id.id):
                find=True
                break
            if(find):
              devoir["soumis"]=True
              
            devoirs_utilisateur.append(devoir)

            
              
           matieres=request.env['matiere'].search([('niveau_ids.id','=',compte.etudiant_id.niveau_id.id)])
           seance=request.env['seance'].search([('niveau_id','=',compte.etudiant_id.niveau_id.id)])
           participations=request.env['participation'].search([('id_etudiant','=',compte.etudiant_id.id)])
           return http.request.render('school_management.home',{'user':person,'devoirs':devoirs_utilisateur,'nbrDev':len(devoirs),"soumis":len(realisations),"nonsoumis":len(devoirs)-len(realisations),"absence":len(seance)-len(participations),"matieres":matieres,"niveau":niveau})
         

       
        if(len(compte)==0):
            request.session.pop('login')
            return request.redirect('/school_management/getloginform')

       



   
          
    
   
  
    