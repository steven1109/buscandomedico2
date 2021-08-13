import os
from regions.controller.ct_departamento import DepartamentoController
from regions.controller.ct_provincia import ProvinciaController
from regions.controller.ct_distrito import DistritoController


class Dispatcher:
    def __init__(self, connection):
        self.connection = connection
        self.dispatcher = DepartamentoController(connection)
        self.param = ""

    def execute(self, parameters):
        self.param = parameters
        self.dispatcher = {
            'departamento': DepartamentoController(self.connection),
            'provincia': ProvinciaController(self.connection),
            'distrito': DistritoController(self.connection)
        }

        data = self.dispatcher[self.param['table']].controller(self.param)
        if len(data) == 0:
            return self.error_result()
        else:
            return self.response(data)

    def response(self, data):
        return {'ubigeosArray': list(
            map(lambda ubigeo: {'codi': str(ubigeo[0]), 'description': ubigeo[1]}, data))}
        
    def error_result(self):
        return {
            '_status': False,
            'message': 'Lo sentimos, no hay resultado para esta busqueda'
        }
