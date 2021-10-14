# , redirect, send_file
from flask import Flask, request, render_template, make_response, jsonify
from config import Config
from json import loads
from flask_cors import CORS
from model import Dispatcher
# import utils
import os

app = Flask(__name__)
CORS(app)
config = Config()
dispatcher = Dispatcher()


# @app.route('/')
# def home():
#     return render_template('index.html')


# @app.route('/add_demo', methods=['POST'])
# def add_specialization():
#     files = request.files.getlist('files[]')
#     for file in files:
#         if file and utils.allowed_file(file.filename):
#             direction = '/home/steven.jefferson.ve/Pictures'
#             utils.upload_to_aws(os.path.join(
#                 direction, file.filename), 'photomedicos', str(file.filename))

#     return redirect('/')


# @app.route('/list')
# def list_contents():
#     el = utils.list_files('photomedicos')
#     sh = utils.show_image('photomedicos')
#     return render_template('show_content.html', elements=el, images=sh)


# @app.route("/download/<filename>", methods=['GET'])
# def download(filename):
#     if request.method == 'GET':
#         print(filename)
#         utils.download_file(str(filename), 'photomedicos')
#         # return send_file(output, as_attachment=True)
#         return render_template('/list')


@app.route('/api/ubigeo', methods=['POST'])
@app.route('/api/busquedaespecialista', methods=['POST'])
@app.route('/api/login', methods=['POST'])
def endpointBuscandomedico():
    payload = loads(request.data.decode('utf8').replace("'", '"'))
    response = dispatcher.model(payload)
    return response


@app.route('/api/add', methods=['GET', 'POST'])
@app.route('/api/read', methods=['GET', 'POST'])
@app.route('/api/update', methods=['GET', 'POST'])
@app.route('/api/delete', methods=['GET', 'POST'])
def adding_record():
    payload = loads(request.data.decode('utf8').replace("'", '"'))
    key = request.headers.get('Authorization', 'Fail')
    if key == "7AB8D23CA175610278D73DC419AA786D150C58EC9C80CCB4EB6FF5395246B640":
        action = request.base_url.split('/')[-1]
        if action == "add":
            response = dispatcher.add_data(payload)
        elif action == 'read':
            response = dispatcher.select_data(payload)
        elif action == 'update':
            response = dispatcher.update_data(payload)
        elif action == 'delete':
            response = dispatcher.delete_data(payload)

    else:
        response = make_response(
            jsonify(response="Unauthorized", status=401), 401)
    return response


if __name__ == '__main__':
    app.run(port=3000, debug=True)
