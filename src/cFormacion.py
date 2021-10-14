from datetime import datetime


class Formacion:
    def __init__(self, parameters):
        self.param = parameters

    def add_data(self):
        id_medico = self.param['id_medico']
        nom_centro = self.param['nom_centro']
        desc_formacion = self.param['desc_formacion']
        fec_anio_inicio = self.param['fec_anio_inicio']
        fec_anio_fin = self.param['fec_anio_fin']
        fec_creacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        query = ' INSERT INTO formacion (id_medico,nom_centro,desc_formacion,fec_anio_inicio,fec_anio_fin,fec_creacion)  ' \
            ' VALUES(%s,%s,%s,%s,%s,%s) '

        values = (id_medico, nom_centro, desc_formacion,
                  fec_anio_inicio, fec_anio_fin, fec_creacion)

        return query, values

    def read_data(self):
        query = ' select id_formacion,id_medico,nom_centro,desc_formacion,fec_anio_inicio,fec_anio_fin,fec_creacion ' \
            ' from formacion ' \
            ' where id_medico = {}'.format(
                str(self.param['id_medico']))

        return query

    def update_data(self):
        nom_centro = self.param['nom_centro']
        desc_formacion = self.param['desc_formacion']
        fec_anio_inicio = self.param['fec_anio_inicio']
        fec_anio_fin = self.param['fec_anio_fin']
        modification_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = 'UPDATE formacion SET nom_centro = %s, desc_formacion = %s, fec_anio_inicio = %s, fec_anio_fin = %s, fec_modificacion = %s ' \
            ' WHERE id_formacion = {}'.format(self.param['id_formacion'])
            
        values = (nom_centro, desc_formacion, fec_anio_inicio, fec_anio_fin, modification_date)
        
        return query, values

    def delete_data(self):
        return 'delete from formacion WHERE id_formacion = {}'.format(self.param['id_formacion'])

    def response_data(self, results):
        response = {
            '_status': 200,
            'formacionArray': list(
                map(lambda formacion: {
                    'id_formacion': int(formacion[0]),
                    'id_medico': int(formacion[1]),
                    'nom_centro': formacion[2],
                    'desc_formacion': formacion[3],
                    'fec_anio_inicio': str(formacion[4]),
                    'fec_anio_fin': str(formacion[5]),
                    'fec_creacion': str(formacion[6])
                }, results))
        }
        return response
