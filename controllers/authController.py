

from odoo import http,models
from odoo.http import request;
import json
import datetime

import base64

class authentication(http.Controller):
    _inherit = "event.event"
    
    @http.route('/school_management/getloginform', website='True', type='http', auth="public")
    def getform(self, **kw):
      
      
        return http.request.render('school_management.login',{})

    
    @http.route('/school_management/login', website='True', type='http', auth="public",csrf=False)
    def giveAccessToUser(self, **kw):
        
         compte=[]
         if request.params.get('login'):
          
             compte = request.env['compte'].search(['&',('login','=', kw.get("login")),('password','=',kw.get('password'))],limit=1)
         elif request.params.get('cle_secrete'):
              compte = request.env['compte'].search([('cle_secrete','=', kw.get("cle_secrete"))],limit=1)
         if(len(compte)==0):
           return request.redirect('/school_management/getloginform?error=1')
    

         else:
            request.session['login']=compte.login
            request.session['password']=compte.password
           
        
            return  request.redirect('/school_management/accueil')
    @http.route('/school_management/logout', website='True', type='http', auth="public",csrf=False)
    def logout_user(self,**kw):
          request.session.pop('login')
          return request.redirect('/school_management/getloginform')




 

 

