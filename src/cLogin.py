from config import Config
from cryptography.fernet import Fernet
import string
import random
from datetime import datetime

characters = list(string.ascii_letters + string.digits + "@$")


def decrypt(message):
    key = Config.TOKEN.encode()  # Fernet.generate_key()
    fernet = Fernet(key)
    return fernet.decrypt(message.encode()).decode()


def encrypted(message):
    key = Config.TOKEN.encode()  # Fernet.generate_key()
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())


def generate_random_password():
    # length of password from the user
    length = 8
    # shuffling the characters
    random.shuffle(characters)
    # picking random characters from the list
    password = []
    for i in range(length):
        password.append(random.choice(characters))
    # shuffling the resultant password
    random.shuffle(password)
    # converting the list to string
    # printing the list
    return "".join(password)


class Login:
    def __init__(self, parameters):
        self.param = parameters

    def add_user(self):
        user = self.param['email_contacto']
        id_medico = self.param['id_medico']
        password_generate = "123456"  # generate_random_password()
        password_enconde = encrypted(password_generate)
        password_no_byte = str(password_enconde, 'utf-8')
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = ' insert into usuario(id_medico, id_perfil_usuario, des_correo, des_pass, fec_creacion) ' \
                ' value (%s,%s,%s,%s,%s)'

        values = (id_medico, 2, user, password_no_byte, creation_date)

        return query, values, password_generate

    def get_all(self):
        query = ' select us.id_medico,pu.des_perfil_usuario,us.des_correo,us.des_pass,me.nombres,me.ape_paterno, ' \
                ' me.ape_materno,me.genero,me.fec_nacimiento,me.codigo_cmp,es.id_especialidad, ' \
                ' es.des_especialidad,esme.codigo_rne,pu.id_perfil_usuario ' \
                ' from usuario us ' \
                ' inner join perfil_usuario pu on us.id_perfil_usuario = pu.id_perfil_usuario ' \
                ' left join medico me on us.id_medico = me.id_medico ' \
                ' left join especialidad_medico esme on me.id_medico = esme.id_medico ' \
                ' left join especialidad es on esme.id_especialidad = es.id_especialidad;'
        return query

    def response_data(self, results):
        response = {}
        i = 0
        for result in results:
            if self.param['user'] == result[2] and decrypt(result[3]) == self.param['pass']:
                i += 1
                if result[1] == 'admin':
                    response = {
                        '_status': 200,
                        'id_medico': result[0],
                        'perfil': result[1],
                        'welcome': 'Administrador',
                        'nombre': 'Administrador',
                        'ape_paterno': '',
                        'ape_materno': '',
                        'fec_nacimiento': '',
                        'cmp': '',
                        'genero': '',
                        'id_especialidad': '',
                        'des_especialidad': '',
                        'rme': '',
                        'id_perfil_usuario': result[13]
                    }
                else:
                    response = {
                        '_status': 200,
                        'id_medico': result[0],
                        'perfil': result[1],
                        'welcome':
                            ('Dra. ' if result[7] == 1 else 'Dr. ') +
                            result[4] + ', ' + result[5] + ' ' + result[6],
                        'nombre': result[4],
                        'ape_paterno': result[5],
                        'ape_materno': result[6],
                        'fec_nacimiento': str(result[8]),
                        'cmp': result[9],
                        'genero': result[7],
                        'id_especialidad': result[10],
                        'des_especialidad': result[11],
                        'rme': result[12],
                        'id_perfil_usuario': result[13]
                    }
                break

        if i == 0:
            response = {
                '_status': 404,
                'result': 'El usuario o la contraseña ingresada es incorrecta.'
            }

        return response
