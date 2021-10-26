from datetime import datetime
import unicodedata


class EspecialidadMedico:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        pass

    def read_data(self):
        clausulas = ''
        if self.param['id_medico'] != "":
            clausulas += ' AND me.genero = {}'.format(
                int(self.param['genero']))

        if self.param['especialidad'] != "":
            name_specialization = unicodedata.normalize(
                'NFKD', self.param['especialidad']).encode('ASCII', 'ignore').upper().decode("utf-8")
            clausulas += ' AND es.des_especialidad LIKE "%{}%"'.format(
                name_specialization.upper())

        query = ' select em.id_especialidad_medico, em.id_especialidad, es.des_especialidad, ' \
            ' em.id_medico, me.nombres, me.ape_paterno, me.ape_materno, em.codigo_rne, ' \
            ' em.fec_creacion, me.bol_activo ' \
            ' from especialidad_medico em ' \
            ' inner join especialidad es on em.id_especialidad = es.id_especialidad ' \
            ' inner join medico me on em.id_medico = me.id_medico ' \
            ' where me.bol_activo = 1 {};'.format(clausulas)

        return query

    def update_data(self):
        pass

    def delete_data(self):
        query = ' delete from especialidad_medico where id_especialidad_medico = {}'.format(
            self.param['id_especialidad_medico'])
        return query

    def response_data(self, results):
        response = {
            '_status': 200,
            'especialidadArray': list(
                map(lambda especialidad: {
                    'id_especialidad_medico': especialidad[0],
                    'id_especialidad': especialidad[1],
                    'des_especialidad': especialidad[2],
                    'id_medico': especialidad[3],
                    'nombre_completo': especialidad[4] + ', ' + especialidad[5] + ' ' + especialidad[6],
                    'codigo_rne': especialidad[7]
                }, results)
            )
        }

        return response
