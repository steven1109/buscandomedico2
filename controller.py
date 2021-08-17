from regions.dispatcher_regions import Dispatcher as disUbigeo
from medico.dispatcher_medico import Dispatcher as disMedico


class Controller:

    def __init__(self, connection):
        self.dispatcher = {
            'ubigeo': disUbigeo(connection),
            'medico': disMedico(connection)
        }

    def execute(self, payload):
        return self.dispatcher[payload['type']].execute(payload)
