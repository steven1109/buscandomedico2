from datetime import datetime


class Medico:
    def __init__(self, nombres='', ape_paterno='', ape_materno='',
                 fec_nacimiento='', genero=0, codigo_cmp='',
                 cod_departamento='', cod_provincia='', cod_distrito='',
                 flag_atiende_covid=0, flag_atiende_vih=0, flag_atiende_videollamada=0,
                 facebook='', instagram='', twitter='', linkedin='', bol_activo=False):
        self.nombres = nombres
        self.ape_paterno = ape_paterno
        self.ape_materno = ape_materno
        self.fec_nacimiento = fec_nacimiento
        self.genero = genero
        self.codigo_cmp = codigo_cmp
        self.cod_departamento = cod_departamento
        self.cod_provincia = cod_provincia
        self.cod_distrito = cod_distrito
        self.flag_atiende_covid = flag_atiende_covid
        self.flag_atiende_vih = flag_atiende_vih
        self.flag_atiende_videollamada = flag_atiende_videollamada
        self.facebook = facebook
        self.instagram = instagram
        self.twitter = twitter
        self.linkedin = linkedin
        self.bol_activo = bol_activo
        self.fec_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # getter methods
        def get_nombres(self):
            return self.nombres

        def get_ape_paterno(self):
            return self.ape_paterno

        def get_ape_materno(self):
            return self.ape_materno

        def get_fec_nacimiento(self):
            return self.fec_creacion

        def get_genero(self):
            return self.genero

        def get_codigo_cmp(self):
            return self.codigo_cmp

        def get_cod_departamento(self):
            return self.cod_departamento

        def get_cod_provincia(self):
            return self.cod_provincia

        def get_cod_distrito(self):
            return self.cod_distrito

        def get_flag_atiende_covid(self):
            return self.flag_atiende_covid

        def get_flag_atiende_vih(self):
            return self.flag_atiende_vih

        def get_flag_atiende_videollamada(self):
            return self.flag_atiende_videollamada

        def get_facebook(self):
            return self.facebook

        def get_instagram(self):
            return self.instagram

        def get_twitter(self):
            return self.twitter

        def get_linkedin(self):
            return self.linkedin

        def get_bol_activo(self):
            return self.bol_activo

        # setter methods
        def set_nombres(self, nombres):
            self.nombres = nombres

        def set_ape_paterno(self, ape_paterno):
            self.ape_paterno = ape_paterno

        def set_ape_materno(self, ape_materno):
            self.ape_materno = ape_materno

        def set_fec_nacimiento(self, fec_creacion):
            self.fec_creacion = fec_creacion

        def set_genero(self, genero):
            self.genero = genero

        def set_codigo_cmp(self, codigo_cmp):
            self.codigo_cmp = codigo_cmp

        def set_cod_departamento(self, cod_departamento):
            self.cod_departamento = cod_departamento

        def set_cod_provincia(self, cod_provincia):
            self.cod_provincia = cod_provincia

        def set_cod_distrito(self, cod_distrito):
            self.cod_distrito = cod_distrito

        def set_flag_atiende_covid(self, flag_atiende_covid):
            self.flag_atiende_covid = flag_atiende_covid

        def set_flag_atiende_vih(self, flag_atiende_vih):
            self.flag_atiende_vih = flag_atiende_vih

        def set_flag_atiende_videollamada(self, flag_atiende_videollamada):
            self.flag_atiende_videollamada = flag_atiende_videollamada

        def set_facebook(self, facebook):
            self.facebook = facebook

        def set_instagram(self, instagram):
            self.instagram = instagram

        def set_twitter(self, twitter):
            self.twitter = twitter

        def set_linkedin(self, linkedin):
            self.linkedin = linkedin

        def set_bol_activo(self, bol_activo):
            self.bol_activo = bol_activo
