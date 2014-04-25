#   Object Model
from datetime import date
from google.appengine.ext import ndb
import logging
#model class para el Login. Debo probar la persistencia

#version 0.9 alfa


class Usuario(ndb.Model):
    usuario = ndb.StringProperty()
    clave = ndb.StringProperty()
    date = ndb.DateTimeProperty(auto_now_add=True)
    nombres = ndb.StringProperty() 
    paterno = ndb.StringProperty()
    materno = ndb.StringProperty()
    email = ndb.StringProperty()
    rol = ndb.StringProperty()
       
    def get_usuariokey(cls, keyusuario):
        result = None
        if keyusuario:
            q = cls.query().filter(Usuario._key == keyusuario).fetch(1)
            for element in q:
                result = element
        return result
         
    def get_usuario(cls, usuario):
        result = None
        if len(usuario) > 0:
            q = cls.query().filter(ndb.GenericProperty('usuario') == usuario).fetch(1)
            for element in q:
                result = element
        return result
                

class Profile(ndb.Model):
        usuario = ndb.StringProperty()
        operaciones = ndb.BooleanProperty()
        inventario = ndb.BooleanProperty()
        reportes = ndb.BooleanProperty()
        
#version 0.9 beta
               
class Cliente(ndb.Model):
        cliente = ndb.StringProperty()
        direccion = ndb.StringProperty()
        activo = ndb.BooleanProperty()
        contacto = ndb.StringProperty()
        ubicacion = ndb.StringProperty()
        
        def get_cliente(cls, id):
            value = None
            if id:
                value = cls.get_by_id(id)
            return value
            


class InformeDefinicion(ndb.Model):
        version = ndb.IntegerProperty()
        informe_schema = ndb.JsonProperty()
        informe_layout = ndb.JsonProperty()


class UsuarioInforme(ndb.Model):
        usuario = ndb.KeyProperty(kind=Usuario)
        informedef = ndb.KeyProperty(kind=InformeDefinicion)
        fecha_creacion = ndb.DateTimeProperty(auto_now_add=True)
        informe_data = ndb.JsonProperty()
      
class InformeMetaData(ndb.Model):
        usuario = ndb.StringProperty()
        fecha_creacion = ndb.DateTimeProperty(auto_now_add=True)
        tiempo_estimado = ndb.IntegerProperty()
        tiempo_atencion = ndb.IntegerProperty()
        tiempo_espera = ndb.IntegerProperty()
        comentario = ndb.StringProperty()
        costo_estimado = ndb.FloatProperty()
        usuario_informe = ndb.KeyProperty(kind=UsuarioInforme)
         
        
class ImagenInforme(ndb.Model):
        usuarioinforme = ndb.KeyProperty(kind=UsuarioInforme)
        titulo = ndb.StringProperty()
        imagen = ndb.BlobProperty()

class TipoOperacion(ndb.Model):
        tipo = ndb.StringProperty()
        descripcion = ndb.StringProperty()
        
class Operaciones(ndb.Model):
        asignado = ndb.KeyProperty(kind=Usuario)
        cliente = ndb.KeyProperty(kind=Cliente)
        cliente_name = ndb.StringProperty()
        registrado = ndb.KeyProperty(kind=Usuario)
        titulo = ndb.StringProperty()
        descripcion = ndb.StringProperty()
        fecha_creacion = ndb.DateTimeProperty(auto_now_add=True)
        tipo_operacion = ndb.KeyProperty(kind=TipoOperacion)
        
        
        def get_operaciones(cls, key_asignado):
            c = {'operaciones':[], 'ope_fecha':''}
            d = date.today()
            list_c = {'cliente':'', 'titulo':'', 'descripcion':'', 'fecha':'', 'url':''}
            logging.info('valor de cls.asignado: %s',cls.asignado)
            logging.info('valor de key_asignado: %s', key_asignado)
            operaciones = cls.query().filter(ndb.GenericProperty('asignado') == key_asignado).fetch(100) #Tener presente en definir en el filter la clase.propiedad
            # Tener presente que cuando se borra una tabla, la primera lectura no funciona bien, problema del SDK
            logging.info('dentro de metodo. valor de operaciones %s',  operaciones)
            if operaciones:
                for element in operaciones:
                    logging.info('dentro del for')
                    list_c = {'cliente':'', 'titulo':'', 'descripcion':'', 'fecha':'', 'url':''}
                    list_c['cliente'] = element.cliente_name
                    list_c['descripcion'] = element.descripcion
                    list_c['fecha'] = str(element.fecha_creacion.strftime("%d/%m/%y"))
                    list_c['url'] = '/informes?operacion=' + str(element._key.id())
                    logging.info('datos ingresados en diccionario : %s, %s, %s', element.titulo, element.descripcion, str(element.fecha_creacion.strftime("%d/%m/%y")))
                    c['operaciones'].append(list_c)
                c['ope_fecha'] = d.strftime("%A, %d. %B %Y %I:%M%p") #formato dependiente del ingles. Se debe usar el api webapp2 con internationalization
            return c
