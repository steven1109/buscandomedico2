import os


class Dispatcher:
    def __init__(self, connection):
        self.connection = connection
        self.cur = connection.cursor()
        self.information = {
            'error_exists': 'Error, el código no existe en la tabla {}',
            'error_blank': 'Error, debe enviar un código para la consulta'
        }
        self.fields_ubigeos = {
            'departamento': 'cod_departamento,des_departamento',
            'provincia': 'cod_provincia,des_provincia',
            'distrito': 'cod_distrito,des_distrito'
        }

    def model(self, parameters):
        condition = ''
        if parameters['type'] == 'Ubigeo':

            if parameters['value'] == "" and parameters['table'] != 'departamento':
                return {"_status": self.information['error_blank']}

            if parameters['value'] != '' and parameters['field'] != '':
                condition = f'where {parameters["field"]} = "{parameters["value"]}";'

            query = f'select {self.fields_ubigeos[parameters["table"]]} from {parameters["table"]} {condition}'

            self.cur.execute(query)
            ubigeos = self.cur.fetchall()
            ubigeosDict = {
                'ubigeosArray': []
            }
            if len(ubigeos) == 0:
                return {'_status': self.information['error_exists'].format(parameters['table'])}

            for ubigeo in ubigeos:
                ubigeosDict['ubigeosArray'].append(
                    {
                        'codi': ubigeo[0],
                        'description': ubigeo[1]
                    }
                )

            return ubigeosDict

        elif parameters['type'] == 'Medico':
            return ''
