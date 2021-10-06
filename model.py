import unicodedata
from cryptography.fernet import Fernet
from config import Config
from datetime import datetime
from config import DBMySql


class Dispatcher:
    def __init__(self):
        self.mydb = DBMySql()
        self.mydb.initialize()
        self.conn = self.mydb.connect()
        self.cur = self.conn.cursor()
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
        if parameters['type'] == 'Ubigeo':
            condition = ''
            try:
                if parameters['value'] == "" and parameters['table'] != 'departamento':
                    return {
                        '_status': 0,
                        'message': self.information['error_blank']
                    }

                if parameters['value'] != '' and parameters['field'] != '':
                    condition = f'where {parameters["field"]} = "{parameters["value"]}";'

                query = f'select {self.fields_ubigeos[parameters["table"]]} from {parameters["table"]} {condition}'
                ubigeos = self.executeQuery(query)

                if len(ubigeos) == 0:
                    return {
                        '_status': 0,
                        'message': self.information['error_exists'].format(parameters['table']),
                        'ubigeosArray': []
                    }

                response = {
                    '_status': 1,
                    'ubigeosArray': list(
                        map(lambda ubigeo: {'codi': ubigeo[0], 'description': ubigeo[1]}, ubigeos))
                }
                self.conn.cursor().close()
                return response

            except Exception as e:
                return {
                    '_status': 0,
                    'message': 'Error en la ejecución de la consulta, ' + str(e)
                }

        elif parameters['type'] == 'Medico':
            # Filtros
            clausulas = ''
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
                    ' where me.bol_activo = 1 {} ' \
                    ' group by me.id_medico,me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.cod_departamento,me.cod_distrito,me.cod_provincia, ' \
                    ' me.codigo_cmp,me.comentario_personal,es.des_especialidad ' \
                    ' order by me.ape_materno;'.format(clausulas)

                medicos = self.executeQuery(query)

                if len(medicos) == 0:
                    return {
                        '_status': 0,
                        'message': self.information['err_medico'],
                        'medicosArray': []
                    }

                response = {
                    '_status': 1,
                    'medicosArray': list(
                        map(lambda medico: {
                            'id_medico': int(medico[0]),
                            'nombre_completo': medico[1] + ' ' + medico[2] + ' ' + medico[3],
                            'codigo_colegiado': medico[8],
                            'descripcion': medico[9],
                            'promedio_puntaje': float(medico[13])
                        }, medicos))}

                self.conn.cursor().close()
                return response

            except Exception as e:
                return {
                    '_status': 0,
                    'message': 'Error en la ejecución de la consulta, ' + str(e),
                }

        elif parameters['type'] == 'Login':
            try:
                i = 0
                query = ' select us.id_medico,pu.des_perfil_usuario,us.des_correo,us.des_pass, ' \
                    ' me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.fec_nacimiento,me.codigo_cmp,es.id_especialidad, ' \
                    ' es.des_especialidad,esme.codigo_rne ' \
                    ' from usuario us ' \
                    ' inner join perfil_usuario pu on us.id_perfil_usuario = pu.id_perfil_usuario ' \
                    ' left join medico me on us.id_medico = me.id_medico ' \
                    ' left join especialidad_medico esme on me.id_medico = esme.id_medico ' \
                    ' left join especialidad es on esme.id_especialidad = es.id_especialidad;'
                results = self.executeQuery(query)

                for result in results:
                    if parameters['user'] == result[2] and self.decrypt(result[3]) == parameters['pass']:
                        i += 1
                        response = {
                            '_status': 1,
                            'id_medico': result[0],
                            'perfil': result[1],
                            'welcome': ('Dra. ' if result[7] == 1 else 'Dr. ') +
                            result[4] + ', ' + result[5] + ' ' + result[6],
                            'nombre': result[4],
                            'ape_paterno': result[5],
                            'ape_materno': result[6],
                            'fec_nacimiento': str(result[8]),
                            'cmp': result[9],
                            'genero': result[7],
                            'id_especialidad': result[10],
                            'des_especialidad': result[11],
                            'rme': result[12]
                        }
                        break

                if i == 0:
                    response = {
                        '_status': 0,
                        'result': 'El usuario o la contraseña ingresada es incorrecta.'
                    }

                self.conn.cursor().close()
                return response

            except Exception as e:
                return {
                    '_status': 0,
                    'message': 'Error en la ejecución de la consulta, ' + str(e)
                }

        elif parameters['type'] == 'get_medico':
            #try:
            i = 0
            query = ' select me.id_medico,me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.cod_departamento,me.cod_distrito,me.cod_provincia, ' \
                ' me.codigo_cmp,me.comentario_personal,es.des_especialidad,me.fec_nacimiento,es.id_especialidad,esme.codigo_rne,me.fec_colegiatura, ' \
                ' me.cod_departamento,me.cod_provincia,me.cod_distrito,us.des_correo,pu.des_perfil_usuario,me.flag_atiende_covid, ' \
                ' me.flag_Atiende_vih,me.flag_atiende_videollamada,me.facebook,me.instagram,me.twitter,me.linkedin, ' \
                ' COUNT(com.id_medico) AS count_doc,  ' \
                ' CASE WHEN COUNT(com.id_medico) > 0 THEN SUM(com.puntaje) ELSE 0 END AS sum_com, ' \
                ' CASE WHEN COUNT(com.id_medico) > 0 THEN ROUND(AVG(com.puntaje),2) ELSE 0 END AS prom ' \
                ' from medico me ' \
                ' inner join especialidad_medico esme on me.id_medico = esme.id_medico ' \
                ' inner join especialidad es on esme.id_especialidad = es.id_especialidad ' \
                ' left join comentarios com on me.id_medico = com.id_medico ' \
                ' left join usuario us on me.id_medico = us.id_medico ' \
                ' inner join perfil_usuario pu on us.id_perfil_usuario = pu.id_perfil_usuario ' \
                ' where me.id_medico = {} ' \
                ' group by me.id_medico,me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.cod_departamento,me.cod_distrito,me.cod_provincia, ' \
                ' me.codigo_cmp,me.comentario_personal,es.des_especialidad,me.fec_nacimiento,es.id_especialidad,esme.codigo_rne,me.fec_colegiatura, ' \
                ' me.cod_departamento,me.cod_provincia,me.cod_distrito,us.des_correo,pu.des_perfil_usuario,me.flag_atiende_covid, ' \
                ' me.flag_Atiende_vih,me.flag_atiende_videollamada' \
                ' order by me.ape_materno;'.format(str(parameters['id_medico']))

            results = self.executeQuery(query)

            if len(results) == 0:
                return {
                    '_status': 0,
                    'message': self.information['err_medico'],
                    'medicoArray': []
                }

            for result in results:
                i += 1
                response = {
                    '_status': 1,
                    'id_medico': result[0],
                    'perfil': result[19],
                    'welcome': ('Dra. ' if result[4] == 1 else 'Dr. ') +
                    result[1] + ', ' + result[2] + ' ' + result[3],
                    'nombre': result[1],
                    'ape_paterno': result[2],
                    'ape_materno': result[3],
                    'fec_nacimiento': str(result[11]),
                    'cmp': result[8],
                    'genero': result[4],
                    'id_especialidad': result[12],
                    'des_especialidad': result[10],
                    'rme': result[13],
                    'fec_colegiatura': str(result[14]),
                    'cod_departamento': result[15],
                    'cod_provincia': result[16],
                    'cod_distrito': result[17],
                    'correo': result[18],
                    'flag_atiende_covid': result[20],
                    'flag_Atiende_vih': result[21],
                    'flag_atiende_videollamada': result[22],
                    'facebook': result[23],
                    'instagram': result[24],
                    'twitter': result[25],
                    'linkedin': result[26]
                }

            if i == 0:
                response = {
                    '_status': 0,
                    'result': 'El médico no existe en la DB.'
                }

            self.conn.cursor().close()
            return response

            # except Exception as e:
            #     return {
            #         '_status': 0,
            #         'message': 'Error en la ejecución de la consulta, ' + str(e)
            #     }

    def add_row(self, parameters):
        try:
            if parameters['cod_departamento'] == "":
                return {
                    '_status': 0,
                    'message': self.information['error_blank']
                }

            cod_departamento = parameters['cod_departamento']
            cod_provincia = parameters['cod_provincia']
            cod_distrito = parameters['cod_distrito']
            id_prospecto = parameters['id_prospecto']
            nombres = parameters['nombres']
            ape_paterno = parameters['ape_paterno']
            ape_materno = parameters['ape_materno']
            fec_nacimiento = parameters['fec_nacimiento']
            genero = parameters['genero']
            codigo_cmp = parameters['codigo_cmp']
            atiende_covid = 0 if int(parameters['atiende_covid']) == 0 else int(
                parameters['atiende_covid'])
            atiende_vih = 0 if int(parameters['atiende_vih']) == 0 else int(
                parameters['atiende_vih'])
            videollamada = 0 if int(parameters['videollamada']) == 0 else int(
                parameters['videollamada'])
            descripcion_profesional = parameters['descripcion_profesional']
            facebook = parameters['facebook']
            instagram = parameters['instagram']
            twitter = parameters['twitter']
            linkedin = parameters['linkedin']
            fec_colegiatura = parameters['fec_colegiatura']
            activo = 1
            creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            query = ' INSERT INTO medico (cod_departamento,cod_provincia,cod_distrito,id_prospecto,nombres,ape_paterno,ape_materno,fec_nacimiento, ' \
                ' genero,codigo_cmp,fec_colegiatura,flag_atiende_covid,flag_Atiende_vih,flag_atiende_videollamada,comentario_personal,facebook, ' \
                ' instagram,twitter,linkedin,bol_activo,fec_creacion)  ' \
                ' VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '

            values = (cod_departamento, cod_provincia, cod_distrito, id_prospecto, nombres, ape_paterno, ape_materno, fec_nacimiento,
                      genero, codigo_cmp, fec_colegiatura, atiende_covid, atiende_vih, videollamada, descripcion_profesional, facebook, instagram,
                      twitter, linkedin, activo, creation_date)

            self.cur.execute(query, values)
            self.conn.commit()
            return {
                '_status': 200,
                'message': "Se ha registrado de manera correcta al medico"
            }
        except Exception as e:
            return {
                '_status': 0,
                'message': 'Error en la ejecución de la inserción, ' + str(e)
            }

    def executeQuery(self, query):        
        if self.conn is False:
            self.conn = self.mydb.connect()
            self.cur = self.conn.cursor()
            
        self.cur.execute(query)
        return self.cur.fetchall()

    def decrypt(self, encMessage):
        key = Config.TOKEN.encode()  # Fernet.generate_key()
        fernet = Fernet(key)
        return fernet.decrypt(encMessage.encode()).decode()

    def encrypted(self, message):
        key = Config.TOKEN.encode()  # Fernet.generate_key()
        fernet = Fernet(key)
        return fernet.encrypt(message.encode())
