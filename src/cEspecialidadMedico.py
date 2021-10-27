from datetime import datetime
import unicodedata


class EspecialidadMedico:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        id_especialidad = self.param['id_especialidad']
        id_medico = self.param['id_medico']
        codigo_rne = str(self.param['codigo_rne'])
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = ' INSERT INTO especialidad_medico (id_especialidad, id_medico, codigo_rne, fec_creacion) ' \
            ' VALUES (%s, %s, %s, %s)'

        values = (id_especialidad, id_medico, codigo_rne, creation_date)

        return query, values

    def read_data(self):
        clausulas = ''
        if self.param['id_medico'] != "":
            clausulas += ' AND me.genero = {}'.format(
                int(self.param['id_medico']))

        if self.param['especialidad'] != "":
            name_specialization = unicodedata.normalize(
                'NFKD', self.param['especialidad']).encode('ASCII', 'ignore').upper().decode("utf-8")
            clausulas += ' AND es.des_especialidad LIKE "%{}%"'.format(
                name_specialization.upper())

        query = ' SELECT em.id_especialidad_medico, em.id_especialidad, es.des_especialidad, ' \
            ' em.id_medico, me.nombres, me.ape_paterno, me.ape_materno, em.codigo_rne, ' \
            ' em.fec_creacion, me.bol_activo ' \
            ' FROM especialidad_medico em ' \
            ' INNER JOIN especialidad es ON em.id_especialidad = es.id_especialidad ' \
            ' INNER JOIN medico me ON em.id_medico = me.id_medico ' \
            ' WHERE me.bol_activo = 1 {};'.format(clausulas)

        return query

    def update_data(self):
        id_especialidad = self.param['id_especialidad']
        id_medico = self.param['id_medico']
        codigo_rne = self.param['codigo_rne']
        modification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = ' UPDATE especialidad_medico SET id_especialidad = %s, id_medico = %s, codigo_rne = %s, fec_modificacion = %s ' \
            ' WHERE id_especialidad_medico = {};'.format(
                self.param['id_especialidad_medico'])

        values = (id_especialidad, id_medico, codigo_rne, modification_date)

        return query, values

    def delete_data(self):
        query = ' DELETE FROM especialidad_medico WHERE id_especialidad_medico = {};'.format(
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
