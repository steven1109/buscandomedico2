from flask import Flask, request, render_template, make_response, jsonify
from config import Config
from json import loads
from flask_cors import CORS
from model import Dispatcher

app = Flask(__name__)
CORS(app)
config = Config()
dispatcher = Dispatcher()


@app.route('/api/ubigeo', methods=['POST'])
@app.route('/api/busquedaespecialista', methods=['POST'])
@app.route('/api/login', methods=['POST'])
@app.route('/api/endpoints', methods=['POST'])
@app.route('/api/get_medico', methods=['POST'])
def endpointBuscandomedico():
    payload = loads(request.data.decode('utf8').replace("'", '"'))
    response = dispatcher.model(payload)
    return response


@app.route('/api/add', methods=['GET', 'POST'])
def adding_record():
    payload = loads(request.data.decode('utf8').replace("'", '"'))

    key = request.headers.get('Authorization', 'Fail')
    if key == "7AB8D23CA175610278D73DC419AA786D150C58EC9C80CCB4EB6FF5395246B640":
        # if request.method == 'GET':
        response = dispatcher.add_row(payload)
    else:
        response = make_response(
            jsonify(response="Unauthorized", status=401), 401)
    return response


if __name__ == '__main__':
    app.run(port=3000, debug=True)
