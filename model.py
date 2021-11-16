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
    def __init__(self, parameters):
        self.mydb = DBMySql()
        self.mydb.initialize()
        self.conn = self.mydb.connect()
        self.cur = self.conn.cursor()
        self.param = parameters
        self.msg = ''

    def model(self):
        if self.param['type'] == 'Ubigeo':
            try:
                cubigeo = disUbigeo(self.param)
                ubigeos = self.executeQuery(cubigeo.read_data())
                return cubigeo.response_data(ubigeos)
            except Exception as e:
                self.msg = e
                self.errorResult()
            finally:
                if self.conn:
                    self.closeConnect()

        elif self.param['type'] == 'Medico':
            try:
                classMedico = disMedico(self.param)
                medicos = self.executeQuery(
                    classMedico.get_medico_by_especialidad())
                return classMedico.response_medico_by_especialidad(medicos)
            except Exception as e:
                self.msg = e
                self.errorResult()
            finally:
                if self.conn:
                    self.closeConnect()

        elif self.param['type'] == 'Login':
            try:
                classLogin = disLogin(self.param)
                results = self.executeQuery(classLogin.get_all())
                return classLogin.response_data(results)

            except Exception as e:
                self.msg = e
                self.errorResult()
            finally:
                if self.conn:
                    self.closeConnect()

    def dispatcher(self):
        return {
            'medico': disMedico(self.param),
            'enfermedades': disEnfermedades(self.param),
            'formacion': disFormacion(self.param),
            'consultorios': disConsultorios(self.param),
            'servicios': disServico(self.param),
            'especialidades': disEspecialidades(self.param),
            'especialidadmedico': disEspecialidadmedico(self.param),
            'prospecto': disProspecto(self.param)
        }

    def add_data(self):
        dis = self.dispatcher()
        try:
            query, values = dis[self.param['table']].add_data()
            self.reConnect()
            self.cur.execute(query, values)
            self.conn.commit()
            if self.param['table'] == 'prospecto' and self.param['estado'] == 'Aprobado':
                self.param['id_prospecto'] = self.cur.lastrowid
                query, values = dis['medico'].add_prospecto_medico(self.param)
                self.reConnect()
                self.cur.execute(query, values)
                self.conn.commit()
            return {
                '_status': 200,
                'message': 'Los datos de {}, se han registrado de manera correcta'.format(self.param['table'])
            }
        except (pymysql.MySQLError, Exception) as e:
            self.msg = e
            self.errorResult()

    def select_data(self):
        dis = self.dispatcher()
        try:
            if self.param['table'] == 'medico' and self.param['id_medico'] == '':
                query = dis[self.param['table']].get_all()
            else:
                query = dis[self.param['table']].read_data()

            self.reConnect()
            results = self.executeQuery(query)
            response = dis[self.param['table']].response_data(results)

            return response
        except (pymysql.MySQLError, Exception) as e:
            self.msg = e
            self.errorResult()

    def update_data(self):
        dis = self.dispatcher()
        try:
            # logger.info('Updating data...')
            query, values = dis[self.param['table']].update_data()
            self.reConnect()
            self.cur.execute(query, values)
            self.conn.commit()
            return {
                '_status': 200,
                'message': 'Los datos se han actualizado correctamente'
            }
        except (pymysql.MySQLError, Exception) as e:
            self.msg = e
            self.errorResult()

    def delete_data(self):
        dis = self.dispatcher()
        try:
            query = dis[self.param['table']].delete_data()
            self.reConnect()
            self.cur.execute(query)
            self.conn.commit()
            return {
                '_status': 200,
                'message': 'Los datos se han eliminado de manera correcta'
            }
        except (pymysql.MySQLError, Exception) as e:
            self.msg = e
            self.errorResult()

    def errorResult(self):
        return {
            '_status': 405,
            'message': 'Error en la ejecución, ' + str(self.msg)
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
