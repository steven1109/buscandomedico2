from regions.repository.bd_provincia import ProvinciaRepository
from logging import getLogger
log = getLogger(__name__)


class ProvinciaController:
    # TODO:
    # Llamadas a los eventos definidos en repository
    def __init__(self, conn):
        self.connection = conn
        self.cursor = self.connection.cursor()
        self.repository = ProvinciaRepository(self.cursor)

    def controller(self, parameters):
        if parameters['value'] != '':
            return self.repository.findByCod(parameters['value'])
        else:
            return self.repository.findAll()
