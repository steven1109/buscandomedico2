import os
from logging import getLogger
log = getLogger(__name__)


class DepartamentoRepository:
    # TODO:
    # Definición de todos los eventos que se hará a la tabla departamento.
    def __init__(self, cursor):
        self.query_find = 'SELECT cod_departamento,des_departamento FROM departamento '
        self.cursor = cursor

    def findByCod(self, codigo):
        self.cursor.execute(self.query_find +
                             f' where cod_departamento = "{codigo}";')
        return self.cursor.fetchall()

    def findAll(self):
        self.cursor.execute(self.query_find)
        return self.cursor.fetchall()

    def create():
        pass

    def update():
        pass

    def deleteByCod(codigo):
        pass

    def deleteAll():
        pass
