import os
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from collections import Counter

app = Flask(__name__)
CORS(app)

# app.config["DEBUG"] = True
client = MongoClient(
    "mongodb+srv://test:test@cluster0.vwlml.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NONE"
)

db = client.occupancyRecords
collection = db.occupancy

# curl --header "Content-Type: application/json" -X POST -d '{"sensor":"abc","ts":"2018-11-14T13:34:49Z","in":3,"out":2}' http://127.0.0.1:5000/api/webhook
@app.route("/api/webhook", methods=["POST"])
def post_data():
    body = request.json
    In = body["in"]
    Out = body["out"]
    sensor = body["sensor"]
    Ts = body["ts"]
    db["data"].insert_one({"sensor": sensor, "In": In, "Out": Out, "Ts": Ts})
    db["sensors"].insert_one({"sensor": sensor})
    return jsonify(
        {
            "status": "Data is posted to MongoDB!",
            "In": In,
            "Out": Out,
            "sensor": sensor,
            "Ts": Ts,
        }
    )

# curl -X GET http://127.0.0.1:5000/api/occupancy
@app.route("/api/occupancy", methods=["GET"])
def make_sensor_list():
    sensors_store = db["sensors"].find()
    dataJson = []
    for data in sensors_store:
        sensor = data["sensor"]
        dataJson.append(sensor)
    sensor_List = list(dict.fromkeys(dataJson))
    return jsonify(sensor_List)


# curl --request GET http://127.0.0.1:5000/api/occupancy?sensor=XYZ
@app.route("/api/occupancy/<sensor>", methods=["GET"])
def get_data_by_sensor(sensor):
    global sensor_name
    sensor_name =  str(sensor)
    Data_store = db["data"].find()
    dataJson = []
    for data in Data_store:
        id = data["_id"]
        sensor = data["sensor"]
        In = int(data["In"])
        Out = int(data["Out"])
        Ts = data["Ts"]
        dataDict = {"id": str(id), "sensor": sensor, "In": In, "Out": Out, "Ts": Ts}
        dataJson.append(dataDict)

    c = Counter()
    for elem in dataJson:
        if elem["sensor"] == sensor_name:
            c.update(elem)
    
    inside = int(c.get('In')) - int(c.get('Out'))
    Dict = {
        "inside": inside,
    }
    print(Dict)
    return jsonify(Dict)


if __name__ == "__main__":
    app.debug = True
    app.run()
