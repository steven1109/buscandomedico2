from flask import Flask, request, jsonify, make_response, render_template
import config
from datetime import datetime
from json import loads
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/departamento', methods=['POST'])
def getDepartmentById():
    payload = loads(request.data.decode('utf8').replace("'", '"'))
    if payload["valor"] != "" and payload["campo"] != "":
        condition = f'where {payload["campo"]} = "{payload["valor"]}";'
    else:
        condition = ""

    query = f'select * from {payload["table"]} {condition}'

    cur = config.db.cursor()
    cur.execute(query)
    departamentos = cur.fetchall()
    departamentosArray = {
        "depas": []
    }
    if len(departamentos) == 0:
        return {"_status": "Error, el código del departamento no existe"}

    for departamento in departamentos:
        departamentosArray["depas"].append(
            {
                "Código": departamento[1],
                "Descripción": departamento[2]
            }
        )

    return departamentosArray


@app.route('/provincia', methods=['POST'])
def getProvinceByIdDepartment():
    payload = loads(request.data.decode('utf8').replace("'", '"'))

    if payload["valor"] == "":
        return {"_status": "Error, debe mandar el código del departamento"}

    query = f'select id_provincia, cod_provincia, des_provincia from provincia where cod_departamento = "{payload["valor"]}";'
    cur = config.db.cursor()
    cur.execute(query)
    provincias = cur.fetchall()
    provinciasArray = {
        "provincias": []
    }
    if len(provincias) == 0:
        return {"_status": "Error, el código del departamento no existe "}

    for provincia in provincias:
        provinciasArray['provincias'].append(
            {
                "Código": provincia[1],
                "Descripción": provincia[2]
            }
        )

    return provinciasArray


if __name__ == '__main__':
    app.run(port=3000, debug=True)
