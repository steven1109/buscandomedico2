from flask import Flask, request, make_response, jsonify
from config import Config
from json import loads
from flask_cors import CORS
from model import Dispatcher

app = Flask(__name__)
CORS(app)
config = Config()


@app.route('/api/ubigeo', methods=['POST'])
@app.route('/api/busquedaespecialista', methods=['POST'])
@app.route('/api/login', methods=['POST'])
def endpointBuscandomedico():
    payload = loads(request.data.decode('utf8').replace("'", '"'))
    dispatcher = Dispatcher(payload)
    response = dispatcher.model()
    return response


@app.route('/api/add', methods=['GET', 'POST'])
@app.route('/api/read', methods=['GET', 'POST'])
@app.route('/api/update', methods=['GET', 'POST'])
@app.route('/api/delete', methods=['GET', 'POST'])
def adding_record():
    response = {}
    payload = loads(request.data.decode('utf8').replace("'", '"'))
    dispatcher = Dispatcher(payload)
    key = request.headers.get('Authorization', 'Fail')
    if key == "7AB8D23CA175610278D73DC419AA786D150C58EC9C80CCB4EB6FF5395246B640":
        action = request.base_url.split('/')[-1]
        if action == "add":
            response = dispatcher.add_data()
        elif action == 'read':
            response = dispatcher.select_data()
        elif action == 'update':
            response = dispatcher.update_data()
        elif action == 'delete':
            response = dispatcher.delete_data()

    else:
        response = make_response(
            jsonify(response="Unauthorized", status=401), 401)

    return response


if __name__ == '__main__':
    app.run(port=3000, debug=True)
