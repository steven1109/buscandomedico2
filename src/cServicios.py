from datetime import datetime


class Servicios:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        id_medico = self.param['id_medico']
        id_consultorio = self.param['id_consultorio']
        des_servicio = self.param['des_servicio']
        num_precio = self.param['num_precio']
        fec_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = ' INSERT INTO servicio (id_medico,id_consultorio,des_servicio,num_precio,fec_creacion) ' \
            ' VALUES(%s,%s,%s,%s,%s) '

        values = (id_medico, id_consultorio,
                  des_servicio, num_precio, fec_creacion)

        return query, values

    def read_data(self):
        query = ' select ser.id_servicio,ser.id_medico,ser.id_consultorio,con.cod_provincia,pro.des_provincia, ' \
            ' con.cod_distrito,dis.des_distrito,con.des_direccion,ser.des_servicio,ser.num_precio,ser.fec_creacion ' \
            ' from servicio ser ' \
            ' inner join consultorio con on ser.id_consultorio = con.id_consultorio ' \
            ' inner join departamento dep on con.cod_departamento = dep.cod_departamento ' \
            ' inner join provincia pro on con.cod_provincia = pro.cod_provincia ' \
            ' inner join distrito dis on con.cod_distrito = dis.cod_distrito ' \
            ' where ser.id_medico = {}'.format(
                str(self.param['id_medico']))

        return query

    def update_data(self):
        id_consultorio = self.param['id_consultorio']
        des_servicio = self.param['des_servicio']
        num_precio = self.param['num_precio']
        fec_modificacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = ' update servicio set id_consultorio = %s, des_servicio = %s, num_precio = %s, fec_modificacion = %s' \
            ' where id_servicio = {}'.format(self.param['id_servicio'])

        values = (id_consultorio, des_servicio, num_precio, fec_modificacion)

        return query, values

    def delete_data(self):
        return 'delete from servicio WHERE id_servicio = {}'.format(self.param['id_servicio'])

    def response_data(self, results):
        response = {
            '_status': 200,
            'serviciosArroy': list(
                map(lambda servicio: {
                    'id_servicio': int(servicio[0]),
                    'id_medico': int(servicio[1]),
                    'id_consultorio': int(servicio[2]),
                    'direccion': servicio[7],
                    'distrito_direccion': (str(servicio[6]) + ' - ' + servicio[7]),
                    'des_servicio': servicio[8],
                    'num_precio': float(servicio[9]),
                    'fec_creacion': str(servicio[10])
                }, results))
        }
        return response
