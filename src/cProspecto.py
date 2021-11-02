from datetime import datetime


class Prospecto:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        pass

    def read_data(self):
        pass

    def update_data(self):
        pass

    def delete_data(self):
        pass

    def response_data(self, results):
        if len(results) == 0:
            response = {
                '_status': 400,
                'message': 'Error, No existen datos en la tabla {}'.format(self.param['table']),
                'emptyArray': []
            }
        else:
            response = {
                '_status': 200
            }

        return response
