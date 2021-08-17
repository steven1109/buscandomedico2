from medico.repository.bd_medico import MedicoRepository


class MedicoController:

    def __init__(self, conn):
        self.connection = conn
        self.cursor = self.connection.cursor()
        self.repository = MedicoRepository(self.cursor)

    def controller(self, parameters):
        if parameters['genero'] != '' or parameters['cod_departamento'] != '' or \
                parameters['cod_provincia'] != '' or parameters['cod_distrito'] != '' or \
                parameters['especialidad'] != '':
            return self.repository.findByFilter(parameters)
        else:
            return self.repository.findAll()
