from flask import Flask, request, jsonify, make_response
import config
from datetime import datetime
from json import loads

app = Flask(__name__)


@app.route("/departamento", methods=['POST'])
def getProvinceByIdDepartment():
    payload = loads(request.data.decode('utf8').replace("'", '"'))
    if payload["valor"] != "" or payload["campo"] != "":
        condition = f'where {payload["campo"]} = "{payload["valor"]}";'
    else:
        condition = ""

    query = f'select * from {payload["table"]} {condition}'

    cur = config.db.cursor()
    cur.execute(query)
    departamentos = cur.fetchall()
    departamentosArray= {
        "depas": []
    }

    for departamento in departamentos:
        departamentosArray["depas"].append(
            {
                "Código": departamento[1],
                "Descripción": departamento[2]
            }
        )

    return departamentosArray


if __name__ == '__main__':
    app.run(port=3000, debug=True)
