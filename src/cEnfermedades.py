from datetime import datetime


class Enfermedadestratadas:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        id_medico = self.param['id_medico']
        des_enfermedades = self.param['des_enfermedades']
        fec_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = ' INSERT INTO enfermedades_tratadas (id_medico, des_enfermedades, fec_creacion)  ' \
            ' VALUES(%s,%s,%s) '

        values = (id_medico, des_enfermedades, fec_creacion)

        return query, values

    def read_data(self):
        query = ' select id_enf_tratadas, id_medico, des_enfermedades, fec_creacion ' \
            ' from enfermedades_tratadas ' \
            ' where id_medico = {}'.format(
                str(self.param['id_medico']))

        return query

    def update_data(self):
        des_enfermedades = self.param['des_enfermedades']
        modification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = ' UPDATE enfermedades_tratadas SET des_enfermedades = %s, fec_modificacion = %s ' \
            ' WHERE id_enf_tratadas = {}'.format(self.param['id_enf_tratadas'])
            
        values = (des_enfermedades, modification_date)
        
        return query, values

    def delete_data(self):
        return 'delete from enfermedades_tratadas WHERE id_enf_tratadas = {}'.format(self.param['id_enf_tratadas'])

    def response_data(self, results):
        response = {
            '_status': 200,
            'enfermedadesArray': list(
                map(lambda enfermedad: {
                    'id_enf_tratadas': int(enfermedad[0]),
                    'id_medico': int(enfermedad[1]),
                    'des_enfermedades': enfermedad[2],
                    'fec_creacion': str(enfermedad[3])
                }, results))}

        return response
