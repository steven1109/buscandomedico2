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
            query = 'select me.id_medico,me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.cod_departamento,me.cod_distrito,me.cod_provincia, ' \
                'me.codigo_cmp,me.comentario_personal,es.des_especialidad, ' \
                'COUNT(com.id_medico) AS count_doc,  ' \
                'CASE WHEN COUNT(com.id_medico) > 0 THEN SUM(com.puntaje) ELSE 0 END AS sum_com, ' \
                'CASE WHEN COUNT(com.id_medico) > 0 THEN ROUND(AVG(com.puntaje),2) ELSE 0 END AS prom ' \
                'from medico me ' \
                'inner join especialidad_medico esme on me.id_medico = esme.id_medico ' \
                'inner join especialidad es on esme.id_especialidad = es.id_especialidad ' \
                'left join comentarios com on me.id_medico = com.id_medico ' \
                'where es.bol_activo = 1 ' \
                'group by me.id_medico,me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.cod_departamento,me.cod_distrito,me.cod_provincia, ' \
                'me.codigo_cmp,me.comentario_personal,es.des_especialidad'

            self.cur.execute(query)
            medicos = self.cur.fetchall()
            medicosDict = {
                "medicosArray": []
            }

            if len(medicos) == 0:
                return {'_status': self.information['error_exists'].format(parameters['table'])}
            
            for medico in medicos:
                medicosDict['medicosArray'].append(
                    {
                        'id_medico': medico[0],
                        'nombre_completo': medico[1] + ' ' + medico[2] + ' ' + medico[3],
                        'codigo_colegiado': medico[8],
                        'descripcion': medico[9],
                        'promedio_puntaje': medico[13]
                    }
                )

            return medicosDict
