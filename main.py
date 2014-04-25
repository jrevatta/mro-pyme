#!/usr/bin/env python

import os
import webapp2
import jinja2
import logging
import cgi
import json

import Crypto.Hash.MD5 as MD5

from google.appengine.ext import db
from google.appengine.ext import ndb

from opmodel import *
#inicializar jinja2

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')))

version = '0.9'
   
    
#---metodos para interactuar desde la web


class MainHandler(webapp2.RequestHandler):
    def get(self):
        
        templates_values = {
            'version': version,
            'empresa': 'Pyme',
            'mensaje':''       
        }
        

        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(templates_values))


       
class LoginHandler(webapp2.RequestHandler):
    
    def printmensaje(self, name_template, mensaje):
            template = jinja_environment.get_template(name_template)
            self.response.out.write(template.render({'version':version, 'empresa':'Pyme ', 'mensaje':mensaje}))    
    
    def post(self):
        
        form_usu = cgi.escape(self.request.get('usuario'))
        form_clave = cgi.escape(self.request.get('password'))
        
       
        usuarios = Usuario.query().filter(ndb.GenericProperty('usuario') == form_usu).fetch(1)
        if usuarios:            
            for element in usuarios:
                if element.usuario == form_usu:
                    n_hash = MD5.new(form_clave).hexdigest()
                    
                    if element.clave == n_hash:
                        
                        val_template = {'url':'', 'nombre':''}
                        list_val = []
                        dict_permisos = {'permisos':[]}
                        permisos = Profile.query().filter(ndb.GenericProperty('usuario') == form_usu).fetch(1)
                        if permisos:
                            for permiso in permisos:
                                if permiso.operaciones == True:
                                    val_template = {'url':'', 'nombre':''}
                                    val_template['url'] = '/operaciones?usuario=' + form_usu
                                    val_template['nombre'] = 'operaciones'
                                    list_val.append(val_template)
                                    
                                if permiso.reportes == True:
                                    val_template = {'url':'', 'nombre':''}
                                    val_template['url'] = '/reportes?usuario=' + form_usu
                                    val_template['nombre'] = 'reportes'
                                    list_val.append(val_template)
                                    
                                if permiso.inventario == True:
                                    val_template = {'url':'', 'nombre':''}
                                    val_template['url'] = '/inventario?usuario=' + form_usu
                                    val_template['nombre'] = 'inventario'
                                    list_val.append(val_template)
                                    
                                logging.info('lista: %s', list_val)
                                dict_permisos['permisos'] = list_val
                                                               
                                

                        template = jinja_environment.get_template('pagina0.html')
                        
                        self.response.out.write(template.render(dict_permisos))    
                        #self.response.out.write(template.render(c))
                    else:
                        self.printmensaje('index.html','Clave incorrecta')
                else:
                    self.printmensaje('index.html','Usuario no existe')
        else:
            self.printmensaje('index.html','Usuario no existe')

class OperacionesHandler(webapp2.RequestHandler):
    
    def printmensaje(self, name_template, mensaje):
        template = jinja_environment.get_template(name_template)
        self.response.out.write(template.render({'version':version, 'empresa':'OP Energetica S.A.C', 'mensaje':mensaje, 'path':'../'}))
        
    def get(self):
      usuario = cgi.escape(self.request.get('usuario'))
      logging.info('usuario en operaciones: %s', usuario)
      usu_obj = Usuario()
      usu_obj = usu_obj.get_usuario(usuario)
      keyusuario = usu_obj._key
      logging.info('keyusuario:', keyusuario)
      if keyusuario:
        obj_operaciones = Operaciones()
        dict_operaciones = obj_operaciones.get_operaciones(keyusuario)
        logging.info('diccionario:', dict_operaciones)
        if dict_operaciones: 
            template = jinja_environment.get_template('t_web_operaciones.html')
            self.response.out.write(template.render(dict_operaciones))
        else:
            mensaje = 'no se encontraron operaciones'
            self.printmensaje('t_web_respuesta.html',mensaje)
            logging.info('no se encontraron operaciones')
      else:
        mensaje = 'no existe usuario'
        self.printmensaje('t_web_respuesta.html',mensaje)
        logging.info('no existe usuario')
        

class InformesHandler(webapp2.RequestHandler):
    def get(self):
        operacion = cgi.escape(self.request.get('operacion'))
        logging.info('codigo de operacion: %s', operacion)
        
        #diccionario que contiene toda la informacion a renderizar para generar la pantalla de formularios.
        
        
        dict_informe = {'operacion':'', 'informe_layout':'',  'mensaje':'', 'empresa':'Pyme'}
      
        logging.info ('el dict_informe', dict_informe)
      
        dict_layout = {
                'tabs': {
                    'tab1':{'name':'uno','label':'Cliente'},
                    'tab2':{'name':'dos','label':'Equipamiento'},
                    'tab3':{'name':'tres','label':'Trabajo'}                                   
                },
                'divs':{
                    'div1':{
                        'name': 'uno',
                        'descripcion':'Cliente',
                        'campos': {
                            'campo1':{
                                'name': 'supervisor',
                                'data': 'Benito Juarez',
                                'type': 'input'
                            },
                            'campo2':{
                                'name': 'hora_ejecucion',
                                'data': '08-20',
                                'type': 'input'
                            },
                            'campo3':{
                                'name': 'fecha',
                                'data': '23/05/2013',
                                'type': 'input'
                            },
                                
                            'campo4':{
                                'name': 'ubicacion',
                                'data': {'op1':'S/D', 'op2':'S/S','op3':'D/D'},
                                'type': 'select'
                            },
                            'campo5':{
                                'name': 'potencia',
                                'data': '40',
                                'type': 'input'
                            },
                            
                            'campo6':{
                                'name': 'nivel_a',
                                'data': '22.5',
                                'type': 'input'
                            },
                            'campo7':{
                                'name': 'nivel_b',
                                'data': '43.6',
                                'type': 'input'
                            },
                                
                            'campo8':{
                                'name': 'suministro',
                                'data': {'op1':'True','op2':'False'},
                                'type': 'checkbox'
                            },

                            'campo9':{
                                'name': 'direccion',
                                'data': 'Jr. 8 de Octubre 454 Pueblo Libre',
                                'type': 'textarea'
                            },
                            'campo10':{
                                'name': 'nombre',
                                'data': 'Teresa Ocampo',
                                'type': 'input'
                            },
                            
                        }
                    },
                    'div2':{
                        'name': 'dos',
                        'descripcion': 'Equipamiento',
                        'campos': {
                            'campo1':{
                                'name': 'celda de MT',
                                'data': '01 seleccionador de potencia marca IMUDIESTRELE',
                                'type': 'textarea'
                            },
    
                            'campo2':{
                                'name': 'celda de Transformacion',
                                'data': '01 Transformador de 1250 KVA 22.9 KV / 04KV marca DELCROSA',
                                'type': 'textarea'
                            },
                            'campo3':{
                                'name': 'celda de baja tension',
                                'data': '01 interruptor termomagnetico general de 2000A, marca Merlin Gerin',
                                'type': 'input'
                            }
                        }
                    },
                        
                    'div3':{
                        'name': 'tres',
                        'descipcion': 'Trabajos Realizados',
                        'campos': {
                            'campo1':{
                                'name': 'Estructura Metalica',
                                'data': 'Limpieza General y pulverizado',
                                'type': 'textarea'
                            },
    
                            'campo2':{
                                'name': 'Seleccionador de potencia',
                                'data': 'Limpieza de seccionador',
                                'type': 'textarea'
                            }
                        }
                    }   
                                               
                }    
                
            
        }
        
        logging.info('el diccionario layout: %s', dict_layout)
          #obj_usuarioInforme = UsuarioInforme()
          #obj_usuarioInforme = UsuarioInforme.get_by_id('usui001')
          #dict_informe['informe_data'] = obj_usuarioInforme.informe_data
      
        dict_informe['informe_layout'] = dict_layout
      
          #informe_def_key = obj_usuarioInforme.informedef
          #id_informe_def = informe_def_key.id()
          #logging.info('informe_def_key %s', id_informe_def)
          #obj_informedef = InformeDefinicion()
          #id_informe_def = 'id001'
          #obj_informedef = obj_informedef.get_by_id(id_informe_def)
      
        
          #dict_informe['operacion'] = str(operacion)
        dict_informe['operacion'] = '0001'
        

       

        logging.info('diccionario completo: %s', dict_layout)
        template = jinja_environment.get_template('t_form_informe.html')
        self.response.out.write(template.render(dict_informe)) 
    
class BatchHandler(webapp2.RequestHandler):
    def get(self):
               
    #dict:layout un diccionario que contiene toda la informacion para renderizar o generar la pagina con el
    #formulario. Este diccionario se debe generar desde otras estructuras de datos.
    #Pendiente crear la pagina que genera el diccionario.
   
   
        dict_layout = {
                'tabs': {
                    'tab1':{'name':'uno','label':'Cliente'},
                    'tab2':{'name':'dos','label':'Equipamiento'},
                    'tab3':{'name':'tres','label':'Trabajo'}                                   
                },
                'divs':{
                    'div1':{
                        'name': 'uno',
                        'descripcion':'Cliente',
                        'campos': {
                            'campo1':{
                                'name': 'supervisor',
                                'data': 'Benito Juarez',
                                'type': 'input'
                            },
    
                            'campo2':{
                                'name': 'hora_ejecucion',
                                'data': '08-20',
                                'type': 'input'
                            },
                            'campo3':{
                                'name': 'fecha',
                                'data': '23/05/2013',
                                'type': 'input'
                            },
                                
                            'campo4':{
                                'name': 'ubicacion',
                                'data': 'S/D',
                                'type': 'input'
                            },
                            'campo5':{
                                'name': 'potencia',
                                'data': '40',
                                'type': 'input'
                            },
                            
                            'campo6':{
                                'name': 'nivel_a',
                                'data': '22.5',
                                'type': 'input'
                            },
                            
                            
                            'campo7':{
                                'name': 'nivel_b',
                                'data': '43.6',
                                'type': 'input'
                            },
                                
                            'campo8':{
                                'name': 'suministro',
                                'data': 'True',
                                'type': 'checkbox'
                            },

                            'campo9':{
                                'name': 'direccion',
                                'data': 'Jr. 8 de Octubre 454 Pueblo Libre',
                                'type': 'textarea'
                            },
                            'campo10':{
                                'name': 'nombre',
                                'data': 'Teresa Ocampo',
                                'type': 'input'
                            },
                            
                        }
                    },
                    'div2':{
                        'name': 'dos',
                        'descripcion': 'Equipamiento',
                        'campos': {
                            'campo1':{
                                'name': 'celda de MT',
                                'data': '01 seleccionador de potencia marca IMUDIESTRELE',
                                'type': 'textarea'
                            },
    
                            'campo2':{
                                'name': 'celda de Transformacion',
                                'data': '01 Transformador de 1250 KVA 22.9 KV / 04KV marca DELCROSA',
                                'type': 'textarea'
                            },
                            'campo3':{
                                'name': 'celda de baja tension',
                                'data': '01 interruptor termomagnetico general de 2000A, marca Merlin Gerin',
                                'type': 'input'
                            }
                        }
                    },
                        
                    'div3':{
                        'name': 'tres',
                        'descipcion': 'Trabajos Realizados',
                        'campos': {
                            'campo1':{
                                'name': 'Estructura Metalica',
                                'data': 'Limpieza General y pulverizado',
                                'type': 'textarea'
                            },
    
                            'campo2':{
                                'name': 'Seleccionador de potencia',
                                'data': 'Limpieza de seccionador',
                                'type': 'textarea'
                            }
                        }
                    }
                        

                    
                                               
                }    
                
            
        }
   
        #Los diccionarios se almacenaran en objetos en formato json.
        #El codigo mostrado es para almacenar la informacion.
        
        
        #print en formato json
        informe_data = json.dumps(dict_data, sort_keys = False)
        informe_schema = json.dumps(dict_schema, sort_keys = False)
        informe_options = json.dumps(dict_options, sort_keys = False)
        
        logging.info('informe_data: %s', informe_data)
        logging.info('informe_schema: %s', informe_schema)
        logging.info('informe_options: %s', informe_options)   
        
        
        #obj_informe = InformeDefinicion(id='id001')
        
        obj_informe = InformeDefinicion()
        
        obj_informe = obj_informe.get_by_id('id001')
        obj_informe.version = 1     
        obj_informe.informe_schema = informe_schema
        obj_informe.informe_layout = informe_options   
        obj_informe.put()
        
            
        usuario = Usuario()
        usuario = usuario.get_usuario('terago')
        key_usuario = usuario._key
        
        logging.info('terago id: %s', key_usuario.id() )
        
        obj_usu_informe = UsuarioInforme(id='usui001')
        obj_usu_informe.usuario = key_usuario
        obj_usu_informe.informedef = obj_informe._key
        obj_usu_informe.informe_data = informe_data
        obj_usu_informe.put()
        
        metadata = InformeMetaData(id='imd001',
                                   usuario = usuario.usuario,
                                   tiempo_estimado = 4,
                                   tiempo_atencion = 3,
                                   tiempo_espera = 1,
                                   comentario = 'crear alerta por falla en control primario',
                                   costo_estimado = 2200.200,
                                   usuario_informe = obj_usu_informe._key)
        metadata.put()
        
        
                                   
        
        
app = webapp2.WSGIApplication([
    ('/', MainHandler),('/pagina0', LoginHandler), ('/operaciones', OperacionesHandler), ('/informes', InformesHandler), ('/batch', BatchHandler)
], debug=True)

def main():
    application.run()
    
if __name__ == '__main__':
    main()