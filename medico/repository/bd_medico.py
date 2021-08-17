import unicodedata
from logging import getLogger
log = getLogger(__name__)


class MedicoRepository:
    def __init__(self, cursor):
        self.query_find = ''
        self.cursor = cursor
        self.nombres = ''
        self.ape_paterno = ''
        self.ape_materno = ''
        self.fec_nacimiento = ''
        self.genero = 0
        self.codigo_cmp = ''
        self.cod_departamento = ''
        self.cod_provincia = ''
        self.cod_distrito = ''
        self.flag_atiende_covid = 0
        self.flag_atiende_vih = 0
        self.flag_atiende_videollamada = 0
        self.facebook = ''
        self.instagram = ''
        self.twitter = ''
        self.linkedin = ''
        self.bol_activo = False

    def findByFilter(self, parameters):
        clausulas = ''
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

        self.query_find = ' select me.id_medico,me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.cod_departamento,me.cod_distrito,me.cod_provincia, ' \
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

        self.cursor.execute(self.query_find)
        return self.cursor.fetchall()

    def findAll(self):
        self.query_find = ' select me.id_medico,me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.cod_departamento,me.cod_distrito,me.cod_provincia, ' \
            ' me.codigo_cmp,me.comentario_personal,es.des_especialidad, ' \
            ' COUNT(com.id_medico) AS count_doc,  ' \
            ' CASE WHEN COUNT(com.id_medico) > 0 THEN SUM(com.puntaje) ELSE 0 END AS sum_com, ' \
            ' CASE WHEN COUNT(com.id_medico) > 0 THEN ROUND(AVG(com.puntaje),2) ELSE 0 END AS prom ' \
            ' from medico me ' \
            ' inner join especialidad_medico esme on me.id_medico = esme.id_medico ' \
            ' inner join especialidad es on esme.id_especialidad = es.id_especialidad ' \
            ' left join comentarios com on me.id_medico = com.id_medico ' \
            ' where me.bol_activo = 1 ' \
            ' group by me.id_medico,me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.cod_departamento,me.cod_distrito,me.cod_provincia, ' \
            ' me.codigo_cmp,me.comentario_personal,es.des_especialidad ' \
            ' order by me.ape_materno;'

        self.cursor.execute(self.query_find)
        return self.cursor.fetchall()

    def create(self, parameters):
        self.nombres = parameters['nombres']
        self.ape_paterno = parameters['ape_paterno']
        self.ape_materno = parameters['ape_materno']
        self.fec_nacimiento = parameters['fec_nacimiento']
        self.genero = parameters['genero']
        self.codigo_cmp = parameters['codigo_cmp']
        self.cod_departamento = parameters['cod_departamento']
        self.cod_provincia = parameters['cod_provincia']
        self.cod_distrito = parameters['cod_distrito']
        self.flag_atiende_covid = parameters['flag_atiende_covid']
        self.flag_atiende_vih = parameters['flag_atiende_vih']
        self.flag_atiende_videollamada = parameters['flag_atiende_videollamada']
        self.facebook = parameters['facebook']
        self.instagram = parameters['instagram']
        self.twitter = parameters['twitter']
        self.linkedin = parameters['linkedin']
        self.bol_activo = parameters['bol_activo']

        query_insert = 'INSERT INTO medico() VALUES (?)'
        self.cursor.execute(query_insert)

    def update(self, parameters):
        pass

    def deleteByCod(self, codigo):
        pass

    def deleteAll(self):
        pass
