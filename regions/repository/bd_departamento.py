import os


class DepartamentoRepository:
    # TODO:
    # Definición de todos los eventos que se hará a la tabla departamento.

    def __init__(self, conn):
        self.query_find = "SELECT * FROM departamento {}"
        self.cursor = conn.cursor()

    def findDepartamentoByCod(self, codigo):
        self.cursor.execute(self.query_find.format(
            f' where cod_departamento = "{codigo}";'))
        return self.cursor.fetchall()

    def findAllDepartamentos(self):
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
