import unicodedata


class Dispatcher:
    def __init__(self, connection):
        self.connection = connection
        self.cur = connection.cursor()
        self.information = {
            'error_exists': 'Error, el código no existe en la tabla {}',
            'error_blank': 'Error, debe enviar un código para la consulta',
            'err_medico': 'Lo sentimos, no se tiene respuesta a la busqueda que está haciendo'
        }
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

    def model(self, parameters):
        condition = ''
        if parameters['type'] == 'Ubigeo':

            if parameters['value'] == "" and parameters['table'] != 'departamento':
                return {"_status": self.information['error_blank']}

            if parameters['value'] != '' and parameters['field'] != '':
                condition = f'where {parameters["field"]} = "{parameters["value"]}";'

            query = f'select {self.fields_ubigeos[parameters["table"]]} from {parameters["table"]} {condition}'

            ubigeos = self.executeQuery(query)
            if len(ubigeos) == 0:
                return {'_status': self.information['error_exists'].format(parameters['table'])}

            response = {'ubigeosArray': list(
                map(lambda ubigeo: {'codi': ubigeo[0], 'description': ubigeo[1]}, ubigeos))}

            return response

        elif parameters['type'] == 'Medico':
            # Filtros
            clausulas = ""
            try:
                if parameters['genero'] != "":
                    clausulas += ' AND me.genero = {}'.format(
                        int(parameters['genero']))

                if parameters['cod_departamento'] != "":
                    clausulas += ' AND me.cod_departamento = "{}"'.format(
                        parameters['cod_departamento'])

                if parameters['cod_provincia'] != "":
                    clausulas += ' AND me.cod_provincia = "{}"'.format(
                        parameters['cod_provincia'])

                if parameters['cod_distrito'] != "":
                    clausulas += ' AND me.cod_distrito = "{}"'.format(
                        parameters['cod_distrito'])

                if parameters['especialidad'] != "":
                    name_specialization = unicodedata.normalize(
                        'NFKD', parameters['especialidad']).encode('ASCII', 'ignore').upper().decode("utf-8")
                    clausulas += ' AND es.des_especialidad LIKE "%{}%"'.format(
                        name_specialization.upper())

                query = ' select me.id_medico,me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.cod_departamento,me.cod_distrito,me.cod_provincia, ' \
                    ' me.codigo_cmp,me.comentario_personal,es.des_especialidad, ' \
                    ' COUNT(com.id_medico) AS count_doc,  ' \
                    ' CASE WHEN COUNT(com.id_medico) > 0 THEN SUM(com.puntaje) ELSE 0 END AS sum_com, ' \
                    ' CASE WHEN COUNT(com.id_medico) > 0 THEN ROUND(AVG(com.puntaje),2) ELSE 0 END AS prom ' \
                    ' from medico me ' \
                    ' inner join especialidad_medico esme on me.id_medico = esme.id_medico ' \
                    ' inner join especialidad es on esme.id_especialidad = es.id_especialidad ' \
                    ' left join comentarios com on me.id_medico = com.id_medico ' \
                    ' where es.bol_activo = 1 {} ' \
                    ' group by me.id_medico,me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.cod_departamento,me.cod_distrito,me.cod_provincia, ' \
                    ' me.codigo_cmp,me.comentario_personal,es.des_especialidad ' \
                    ' order by me.ape_materno;'.format(clausulas)

                medicos = self.executeQuery(query)

                if len(medicos) == 0:
                    return {'_status': self.information['err_medico']}

                response = {'medicosArray': list(
                    map(lambda medico: {
                        'id_medico': int(medico[0]),
                        'nombre_completo': medico[1] + ' ' + medico[2] + ' ' + medico[3],
                        'codigo_colegiado': medico[8],
                        'descripcion': medico[9],
                        'promedio_puntaje': float(medico[13])
                    }, medicos))}

                return response

            except Exception as e:
                return {
                    'message': 'Error en la ejecución de la consulta, ' + str(e),
                    'status': False
                }

        elif parameters['type'] == 'Login':
            response = {
                'status': 'ok'
            }

            return response

    def executeQuery(self, query):
        self.cur.execute(query)
        return self.cur.fetchall()
