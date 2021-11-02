from datetime import datetime


class Ubigeo:
    def __init__(self, parameters):
        self.param = parameters
        self.fields_ubigeos = {
            'departamento': 'cod_departamento,des_departamento',
            'provincia': 'cod_provincia,des_provincia',
            'distrito': 'cod_distrito,des_distrito'
        }
        self.query_fields = {
            'departamento': 'cod_departamento',
            'provincia': 'cod_departamento',
            'distrito': 'cod_provincia'
        }
        self.information = {
            'error_exists': 'Error, el código no existe en la tabla {}',
            'error_blank': 'Error, debe enviar un código para la consulta',
            'err_medico': 'Lo sentimos, no se tiene respuesta a la busqueda que está haciendo'
        }

    def add_data(self):
        pass

    def read_data(self):
        condition = ''
        if self.param['value'] == "" and self.param['table'] != 'departamento':
            query = ''

        if self.param['value'] != '' and self.param['field'] != '':
            condition = f'where {self.param["field"]} = "{self.param["value"]}";'

        query = f'select {self.fields_ubigeos[self.param["table"]]} from {self.param["table"]} {condition}'

        return query

    def update_data(self):
        pass

    def delete_data(self):
        pass

    def response_data(self, results):
        if len(results) == 0:
            response = {
                '_status': 404,
                'message': 'Error, el código no existe en la tabla {}'.format(self.param['table']),
                'ubigeosArray': []
            }
        else:
            response = {
                '_status': 200,
                'ubigeosArray': list(
                    map(lambda ubigeo: {
                        'codi': ubigeo[0],
                        'description': ubigeo[1]},
                        results))
            }

        return response
