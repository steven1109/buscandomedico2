from regions.dispatcher_regions import Dispatcher


connection = "colocar la cadena de conexion"
parameters = {
    'type': 'departamento',
    'value': '05'
}

dispatcher = Dispatcher(connection=connection, parameters=parameters)


