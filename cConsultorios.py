from datetime import datetime


class Consultorio:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        id_medico = self.param['id_medico']
        cod_departamento = self.param['cod_departamento']
        cod_provincia = self.param['cod_provincia']
        cod_distrito = self.param['cod_distrito']
        des_direccion = self.param['des_direccion']
        horario_atencion = self.param['horario_atencion']
        fec_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = ' INSERT INTO consultorio (id_medico,cod_distrito,cod_provincia,cod_departamento,des_direccion,horario_atencion,fec_creacion) ' \
            ' VALUES(%s,%s,%s,%s,%s,%s,%s) '

        values = (id_medico,cod_distrito,cod_provincia,cod_departamento,des_direccion,horario_atencion,fec_creacion)

        return query, values

    def read_data(self):
        query = ' select id_consultorio,id_medico,cod_distrito,cod_provincia,cod_departamento,des_direccion,horario_atencion,fec_creacion ' \
            ' from consultorio ' \
            ' where id_medico = {}'.format(
                str(self.param['id_medico']))

        return query

    def update_data(self):
        pass

    def delete_data(self):
        pass
