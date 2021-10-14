from cryptography.fernet import Fernet
from config import Config
from config import DBMySql
import pymysql
from src.cMedico import Medico as disMedico
from src.cEnfermedades import Enfermedadestratadas as disEnfermedades
from src.cFormacion import Formacion as disFormacion
from src.cConsultorios import Consultorio as disConsultorios
from src.cServicios import Servicios as disServico
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
            try:
                class_medico = disMedico(parameters)
                query = class_medico.get_medico_by_especialidad()
                medicos = self.executeQuery(query)

                if len(medicos) == 0:
                    return {
                        '_status': 404,
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
                            'promedio_puntaje': float(medico[13]),
                            'especialidad': medico[10]
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

    def dispatcher(self, parameters):
        return {
            'medico': disMedico(parameters),
            'enfermedades': disEnfermedades(parameters),
            'formacion': disFormacion(parameters),
            'consultorios': disConsultorios(parameters),
            'servicios': disServico(parameters)
        }

    def add_data(self, parameters):
        dispatcher = self.dispatcher(parameters)
        try:
            query, values = dispatcher[parameters['table']].add_data()
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
        dispatcher = self.dispatcher(parameters)
        try:
            if parameters['table'] == 'medico' and parameters['id_medico'] == '':
                query = dispatcher[parameters['table']].get_all()

            else:
                query = dispatcher[parameters['table']].read_data()

            self.reConnect()
            results = self.executeQuery(query)

            if len(results) == 0:
                return {
                    '_status': 400,
                    'message': self.information['err_medico'],
                    'emptyArray': []
                }

            response = dispatcher[parameters['table']].response_data(
                results)

            return response

        except pymysql.MySQLError as e:
            self.errorResult(e)
        except Exception as e:
            self.errorResult(e)
            
    def update_data(self, parameters):
        dispatcher = self.dispatcher(parameters)
        try:
            # logger.info('Updating data...')
            query, values = dispatcher[parameters['table']].update_data()
            self.reConnect()
            self.cur.execute(query, values)
            self.conn.commit()
            return {
                '_status': 200,
                'message': 'Los datos se han actualizado correctamente'
            }
        except pymysql.MySQLError as e:
            self.errorResult(e)
        except Exception as e:
            self.errorResult(e)

    def delete_data(self, parameters):
        dispatcher = self.dispatcher(parameters)
        try:
            query = dispatcher[parameters['table']].delete_data()
            self.reConnect()
            self.cur.execute(query)
            self.conn.commit()
            return {
                '_status': 200,
                'message': 'Los datos se han eliminado de manera correcta'
            }
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
