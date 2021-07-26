from flask import Flask, request #, jsonify, make_response, render_template
from config import Config
from datetime import datetime
from json import loads
from flask_cors import CORS
import mysql.connector
from model import Dispatcher

app = Flask(__name__)
CORS(app)
config = Config()

connection = mysql.connector.connect(host=config.MYSQL_HOST,
                                     database=config.MYSQL_DB,
                                     user=config.MYSQL_USER,
                                     password=config.MYSQL_PASSWORD)

dispatcher = Dispatcher(connection)


@app.route('/ubigeo', methods=['POST'])
def getUbigeoByCod():
    payload = loads(request.data.decode('utf8').replace("'", '"'))
    # Se envía los parametros que recoge el endpoint y lo envía al dispatcher
    response = dispatcher.model(payload)
    # Validación de la respuesta
    return response


@app.route('/busquedaespecialista', methods=['POST'])
def busquedaespecialista():
    return "ok"


if __name__ == '__main__':
    app.run(port=3000, debug=True)
