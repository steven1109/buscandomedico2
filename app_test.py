import mysql.connector
from config import Config
from flask import Flask, request
from json import loads
from regions.dispatcher_regions import Dispatcher

app = Flask(__name__)
config = Config()

connection = mysql.connector.connect(host=config.MYSQL_HOST,
                                     database=config.MYSQL_DB,
                                     user=config.MYSQL_USER,
                                     password=config.MYSQL_PASSWORD)

dispatcher = Dispatcher(connection)


@app.route('/ubigeo', methods=['POST'])
def endpointBuscandomedico():
    payload = loads(request.data.decode('utf8').replace("'", '"'))
    response = dispatcher.execute(payload)
    return response


if __name__ == "__main__":
    app.run(port=3000, debug=True)
