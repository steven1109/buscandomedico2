from datetime import datetime


class Enfermedadestratadas:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        id_medico = self.param['id_medico']
        des_enfermedades = self.param['des_enfermedades']
        fec_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = ' INSERT INTO enfermedades_tratadas (id_medico, des_enfermedades, fec_creacion)  ' \
            ' VALUES(%s,%s,%s) '

        values = (id_medico, des_enfermedades, fec_creacion)

        return query, values

    def read_data(self):
        query = ' select id_enf_tratadas, id_medico, des_enfermedades, fec_creacion ' \
            ' from enfermedades_tratadas ' \
            ' where id_medico = {}'.format(
                str(self.param['id_medico']))

        return query

    def update_data(self):
        pass

    def delete_data(self):
        pass
