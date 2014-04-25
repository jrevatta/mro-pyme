#script para el administrador

import os
import webapp2
import jinja2
import logging
import cgi
import Crypto.Hash.MD5 as MD5

from google.appengine.ext import db
from google.appengine.ext import ndb
from opmodel import *

#inicializar jinja2

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

version = '0.9'
loginpage = 'http://localhost:9080/profile'

#generic function
def global_printmensaje(cls, name_template, mensaje, path):
            template = jinja_environment.get_template(name_template)
            cls.response.out.write(template.render({'version':version, 'empresa':'Pyme', 'mensaje':mensaje, 'path':''}))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        registros = Usuario.query().fetch(1) 
        if registros:
                global_printmensaje(self,'t_adm_login.html','Ingrese su usuario y clave','')
        else:
            #Primer registro de usuario en el administrador. Solo se ejecuta mientras no exista ningun registro en la BD.
            global_printmensaje(self,'t_adm_first_profile.html','Registre sus datos','')


class MenuHandler(webapp2.RequestHandler):
    
    def printmensaje(self, name_template, mensaje):
            template = jinja_environment.get_template(name_template)
            self.response.out.write(template.render({'version':version, 'empresa':'Pyme', 'mensaje':mensaje, 'path':'../'}))
            
    def printusuario(self, name_template, usuario):
            template = jinja_environment.get_template(name_template)
            self.response.out.write(template.render({'version':version, 'empresa':'Pyme', 'usuario':usuario, 'path':'../'}))
            
    def printprofile(self,name_template, usuario, values):
            template = jinja_environment.get_template(name_template)
            strvalues = {'val1':'', 'val2':'', 'val3':''}
            for x in range(1,4):
                indice = 'val' + str(x)
                if values[indice] == True:
                    strvalues[indice] = 'checked'
                    
            self.response.out.write(template.render({'version':version, 'empresa':'Pyme', 'usuario':usuario, 'path':'../', 'val1': strvalues['val3'], 'val2':strvalues['val2'], 'val3':strvalues['val1']})) 
            
    def post(self):
        usuario = cgi.escape(self.request.get('usuario'))
        password = cgi.escape(self.request.get('password'))
        
        destino_login = 't_adm_login.html'
        
        if (len(usuario) > 0) and (len(password) > 0):
            
            usuarios = Usuario.query().filter(ndb.GenericProperty('usuario') == usuario).fetch(1)

            
            if usuarios:              
                for element in usuarios:                    
                    if element.usuario == usuario:                        
                        n_hash = MD5.new(password).hexdigest()                       
                        if element.clave == n_hash:                           
                            if element.rol == 'rol04':
                                #ToDo: Leer los usuarios registrados
                                self.printusuario('t_adm_profile.html', usuario)                                
                            elif element.rol =='rol02' or element.rol =='rol03':
                                    values = {'val1':False, 'val2': False, 'val3': False}
                                    permisos = Profile.query().filter(ndb.GenericProperty('usuario') == usuario).fetch(1)
                                    if permisos:
                                        for ele in permisos:
 
                                            if ele.usuario == usuario:
                                                values['val1'] = ele.operaciones
                                                values['val2'] = ele.inventario
                                                values['val3'] = ele.reportes                                                
                                                self.printprofile('t_adm_profile_rol.html', usuario, values)
                                            else:
                                                self.printprofile('t_adm_profile_rol.html', usuario, values)
                                    else:
                                        self.printprofile('t_adm_profile_rol.html', usuario, values)
                            else:                                
                                self.printmensaje(destino_login,'su usuario no tiene permisos en esta seccion')
                        else:                            
                            self.printmensaje(destino_login,'clave incorrecta')
                    else:                        
                        self.printmensaje(destino_login,'usuario no registrado')
            else:                
                self.printmensaje(destino_login,'usuario no existe')
        else:            
            self.printmensaje(destino_login,'ingrese usuario y password')
 
            
class ProfileHandler(webapp2.RequestHandler):
        
    def updateprofile(self, usuario, opciones):
        respuesta = False              
        if len(usuario) > 0:
            profile = Profile.query().filter(ndb.GenericProperty('usuario') == usuario).fetch(1)
            if profile:
                for element in profile:
                    if element.usuario == usuario:
                        element.operaciones = opciones['val1']
                        element.inventario = opciones['val2']
                        element.reportes = opciones['val3']
                        element.put()
                        respuesta = True
            else:
                element = Profile(usuario = usuario, operaciones = opciones['val1'], inventario = opciones['val2'], reportes = opciones['val3'])
                element.put()
                respuesta = True
        return respuesta

    def printmensaje(self, name_template, mensaje):
            template = jinja_environment.get_template(name_template)
            self.response.out.write(template.render({'version':version, 'empresa':'Pyme', 'mensaje':mensaje, 'path':'../'}))

    
    def setnewopciones(self, valopciones):      
        opciones = {'val1':False, 'val2': False, 'val3': False }
        for i in range(1,4):
            indice = 'val' + str(i)
            if valopciones[indice] == 'on':
                opciones[indice] = True
        return opciones
  
    def post(self):
        usuario = cgi.escape(self.request.get('login_usuario'))
        password = cgi.escape(self.request.get('login_password'))
        
        
        if (len(usuario) > 0) and (len(password) > 0):
            usuarios = Usuario.query().filter(ndb.GenericProperty('usuario') == usuario).fetch(1) 
            if usuarios:              
                for element in usuarios:                    
                    if element.usuario == usuario:                        
                        n_hash = MD5.new(password).hexdigest()                       
                        if element.clave == n_hash:                           
                            if element.rol == 'rol02' or element.rol == 'rol03':
                                #ojo al llenado al reves           
                                ckb1 = cgi.escape(self.request.get('ckb3'))
                                ckb2 = cgi.escape(self.request.get('ckb2'))
                                ckb3 = cgi.escape(self.request.get('ckb1'))
                                                                
                                valopciones = {'val1':str(ckb1), 'val2': str(ckb2), 'val3': str(ckb3) }
                                opciones = self.setnewopciones(valopciones)
                                if self.updateprofile(usuario, opciones):
                                    self.printmensaje('t_adm_respuesta_rol.html','Actualizacion correcta')
                                else:
                                    self.printmensaje('t_adm_respuesta_rol.html','Existen problemas para actualizar los datos')
                            else:                                
                                self.printmensaje(destino_login,'su usuario no tiene permisos en esta seccion')
                        else:                            
                            self.printmensaje(destino_login,'clave incorrecta')
                    else:                        
                        self.printmensaje(destino_login,'usuario no registrado')
            else:                
                self.printmensaje(destino_login,'usuario no existe')
            
        
        
class RegistroHandler(webapp2.RequestHandler):
    
    def printmensaje(self, name_template, mensaje):
        template = jinja_environment.get_template(name_template)
        self.response.out.write(template.render({'version':version, 'empresa':'OP Energetica S.A.C', 'mensaje':mensaje, 'path':'../'}))
        
        
    def post(self):
 
            Respuesta = ''
            login_usuario = cgi.escape(self.request.get('login_usuario'))
            login_password = cgi.escape(self.request.get('login_password'))
            nombres = cgi.escape(self.request.get('nombres'))
            paterno = cgi.escape(self.request.get('paterno'))
            materno = cgi.escape(self.request.get('materno'))
            usuario = cgi.escape(self.request.get('usuario'))
            cambio_clave = cgi.escape(self.request.get('flip'))
            clave = cgi.escape(self.request.get('clave'))
            re_clave = cgi.escape(self.request.get('re_clave'))
            email = cgi.escape(self.request.get('email'))
            sel_rol = cgi.escape(self.request.get('sel_rol'))

            #flag para habilitar crear otros usuarios
            booladmin = False
            
            if (len(login_usuario) > 0) and (len(login_password) > 0):
                
                useradmin = Usuario.query().filter(ndb.GenericProperty('usuario') == login_usuario).fetch(1)
            
                if useradmin:             
                    for element in useradmin:                    
                        if element.usuario == login_usuario:                        
                            n_hash = MD5.new(login_password).hexdigest()                       
                            if element.clave == n_hash:                           
                                if element.rol == 'rol04':                                
                                    booladmin = True 
                            else:
                                self.printmensaje('t_adm_respuesta.html', 'clave incorrecta')
                        else:
                            self.printmensaje('t_adm_respuesta.html', 'usuario no registrado')                        
                else:
                    self.printmensaje('t_adm_respuesta.html', 'usuario no registrado')
            else: 
               strreferer = self.request.referer
               if strreferer.find(loginpage) >= 0:
                    hash = MD5.new(clave).hexdigest()
                    ndb_profile = Usuario(usuario = usuario, clave = hash, nombres = nombres, paterno = paterno, materno = materno, rol = sel_rol, email = email)
                    ndb_profile.put()
                    self.printmensaje('t_adm_respuesta.html', 'usuario registrado')
               else:
                    self.printmensaje('t_adm_respuesta.html', 'Debe ingresar un usuario') 
        
        
            if booladmin:
          
                if len(usuario) > 0:
                    usuarios = Usuario.query().filter(ndb.GenericProperty('usuario') == usuario).fetch(1) 
                    if usuarios:            
                         for element in usuarios:
                            if element.usuario == usuario:
    
                                response_profile = {
                                    'path': '../',
                                    'version': version,
                                    'mensaje':'',
                                    'lnombre':'',
                                    '':'',
                                    '':'',
                                    '':'',
                                    '':'',
                                    '':'',
                                    '':'',
                                    '':'',
                                    '':'',
                                    '':'',
                                    '':'',
                                    '':'',
                                    '':'',
                                    '':'',
                                    '':''
                                }
                                
                                n_hash = MD5.new(clave).hexdigest()
                                
                                if element.clave == n_hash:
                                    self.printmensaje('t_adm_respuesta.html', 'usuario ya se encuentra registrado')
                                else:
                                    self.printmensaje('t_adm_respuesta.html', 'usuario ya se encuentra registrado')
                    else:
    
                        hash = MD5.new(clave).hexdigest()
                        ndb_profile = Usuario(usuario = usuario, clave = hash, nombres = nombres, paterno = paterno, materno = materno, rol = sel_rol, email = email)
                        ndb_profile.put()
                        self.printmensaje('t_adm_respuesta.html', 'registro con exito')
                        
                else:
                    global_printmensaje(self,'t_adm_profile.html','debe ingresar nombre de usuario','')

app = webapp2.WSGIApplication([
    ('/profile', MainHandler),('/profile/menu',MenuHandler),('/profile/roles',ProfileHandler), ('/profile/respuesta',RegistroHandler)
    ], debug=True)

def main():
    application.run()
    
if __name__ == '__main__':
    main()