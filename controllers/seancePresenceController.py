
from odoo import http,models
from odoo.http import request;
import json
import datetime

import base64

class seancePresenceController(http.Controller):
    _inherit = "event.event"

    @http.route('/school_management/create/seance', website='True', type='http', auth="public",csrf=False)
    def create_seance(self,**kw):
         form_data={
          'matiere_id':kw['matiere_id'],
          'nom':kw['nom'],
          'niveau_id':kw['niveau_id']
         }
         request.env['seance'].sudo().create(form_data)
      
         request.session['niveau']=kw['niveau_id']
         request.session['matiere']=kw['matiere_id']
         request.session['seance']= request.env['seance'].search([])[-1].id
         return request.redirect('/school_management/presences')
      
    @http.route('/school_management/valider_presence', website='True', type='http', auth="public",csrf=False)
    def valider_inscription(self,**kw):
      try:request.session.pop('alreadymarked')
      except:print('')
      participation=request.env['participation'].search(['&',('id_etudiant','=',kw['id_etudiant']),('id_seance.id','=',kw['id_seance'])])
    
         
      if(participation.id_etudiant==0):request.env['participation'].sudo().create(kw)
      else:  request.session['alreadymarked']=1
      return request.redirect('/school_management/presences')
    
    
    @http.route('/school_management/presences', website='True', type='http', auth="public",csrf=False)
    def check_presence(self,**kw):
      compte= request.env['compte'].search([('login','=', request.session.get('login'))])
      person={
              "nom":compte.enseignant_id.name,
              "prenom":compte.enseignant_id.prenom,
              "email":compte.enseignant_id.email,
              "telephone":compte.enseignant_id.telephone,
              "matricule":compte.enseignant_id.matricule,
              "type":"enseignant",

            }
      try:
         duplication_check=request.session['alreadymarked']
      except:
          duplication_check=False
      try:request.session.pop('alreadymarked')
      except:print("")
      etudiants=  request.env['etudiant'].search([('niveau_id.id_niveau','=',request.session['niveau'])])
      nbreSeance=request.env['seance'].search([('niveau_id','=',request.session['niveau'])])
      seance=request.env['seance'].search([('id','=',request.session['seance'])])
      matiere=request.env['matiere'].search([('id_matiere','=',request.session['matiere'])])
      students=[]
      for etudiant in  etudiants:
        student=etudiant
        
        student.presence= len(nbreSeance)-len(request.env['participation'].search(['&',('id_etudiant','=',etudiant.id),('id_seance.matiere_id.id_matiere','=',matiere.id_matiere)]))-1
        if(student.presence<0): student.presence=0
        students.append(student)
      
      return request.render("school_management.seance_presences",{'user':person,'etudiants':students,'seance':seance,'matiere':matiere.libelle,'nbreSeance':len(nbreSeance)-1,'duplication_check':duplication_check})

    @http.route('/school_management/presence-par-niveau', website='True', type='http', auth="public",csrf=False)
    def check_presence_by_niveau(self,**kw):
      compte= request.env['compte'].search([('login','=', request.session.get('login'))])
      person={
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
      niveaux=request.env['niveau'].search([('matiere_ids.enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
    
      etudiants=  request.env['etudiant'].search([('niveau_id.id_niveau','=',request.params.get('niveau'))])
      seance=request.env['seance'].search([('niveau_id','=',request.params.get('niveau'))])
    
      students=[]
      for etudiant in  etudiants:
        student=etudiant
        
        student.presence= len(seance)-len(request.env['participation'].search([('id_etudiant','=',etudiant.id)]))
        students.append(student)
      
      return request.render("school_management.list_presences",{'user':person,'etudiants':students,'seance':seance,'nbreSeance':len(seance)-1,'nbrDev':len(devoirs),"matieres":matieres,"niveaux":niveaux,"nbreMatieres":len(matieres),"nbreNiveaux":len(niveaux),"articles":len(articles)})

    
    @http.route('/school_management/presences-par-seance', website='True', type='http', auth="public",csrf=False)
    def get_presences_absences_par_seances(self,**kw):

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
      presences=[]
      etudiant=request.env['etudiant'].search([("id",'=',request.params.get("etudiant"))])
      seances=request.env['seance'].search([('niveau_id','=',etudiant.niveau_id.id)])
      for seance in seances:
        participation=request.env['participation'].search(['&',('id_seance','=',seance.id),('id_etudiant','=',etudiant.id)])
        if(len(participation)==0):
          res={
            "libelle":seance.nom,
            "presence":"non",
            "date":seance.date,
          }
          presences.append(res)
        else: 
          res={
            "libelle":seance.nom,
            "presence":"oui",
            "date":seance.date,
          }
          presences.append(res)
        
      articles_published=request.env['article'].search([('enseignant_id','=',compte.enseignant_id.id)])
      devoirs=request.env['devoir'].search([('matiere_id.enseignant_id.name','=',compte.enseignant_id.name)])
      matieres=request.env['matiere'].search([('enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
      niveaux=request.env['niveau'].search([('matiere_ids.enseignant_id.id_enseignant','=',compte.enseignant_id.id_enseignant)])
      return http.request.render('school_management.absences_ou_presences_par_seances',{'user':person,'devoirs':devoirs,'nbrDev':len(devoirs),"matieres":matieres,"niveaux":niveaux,"nbreMatieres":len(matieres),"nbreNiveaux":len(niveaux),'presences':presences,"etudiant":etudiant,"articles":len(articles_published)})


    @http.route('/school_management/etudiant/absence-par-matiere', website='True', type='http', auth="public",csrf=False)
    def get_absences_par_matiere(self,**kw):
      id_etu=int(request.params.get("etudiant"))
      id_mat=int(request.params.get('matiere'))
      etudiant=request.env['etudiant'].search([('id','=',id_etu)])
      seances=request.env['seance'].search(['&',('niveau_id','=',etudiant.niveau_id.id),('matiere_id.id','=',id_mat)])
       
      matieres=request.env['matiere'].search([('niveau_ids.id','=',etudiant.niveau_id.id)])
      nom_matiere=request.env['matiere'].search([('id','=',id_mat)])
    
      person={
              "id":etudiant.id,
              "nom":etudiant.name,
              "prenom":etudiant.prenom,
              "email":etudiant.email,
              "telephone":etudiant.telephone,
              "type":"etudiant",

            }
      presences=[]
      for seance in seances:
        participation=request.env['participation'].search(['&',('id_seance','=',seance.id),('id_etudiant','=',etudiant.id)])
        if(len(participation)==0):
          res={
            "libelle":seance.nom,
            "presence":"non",
            "date":seance.date,
          }
          presences.append(res)
        else: 
          res={
            "libelle":seance.nom,
            "presence":"oui",
            "date":seance.date,
          }
          presences.append(res)

      return http.request.render('school_management.absences_par_matiere',{'user':person,"matieres":matieres,"nbreMatieres":len(matieres),'presences':presences,"etudiant":etudiant,"presences":presences,"module":nom_matiere.libelle})





