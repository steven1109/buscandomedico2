import mysql.connector
from config import Config
from flask import Flask, request
from json import loads
from controller import Controller

app = Flask(__name__)
config = Config()

connection = mysql.connector.connect(host=config.MYSQL_HOST,
                                     database=config.MYSQL_DB,
                                     user=config.MYSQL_USER,
                                     password=config.MYSQL_PASSWORD)

controller = Controller(connection)


@app.route('/ubigeo', methods=['POST'])
@app.route('/medico', methods=['POST'])
def buscandomedicos():
    payload = loads(request.data.decode('utf8').replace("'", '"'))
    response = controller.execute(payload)
    return response

# @app.route('/ubigeo', methods=['POST'])
# def endpointUbigeo():
#     payload = loads(request.data.decode('utf8').replace("'", '"'))
#     response = dispatcher.execute(payload)

#     res = controller._response(payload)
#     print(res)

#     return response


# @app.route('/medico', methods=['POST'])
# def endpointBuscandomedico():
#     payload = loads(request.data.decode('utf8').replace("'", '"'))
#     response = dis_medico.execute(payload)

#     res = controller.execute(payload)
#     print(res)

#     return response


if __name__ == "__main__":
    app.run(port=3000, debug=True)
