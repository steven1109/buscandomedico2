import os
from datetime import datetime


class Provincia:
    # Clase provincia
    def __init__(self, cod_provincia='', des_provincia=''):
        self._cod_provincia = cod_provincia
        self._des_provincia = des_provincia
        self.fecha_provincia = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # getter methods
    def get_cod_provincia(self):
        return self._cod_departamento

    def get_des_provincia(self):
        return self._des_provincia

    # setter methods
    def set_cod_provincia(self, codigo):
        self._cod_provincia = codigo

    def set_des_provincia(self, descripcion):
        self._des_provincia = descripcion
