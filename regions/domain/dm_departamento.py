from datetime import datetime


class Departamento:
    # Clase departamento
    def __init__(self, cod_departamento='', des_departamento=''):
        self._cod_departamento = cod_departamento
        self._des_departamento = des_departamento
        self.fecha_departamento = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # getter methods
    def get_cod_departamento(self):
        return self._cod_departamento

    def get_des_departamento(self):
        return self._des_departamento

    # setter methods
    def set_cod_departamento(self, codigo):
        self._cod_departamento = codigo

    def set_des_departamento(self, descripcion):
        self._des_departamento = descripcion
