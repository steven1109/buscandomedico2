from datetime import datetime
import unicodedata


class Medico:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        if self.param['cod_departamento'] == "":
            return {
                '_status': 404,
                'message': 'Error, no ha seleccionado un departamento'
            }

        cod_departamento = self.param['cod_departamento']
        cod_provincia = self.param['cod_provincia']
        cod_distrito = self.param['cod_distrito']
        id_prospecto = self.param['id_prospecto']
        nombres = self.param['nombres']
        ape_paterno = self.param['ape_paterno']
        ape_materno = self.param['ape_materno']
        fec_nacimiento = self.param['fec_nacimiento']
        genero = self.param['genero']
        codigo_cmp = self.param['codigo_cmp']
        atiende_covid = 0 if int(self.param['atiende_covid']) == 0 else int(
            self.param['atiende_covid'])
        atiende_vih = 0 if int(self.param['atiende_vih']) == 0 else int(
            self.param['atiende_vih'])
        videollamada = 0 if int(self.param['videollamada']) == 0 else int(
            self.param['videollamada'])
        descripcion_profesional = self.param['descripcion_profesional']
        facebook = self.param['facebook']
        instagram = self.param['instagram']
        twitter = self.param['twitter']
        linkedin = self.param['linkedin']
        fec_colegiatura = self.param['fec_colegiatura']
        activo = self.param['activo']
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = ' INSERT INTO medico (cod_departamento,cod_provincia,cod_distrito,id_prospecto,nombres,ape_paterno,ape_materno,fec_nacimiento, ' \
            ' genero,codigo_cmp,fec_colegiatura,flag_atiende_covid,flag_Atiende_vih,flag_atiende_videollamada,comentario_personal,facebook, ' \
            ' instagram,twitter,linkedin,bol_activo,fec_creacion)  ' \
            ' VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '

        values = (cod_departamento, cod_provincia, cod_distrito, id_prospecto, nombres, ape_paterno, ape_materno, fec_nacimiento,
                  genero, codigo_cmp, fec_colegiatura, atiende_covid, atiende_vih, videollamada, descripcion_profesional, facebook, instagram,
                  twitter, linkedin, activo, creation_date)

        return query, values

    def read_data(self):
        query = ' select me.id_medico,me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.cod_departamento,me.cod_distrito,me.cod_provincia, ' \
            ' me.codigo_cmp,me.comentario_personal,es.des_especialidad,me.fec_nacimiento,es.id_especialidad,esme.codigo_rne,me.fec_colegiatura, ' \
            ' me.cod_departamento,me.cod_provincia,me.cod_distrito,us.des_correo,pu.des_perfil_usuario,me.flag_atiende_covid, ' \
            ' me.flag_Atiende_vih,me.flag_atiende_videollamada,me.facebook,me.instagram,me.twitter,me.linkedin ' \
            ' from medico me ' \
            ' left join especialidad_medico esme on me.id_medico = esme.id_medico ' \
            ' left join especialidad es on esme.id_especialidad = es.id_especialidad ' \
            ' left join usuario us on me.id_medico = us.id_medico ' \
            ' left join perfil_usuario pu on us.id_perfil_usuario = pu.id_perfil_usuario ' \
            ' where me.id_medico = {} ' \
            ' order by me.ape_materno;'.format(
                str(self.param['id_medico']))

        return query

    def update_data(self):
        cod_departamento = self.param['cod_departamento']
        cod_provincia = self.param['cod_provincia']
        cod_distrito = self.param['cod_distrito']
        id_prospecto = self.param['id_prospecto']
        nombres = self.param['nombres']
        ape_paterno = self.param['ape_paterno']
        ape_materno = self.param['ape_materno']
        fec_nacimiento = self.param['fec_nacimiento']
        genero = self.param['genero']
        codigo_cmp = self.param['codigo_cmp']
        atiende_covid = 0 if int(self.param['atiende_covid']) == 0 else int(
            self.param['atiende_covid'])
        atiende_vih = 0 if int(self.param['atiende_vih']) == 0 else int(
            self.param['atiende_vih'])
        videollamada = 0 if int(self.param['videollamada']) == 0 else int(
            self.param['videollamada'])
        descripcion_profesional = self.param['descripcion_profesional']
        facebook = None if self.param['facebook'] == '' else self.param['facebook']
        instagram = None if self.param['instagram'] == '' else self.param['instagram']
        twitter = None if self.param['twitter'] == '' else self.param['twitter']
        linkedin = None if self.param['linkedin'] == '' else self.param['linkedin']
        fec_colegiatura = self.param['fec_colegiatura']
        activo = self.param['activo']
        modification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = 'UPDATE medico SET cod_departamento = %s,cod_provincia = %s,cod_distrito = %s,id_prospecto = %s,nombres = %s,ape_paterno = %s,ape_materno = %s,fec_nacimiento = %s, ' \
            ' genero = %s,codigo_cmp = %s,fec_colegiatura = %s,flag_atiende_covid = %s,flag_Atiende_vih = %s,flag_atiende_videollamada = %s,comentario_personal = %s,facebook = %s, ' \
            ' instagram = %s,twitter = %s,linkedin = %s,bol_activo = %s,fec_modificacion = %s ' \
            ' WHERE id_medico = {}'.format(self.param['id_medico'])

        values = (cod_departamento, cod_provincia, cod_distrito, id_prospecto, nombres, ape_paterno, ape_materno, fec_nacimiento,
                  genero, codigo_cmp, fec_colegiatura, atiende_covid, atiende_vih, videollamada, descripcion_profesional, facebook, instagram,
                  twitter, linkedin, activo, modification_date)

        return query, values

    def delete_data(self):
        return 'UPDATE medico SET bol_activo = 0 WHERE id_medico = {}'.format(self.param['id_medico'])

    def get_all(self):
        query = ' select me.id_medico,me.nombres,me.ape_paterno,me.ape_materno,me.genero,me.cod_departamento,me.cod_distrito,me.cod_provincia, ' \
            ' me.codigo_cmp,me.comentario_personal,es.des_especialidad,me.fec_nacimiento,es.id_especialidad,esme.codigo_rne,me.fec_colegiatura, ' \
            ' me.cod_departamento,me.cod_provincia,me.cod_distrito,us.des_correo,pu.des_perfil_usuario,me.flag_atiende_covid, ' \
            ' me.flag_Atiende_vih,me.flag_atiende_videollamada,me.facebook,me.instagram,me.twitter,me.linkedin ' \
            ' from medico me ' \
            ' left join especialidad_medico esme on me.id_medico = esme.id_medico ' \
            ' left join especialidad es on esme.id_especialidad = es.id_especialidad ' \
            ' left join usuario us on me.id_medico = us.id_medico ' \
            ' left join perfil_usuario pu on us.id_perfil_usuario = pu.id_perfil_usuario ' \
            ' order by me.ape_materno;'

        return query

    def get_medico_by_especialidad(self):
        clausulas = ''
        if self.param['genero'] != "":
            clausulas += ' AND me.genero = {}'.format(
                int(self.param['genero']))

        if self.param['cod_departamento'] != "":
            clausulas += ' AND me.cod_departamento = "{}"'.format(
                self.param['cod_departamento'])

        if self.param['cod_provincia'] != "":
            clausulas += ' AND me.cod_provincia = "{}"'.format(
                self.param['cod_provincia'])

        if self.param['cod_distrito'] != "":
            clausulas += ' AND me.cod_distrito = "{}"'.format(
                self.param['cod_distrito'])

        if self.param['especialidad'] != "":
            name_specialization = unicodedata.normalize(
                'NFKD', self.param['especialidad']).encode('ASCII', 'ignore').upper().decode("utf-8")
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

        return query

    def response_data(self, results):
        print('Responses....')
        response = {
            '_status': 200,
            'medicosArray': list(
                map(lambda medicos: {
                    'id_medico': int(medicos[0]),
                    'perfil': medicos[19],
                    'welcome': ('Dra. ' if medicos[4] == 1 else 'Dr. ') +
                    medicos[1] + ', ' + medicos[2] + ' ' + medicos[3],
                    'nombre': medicos[1],
                    'ape_paterno': medicos[2],
                    'ape_materno': medicos[3],
                    'fec_nacimiento': str(medicos[11]),
                    'cmp': medicos[8],
                    'genero': medicos[4],
                    'id_especialidad': medicos[12],
                    'des_especialidad': medicos[10],
                    'rme': medicos[13],
                    'fec_colegiatura': str(medicos[14]),
                    'cod_departamento': medicos[15],
                    'cod_provincia': medicos[16],
                    'cod_distrito': medicos[17],
                    'correo': medicos[18],
                    'flag_atiende_covid': medicos[20],
                    'flag_Atiende_vih': medicos[21],
                    'flag_atiende_videollamada': medicos[22],
                    'facebook': medicos[23],
                    'instagram': medicos[24],
                    'twitter': medicos[25],
                    'linkedin': medicos[26]
                }, results))
        }

        return response
