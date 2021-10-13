from datetime import datetime


class Servicios:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        id_medico = self.param['id_medico']
        des_servicio = self.param['des_servicio']
        num_precio = self.param['num_precio']
        fec_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = ' INSERT INTO servicio (id_medico,des_servicio,num_precio,fec_creacion) ' \
            ' VALUES(%s,%s,%s,%s) '

        values = (id_medico,des_servicio,num_precio,fec_creacion)

        return query, values

    def read_data(self):
        query = ' select id_servicio,id_medico,des_servicio,num_precio,fec_creacion ' \
            ' from servicio ' \
            ' where id_medico = {}'.format(
                str(self.param['id_medico']))

        return query

    def update_data(self):
        pass

    def delete_data(self):
        pass
