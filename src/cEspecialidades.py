from datetime import datetime


class Especialidades:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        pass

    def read_data(self):
        query = ' select id_especialidad, des_especialidad, bol_activo ' \
            ' from especialidad where bol_activo = 1;'
        
        return query

    def update_data(self):
        pass

    def delete_data(self):
        pass

    def response_data(self, results):
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
