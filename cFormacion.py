from datetime import datetime


class Formacion:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        id_medico = self.param['id_medico']
        nom_centro = self.param['nom_centro']
        desc_formacion = self.param['desc_formacion']
        fec_anio_inicio = self.param['fec_anio_inicio']
        fec_anio_fin = self.param['fec_anio_fin']
        fec_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = ' INSERT INTO formacion (id_medico,nom_centro,desc_formacion,fec_anio_inicio,fec_anio_fin,fec_creacion)  ' \
            ' VALUES(%s,%s,%s,%s,%s,%s) '

        values = (id_medico,nom_centro,desc_formacion,fec_anio_inicio,fec_anio_fin,fec_creacion)

        return query, values

    def read_data(self):
        query = ' select id_formacion,id_medico,nom_centro,desc_formacion,fec_anio_inicio,fec_anio_fin,fec_creacion ' \
            ' from formacion ' \
            ' where id_medico = {}'.format(
                str(self.param['id_medico']))

        return query

    def update_data(self):
        pass

    def delete_data(self):
        pass