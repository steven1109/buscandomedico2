import os
from controller.ct_departamento import DepartamentoController
import controller.ct_provincia
import controller.ct_distrito


class Dispatcher:
    def __init__(self, connection):
        self.dispatcher = DepartamentoController(connection)
        self.param = ""
        
    def execute(self, parameters):
        self.param = parameters
        return self.dispatcher.controller(self.param)
