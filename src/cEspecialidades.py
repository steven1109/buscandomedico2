import unicodedata


class Especialidades:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        pass

    def read_data(self):
        clausulas = ''
        if self.param['especialidad'] != "":
            name_specialization = unicodedata.normalize(
                'NFKD', self.param['especialidad']).encode('ASCII', 'ignore').upper().decode("utf-8")
            clausulas += ' AND des_especialidad LIKE "%{}%"'.format(
                name_specialization.upper())

        query = ' select id_especialidad, des_especialidad, bol_activo ' \
                ' from especialidad where bol_activo = 1 {};'.format(clausulas)

        return query

    def update_data(self):
        pass

    def delete_data(self):
        pass

    def response_data(self, results):
        if len(results) == 0:
            response = {
                '_status': 404,
                'message': 'Error, la especialidad no existe en la tabla {}'.format(self.param['table']),
                'emptyArray': []
            }
        else:
            response = {
                '_status': 200,
                'especialidadArray': list(
                    map(lambda especialidad: {
                        'codi': especialidad[0],
                        'especialidad': especialidad[1]
                    }, results)
                )
            }

        return response
