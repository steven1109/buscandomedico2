import os
import controller.ct_departamento
import controller.ct_provincia
import controller.ct_distrito


class Dispatcher:
    def __init__(self, connection):
        self.connection = connection
        self.action = {}
        
    def model(self):
        return "ok"
