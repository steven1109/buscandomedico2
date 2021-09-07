from flask import Flask, request, render_template  # , jsonify, make_response
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

dispatcher = Dispatcher()


# @app.route('/')
# def principal():
#     return render_template('ejemploToAWS/index.html')


@app.route('/api/ubigeo', methods=['POST'])
@app.route('/api/busquedaespecialista', methods=['POST'])
@app.route('/api/login', methods=['POST'])
@app.route('/api/endpoints', methods=['POST'])
def endpointBuscandomedico():
    payload = loads(request.data.decode('utf8').replace("'", '"'))
    response = dispatcher.model(payload)
    return response


if __name__ == '__main__':
    app.run(port=3000, debug=True)
