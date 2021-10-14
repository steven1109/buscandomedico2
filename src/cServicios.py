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

        values = (id_medico, id_consultorio, des_servicio, num_precio, fec_creacion)

        return query, values

    def read_data(self):
        query = ' select id_servicio,id_medico,id_consultorio,des_servicio,num_precio,fec_creacion ' \
            ' from servicio ' \
            ' where id_medico = {}'.format(
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
                    'des_servicio': servicio[3],
                    'num_precio': float(servicio[4]),
                    'fec_creacion': str(servicio[5])
                }, results))
        }
        return response
