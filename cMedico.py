from datetime import datetime


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
        activo = 1
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
            ' left join comentarios com on me.id_medico = com.id_medico ' \
            ' left join usuario us on me.id_medico = us.id_medico ' \
            ' left join perfil_usuario pu on us.id_perfil_usuario = pu.id_perfil_usuario ' \
            ' where me.id_medico = {} ' \
            ' order by me.ape_materno;'.format(
                str(self.param['id_medico']))

        return query

    def update_data(self):
        pass

    def delete_data(self):
        pass
