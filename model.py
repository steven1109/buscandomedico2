import unicodedata
from cryptography.fernet import Fernet
from config import Config
from datetime import datetime
from config import DBMySql
import pymysql
from cMedico import Medico as disMedico
from cEnfermedades import Enfermedadestratadas as disEnfermedades
from cFormacion import Formacion as disFormacion
from cConsultorios import Consultorio as disConsultorios
from cServicios import Servicios as disServico
# from loguru import logger


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

        self.dispatcher = {}

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

                return response

            except Exception as e:
                self.errorResult(e)
            finally:
                if self.conn:
                    self.closeConnect()

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

                return response

            except Exception as e:
                self.errorResult(e)
            finally:
                if self.conn:
                    self.closeConnect()

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

                return response

            except Exception as e:
                self.errorResult(e)
            finally:
                if self.conn:
                    self.closeConnect()

    def add_row(self, parameters):

        self.dispatcher = {
            'medico': disMedico(parameters),
            'enfermedades': disEnfermedades(parameters),
            'formacion': disFormacion(parameters),
            'consultorios': disConsultorios(parameters),
            'servicios': disServico(parameters)
        }

        try:
            query, values = self.dispatcher[parameters['table']].add_data()
            self.reConnect()
            self.cur.execute(query, values)
            self.conn.commit()
            return {
                '_status': 200,
                'message': 'Los datos de {}, se han registrado de manera correcta'.format(parameters['table'])
            }
        except pymysql.MySQLError as e:
            self.errorResult(e)
        except Exception as e:
            self.errorResult(e)

    def select_data(self, parameters):
        self.dispatcher = {
            'medico': disMedico(parameters),
            'enfermedades': disEnfermedades(parameters),
            'formacion': disFormacion(parameters),
            'consultorios': disConsultorios(parameters),
            'servicios': disServico(parameters)
        }
        try:
            query = self.dispatcher[parameters['table']].read_data()
            self.reConnect()
            results = self.executeQuery(query)

            if len(results) == 0:
                return {
                    '_status': 400,
                    'message': self.information['err_medico'],
                    'medicoArray': []
                }

            if parameters['table'] == 'medico':
                for result in results:
                    response = {
                        '_status': 200,
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

            elif parameters['table'] == 'enfermedades':
                response = {
                    '_status': 200,
                    'enfermedadesArray': list(
                        map(lambda enfermedad: {
                            'id_enf_tratadas': int(enfermedad[0]),
                            'id_medico': int(enfermedad[1]),
                            'des_enfermedades': enfermedad[2],
                            'fec_creacion': str(enfermedad[3])
                        }, results))}

            elif parameters['table'] == 'formacion':
                response = {
                    '_status': 200,
                    'formacionArray': list(
                        map(lambda formacion: {
                            'id_formacion': int(formacion[0]),
                            'id_medico': int(formacion[1]),
                            'nom_centro': formacion[2],
                            'desc_formacion': formacion[3],
                            'fec_anio_inicio': str(formacion[4]),
                            'fec_anio_fin': str(formacion[5]),
                            'fec_creacion': str(formacion[6])
                        }, results))
                }

            elif parameters['table'] == 'consultorios':
                response = {
                    '_status': 200,
                    'consultoriosArray': list(
                        map(lambda consultorio: {
                            'id_consultorio': int(consultorio[0]),
                            'id_medico': int(consultorio[1]),
                            'cod_distrito': consultorio[2],
                            'cod_provincia': consultorio[3],
                            'cod_departamento': consultorio[4],
                            'des_direccion': consultorio[5],
                            'horario_atencion': consultorio[6],
                            'fec_creacion': str(consultorio[7])
                        }, results))
                }
                
            elif parameters['table'] == 'servicios':
                response = {
                    '_status': 200,
                    'serviciosArroy': list(
                        map(lambda servicio: {
                            'id_servicio': int(servicio[0]),
                            'id_medico': int(servicio[1]),
                            'des_servicio': servicio[2],
                            'num_precio': float(servicio[3]),
                            'fec_creacion': str(servicio[4])
                        }, results))
                }

            return response

        except pymysql.MySQLError as e:
            self.errorResult(e)
        except Exception as e:
            self.errorResult(e)

    def errorResult(self, msg):
        return {
            '_status': 405,
            'message': 'Error en la ejecución, ' + str(msg)
        }

    def reConnect(self):
        # logger.info('Database reconnection.')
        self.conn = self.mydb.connect()
        self.cur = self.conn.cursor()

    def closeConnect(self):
        self.conn.close()
        self.conn = None
        # logger.info('Database connection closed.')

    def executeQuery(self, query):
        if self.conn is None:
            self.reConnect()

        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def decrypt(self, encMessage):
        key = Config.TOKEN.encode()  # Fernet.generate_key()
        fernet = Fernet(key)
        return fernet.decrypt(encMessage.encode()).decode()

    def encrypted(self, message):
        key = Config.TOKEN.encode()  # Fernet.generate_key()
        fernet = Fernet(key)
        return fernet.encrypt(message.encode())
