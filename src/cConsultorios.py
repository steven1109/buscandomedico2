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
        horario_inicio = self.param['horario_inicio']
        horario_fin = self.param['horario_fin']
        fec_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = ' INSERT INTO consultorio (id_medico,cod_distrito,cod_provincia,cod_departamento,' \
                ' des_direccion,horario_inicio,horario_fin,fec_creacion) ' \
                ' VALUES(%s,%s,%s,%s,%s,%s,%s,%s) '

        values = (id_medico, cod_distrito, cod_provincia, cod_departamento, des_direccion,
                  horario_inicio, horario_fin, fec_creacion)

        return query, values

    def read_data(self):
        query = ' select con.id_consultorio,con.id_medico,con.cod_departamento,dep.des_departamento, ' \
                ' con.cod_provincia,pro.des_provincia,con.cod_distrito,dis.des_distrito, ' \
                ' con.des_direccion,con.horario_inicio,con.horario_fin,con.fec_creacion ' \
                ' from consultorio con ' \
                ' inner join departamento dep on con.cod_departamento = dep.cod_departamento ' \
                ' inner join provincia pro on con.cod_provincia = pro.cod_provincia ' \
                ' inner join distrito dis on con.cod_distrito = dis.cod_distrito ' \
                ' where con.id_medico = {}'.format(
            str(self.param['id_medico']))

        return query

    def update_data(self):
        cod_departamento = self.param['cod_departamento']
        cod_provincia = self.param['cod_provincia']
        cod_distrito = self.param['cod_distrito']
        des_direccion = self.param['des_direccion']
        horario_inicio = self.param['horario_inicio']
        horario_fin = self.param['horario_fin']
        fec_modificacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = ' UPDATE consultorio SET cod_distrito = %s, cod_provincia = %s, cod_departamento = %s, ' \
                ' des_direccion = %s, horario_inicio = %s, horario_fin = %s, fec_modificacion = %s ' \
                ' WHERE id_consultorio = {}'.format(self.param['id_consultorio'])

        values = (cod_distrito, cod_provincia, cod_departamento, des_direccion,
                  horario_inicio, horario_fin, fec_modificacion)

        return query, values

    def delete_data(self):
        return 'delete from consultorio WHERE id_consultorio = {}'.format(self.param['id_consultorio'])

    def response_data(self, results):
        if len(results) == 0:
            response = {
                '_status': 404,
                'message': 'Error, No existen datos en la tabla {}'.format(self.param['table']),
                'emptyArray': []
            }
        else:
            response = {
                '_status': 200,
                'consultoriosArray': list(
                    map(lambda consultorio: {
                        'id_consultorio': int(consultorio[0]),
                        'id_medico': int(consultorio[1]),
                        'cod_departamento': str(consultorio[2]),
                        'des_departamento': consultorio[3],
                        'cod_provincia': str(consultorio[4]),
                        'des_provincia': consultorio[5],
                        'cod_distrito': str(consultorio[6]),
                        'des_distrito': consultorio[7],
                        'des_direccion': consultorio[8],
                        'horario_inicio': consultorio[9],
                        'horario_fin': consultorio[10],
                        'fec_creacion': str(consultorio[11])
                    }, results))
            }

        return response
