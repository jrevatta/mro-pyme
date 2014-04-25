#miscelanea de codigo
#Este archivo solo contiene partes de codigo que se pueden reutilizar mas adelante y ejemplos.

     #populate todas las clases para reportes y operaciones
   
      
        #cargar operaciones por supervisor jmatusalen
        q = Usuario.query().filter(ndb.GenericProperty('usuario') == 'jmatusalen').fetch(1)
        for element in q:
            usuario_key = element.key
            logging.info('la key de jmatusalen es: %s', usuario_key)
            logging.info('la key de jmatusalen en urlsafe es: %s', usuario_key.urlsafe() )
        
        #cliente = Cliente(id='cl001', cliente = 'TopiTop S.A.C', direccion = 'jr. amazonas 454 dpto 101', activo = True, contacto = 'Juan Perez', ubicacion = 'San Juan')
        #cliente.put()
        #cliente_key = cliente._key
        
        #cliente_key = ndb.Key(Cliente, 'cl001')
        #logging.info('la key para el nuevo cliente es: %s', cliente_key.id())
        #cliente = Cliente(id='cl001') #esto crearia un nuevo cliente con esa llave
        
        #logging.info('el valor en cliente: %s, direccion: %s, contacto: %s', cliente.cliente, cliente.direccion, cliente.contacto)
        
        #cliente_key = ndb.Key(Cliente, 'cl001')
        #cliente2 = Cliente.get_by_id(cliente_key.id()) #aqui si se obtiene el cliente con esa llave
        cliente = Cliente()
        x = cliente.get_cliente('cl001')
        logging.info('el mismo cliente por otros metodos %s', x.cliente) #ufffff me costo trabajo encontrar la forma de crear un metodo que me devuelva un cliente
        
        cliente = Cliente(id='cl002', cliente = 'Operaciones del MAR S.A.C', direccion = 'jr. naciones unidas 123', activo = True, contacto = 'Jhon Ramirez', ubicacion = 'San Miguel')
        cliente.put()
        key_cliente2 = cliente._key
        obj_name2 = cliente.cliente
        
        cliente = Cliente(id='cl003', cliente = 'CENCOSUD S.A.', direccion = 'av. Argentina 1', activo = True, contacto = 'Nicolas Lynch', ubicacion = 'La Molina')
        cliente.put()
        key_cliente3 = cliente._key
        obj_name3 = cliente.cliente
        #especifico.
        #debo crear una instancia del objeto que deseo recuperar
        #luego pasarle el id y obtener el objeto deseado.
        
        op = TipoOperacion(id='t01', tipo = 'preventivo', descripcion ='operaciones preventivas')
        op.put()
        
        op = TipoOperacion(id='t02', tipo = 'emergencias', descripcion = 'operaciones de emergencias')
        op.put()
        
        op = TipoOperacion(id='t03', tipo = 'mantenimiento', descripcion = 'operaciones de mantenimiento')
        op.put()
        
        
        asignado = Usuario()
        asignado = asignado.get_usuario('terago')
        key_asignado = asignado._key
        logging.info('asignado: %s', key_asignado)
        
        cliente = Cliente()
        cliente = cliente.get_cliente('cl001')
        key_cliente = cliente._key
        obj_name = cliente.cliente
        logging.info('cliente: %s', key_cliente)
        
        registrado = Usuario()
        registrado = registrado.get_usuario('jmatusalen')
        key_registrado = registrado._key
        logging.info('usuario: %s', key_registrado)
        
        key_tipo_operacion = ndb.Key(TipoOperacion, 't02')
        
        localop = Operaciones(id='op001',
                              asignado = key_asignado,
                              cliente = key_cliente,
                              cliente_name = obj_name,
                              registrado = key_registrado,
                              titulo = 'emergencia cableado',
                              descripcion ='Emergencia en cableado estructurado de planta de alimentacion electrica en sede huachipa',
                              tipo_operacion = key_tipo_operacion)
        localop.put()
        
        localop = Operaciones(id='op002',
                              asignado = key_asignado,
                              cliente = key_cliente2,
                              cliente_name = obj_name2,
                              registrado = key_registrado,
                              titulo = 'emergencia subterranea',
                              descripcion ='Emergencia subterranea en planta extractora de tintes',
                              tipo_operacion = key_tipo_operacion)
        
        localop.put()
        
        key_tipo_operacion = ndb.Key(TipoOperacion, 't03')

        localop = Operaciones(id='op003',
                              asignado = key_asignado,
                              cliente = key_cliente3,
                              cliente_name = obj_name3,
                              registrado = key_registrado,
                              titulo = 'Mantenimiento subterranea',
                              descripcion ='Mantenimiento de lineas subterranea en planta extractora de tintes',
                              tipo_operacion = key_tipo_operacion)        
        
        localop.put()
        
        logging.info('info de tipos')
        
        q = TipoOperacion.query().filter().fetch(10)
        for e in q:
            logging.info('datos: %s', e.descripcion)            
    
        logging.info('key_asignado: %s', key_asignado)
        c = localop.get_operaciones(key_asignado)
        
        logging.info('el diccionario con la info registrada: %s', c)
        
        
        #diccionario con un array dentro
        informe = {'action':'', 'method':'', 'html':[]}
        informe['method'] = 'get'
        informe['action'] = 'detail?usuario='
        element = {'html':'formulario de intervencion:', 'type':'p'}
        informe['html'].append(element)
        element = {'type':'text', 'nombre':'usuario', 'id':'usuario', 'caption':'usuario'}
        informe['html'].append(element)
        element = { 'type':'password', 'name':'password', 'caption':'Password'}
        informe['html'].append(element)
        element = {'type':'submit', 'value':'Login'}
        informe['html'].append(element)
        logging.info('diccionario: %s', informe)
        
     #script para usar alpaca script.
     #como conclusi—n el problema es que se complica injectar codigo para armar un html5 de acuerdo a un
     #dise–o particular. Sirve para formularios directos en HTML pero se complica un poco con el 5.
<script type="text/javascript">
$(document).ready(function() {
      {% if informe_data %}
      
      var data = {{informe_data|safe}};
      
      {% endif %}
      
      
      {% if informe_schema %}
      
      var schema = {{informe_schema|safe}};
      
      {% endif %}
      
      {% if informe_layout %}
      
      var options = {{informe_layout|safe}};

      
      {% endif %}
      
      $("#form1").alpaca({
         {% if informe_data %}
	 "data": data,	 
	 {% endif %}
         {% if informe_schema %}
	 "schema": schema,	 
	 {% endif %}
         {% if informe_layout %}
	 "options": options
	 {% endif %}
      });
});

</script>
        
        
        

        