from medico.controller.ct_medico import MedicoController


class Dispatcher:
    def __init__(self, connection):
        self.connection = connection
        self.dispatcher = MedicoController(connection)
        self.param = ''

    def execute(self, parameters):
        self.param = parameters
        data = self.dispatcher.controller(self.param)
        if len(data) == 0:
            return self.error_result()
        else:
            return self.response(data)

    def response(self, data):
        return {'_status': 1,
                'medicosArray': list(
                    map(lambda medico: {
                        'id_medico': int(medico[0]),
                        'nombre_completo': medico[1] + ' ' + medico[2] + ' ' + medico[3],
                        'codigo_colegiado': medico[8],
                        'descripcion': medico[9],
                        'promedio_puntaje': float(medico[13])
                    }, data))}

    def error_result(self):
        return {
            '_status': 0,
            'medicosArray': [],
            'message': 'Lo sentimos, no hay resultado para esta busqueda'
        }
