import os
from repository.bd_departamento import DepartamentoRepository


class DepartamentoController:
    # TODO:
    # Llamadas a los eventos definidos en repository
    def __init__(self, conn):
        self.repository = DepartamentoRepository(conn)
        
    def controller(self, parameters):
        if parameters.value != '':
            return self.repository.findDepartamentoByCod(parameters['value'])
        else:
            return self.repository.findAllDepartamentos()
            
