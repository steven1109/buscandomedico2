from datetime import datetime


class Prospecto:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        nombres = self.param['nombres']
        ape_paterno = self.param['ape_paterno']
        ape_materno = self.param['ape_materno']
        fec_nacimiento = self.param['fec_nacimiento']
        genero = self.param['genero']
        num_contacto = self.param['num_contacto']
        email_contacto = self.param['email_contacto']
        codigo_cmp = self.param['codigo_cmp']
        observacion = self.param['observacion']
        estado = self.param['estado']
        creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = ' INSERT INTO prospecto(nombres,ape_paterno,ape_materno,fec_nacimiento,genero,num_contacto,' \
                ' email_contacto,codigo_cmp,observacion,estado,fec_creacion) ' \
                ' VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'

        values = (nombres, ape_paterno, ape_materno, fec_nacimiento, genero, num_contacto, email_contacto,
                  codigo_cmp, observacion, estado, creation_date)

        return query, values

    def read_data(self):
        where = ' WHERE id_prospecto = {}'.format(
            self.param['id_prospecto']) if self.param['id_prospecto'] != '' else ''

        query = ' SELECT id_prospecto, nombres, ape_paterno, ape_materno, fec_nacimiento, genero, num_contacto,' \
                ' email_contacto, codigo_cmp, observacion, estado, fec_creacion, fec_modificacion' \
                ' FROM prospecto {};'.format(where)

        return query

    def update_data(self):
        nombres = self.param['nombres']
        ape_paterno = self.param['ape_paterno']
        ape_materno = self.param['ape_materno']
        fec_nacimiento = self.param['fec_nacimiento']
        genero = self.param['genero']
        num_contacto = self.param['num_contacto']
        email_contacto = self.param['email_contacto']
        codigo_cmp = self.param['codigo_cmp']
        observacion = self.param['observacion']
        estado = self.param['estado']
        modification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = ' UPDATE prospecto SET nombres = %s, ape_paterno = %s, ape_materno = %s, fec_nacimiento = %s, ' \
                ' genero = %s, num_contacto = %s, email_contacto = %s, codigo_cmp = %s, observacion = %s, estado = %s, ' \
                ' fec_modificacion = %s WHERE id_prospecto = {};'.format(
                    self.param['id_prospecto'])

        values = (nombres, ape_paterno, ape_materno, fec_nacimiento, genero, num_contacto, email_contacto,
                  codigo_cmp, observacion, estado, modification_date)

        return query, values

    def delete_data(self):
        query = 'DELETE FROM prospecto WHERE id_prospecto = {};'. format(
            self.param['id_prospecto'])

        return query

    def response_data(self, results):
        if len(results) == 0:
            response = {
                '_status': 404,
                'message': 'Error, No existen datos en la tabla {}'.format(self.param['table']),
                'emptyArray': []
            }
        else:
            response = {
                '_status': 200,
                'prospectoArray': list(
                    map(lambda prospecto: {
                        'id_prospecto': int(prospecto[0]),
                        'nombres': prospecto[1],
                        'ape_paterno': prospecto[2],
                        'ape_materno': prospecto[3],
                        'fec_nacimiento': str(prospecto[4]),
                        'genero': int(prospecto[5]),
                        'num_contacto': prospecto[6],
                        'email_contacto': prospecto[7],
                        'codigo_cmp': prospecto[8],
                        'observacion': prospecto[9],
                        'estado': prospecto[10]
                    }, results))
            }

        return response
