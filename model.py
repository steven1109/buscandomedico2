from config import DBMySql
import pymysql
from src.cMedico import Medico as disMedico
from src.cEnfermedades import Enfermedadestratadas as disEnfermedades
from src.cFormacion import Formacion as disFormacion
from src.cConsultorios import Consultorio as disConsultorios
from src.cServicios import Servicios as disServico
from src.cLogin import Login as disLogin
from src.cUbigeo import Ubigeo as disUbigeo
from src.cEspecialidades import Especialidades as disEspecialidades
from src.cEspecialidadMedico import EspecialidadMedico as disEspecialidadmedico
from src.cProspecto import Prospecto as disProspecto


# from loguru import logger


class Dispatcher:
    def __init__(self):
        self.mydb = DBMySql()
        self.mydb.initialize()
        self.conn = self.mydb.connect()
        self.cur = self.conn.cursor()

    def model(self, parameters):
        if parameters['type'] == 'Ubigeo':
            try:
                cubigeo = disUbigeo(parameters)
                ubigeos = self.executeQuery(cubigeo.read_data())
                return cubigeo.response_data(ubigeos)
            except Exception as e:
                self.errorResult(e)
            finally:
                if self.conn:
                    self.closeConnect()

        elif parameters['type'] == 'Medico':
            try:
                classMedico = disMedico(parameters)
                medicos = self.executeQuery(
                    classMedico.get_medico_by_especialidad())
                return classMedico.response_medico_by_especialidad(medicos)
            except Exception as e:
                self.errorResult(e)
            finally:
                if self.conn:
                    self.closeConnect()

        elif parameters['type'] == 'Login':
            try:
                classLogin = disLogin(parameters)
                results = self.executeQuery(classLogin.get_all())
                return classLogin.response_data(results)

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
            'servicios': disServico(parameters),
            'especialidades': disEspecialidades(parameters),
            'especialidadmedico': disEspecialidadmedico(parameters),
            'prospecto': disProspecto(parameters)
        }

    def add_data(self, parameters):
        dispatcher = self.dispatcher(parameters)
        try:
            query, values = dispatcher[parameters['table']].add_data()
            self.reConnect()
            self.cur.execute(query, values)
            self.conn.commit()
            if parameters['table'] == 'prospecto' and parameters['estado'] == 'Aprobado':
                parameters['id_prospecto'] = self.cur.lastrowid
                query, values = dispatcher['medico'].add_prospecto_medico(parameters)
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
