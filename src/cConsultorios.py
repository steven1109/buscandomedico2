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

        values = (id_medico, cod_distrito, cod_provincia, cod_departamento,
                  des_direccion, horario_atencion, fec_creacion)

        return query, values

    def read_data(self):
        query = ' select id_consultorio,id_medico,cod_distrito,cod_provincia,cod_departamento,des_direccion,horario_atencion,fec_creacion ' \
            ' from consultorio ' \
            ' where id_medico = {}'.format(
                str(self.param['id_medico']))

        return query

    def update_data(self):
        cod_departamento = self.param['cod_departamento']
        cod_provincia = self.param['cod_provincia']
        cod_distrito = self.param['cod_distrito']
        des_direccion = self.param['des_direccion']
        horario_atencion = self.param['horario_atencion']
        fec_modificacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = 'UPDATE consultorio SET cod_distrito = %s, cod_provincia = %s, cod_departamento = %s, des_direccion = %s, horario_atencion = %s, fec_modificacion = %s ' \
            ' WHERE id_consultorio = {}'.format(self.param['id_consultorio'])
        
        values = (cod_distrito, cod_provincia, cod_departamento, des_direccion, horario_atencion, fec_modificacion)
        
        return query, values

    def delete_data(self):
        return 'delete from consultorio WHERE id_consultorio = {}'.format(self.param['id_consultorio'])

    def response_data(self, results):
        response = {
            '_status': 200,
            'consultoriosArray': list(
                map(lambda consultorio: {
                    'id_consultorio': int(consultorio[0]),
                    'id_medico': int(consultorio[1]),
                    'cod_distrito': consultorio[2],
                    'cod_provincia': consultorio[3],
                    'cod_departamento': consultorio[4],
                    'des_direccion': consultorio[5],
                    'horario_atencion': consultorio[6],
                    'fec_creacion': str(consultorio[7])
                }, results))
        }

        return response
