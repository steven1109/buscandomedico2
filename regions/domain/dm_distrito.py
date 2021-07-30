import os
from datetime import datetime


class Distrito:
    # Clase distrito
    def __init__(self, cod_distrito='', des_distrito=''):
        self._cod_distrito = cod_distrito
        self._des_distrito = des_distrito
        self.fecha_distrito = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # getter methods
    def get_cod_distrito(self):
        return self._cod_distrito

    def get_des_distrito(self):
        return self._des_distrito

    # setter methods
    def set_cod_distrito(self, codigo):
        self._cod_distrito = codigo

    def set_des_distrito(self, descripcion):
        self._des_distrito = descripcion
