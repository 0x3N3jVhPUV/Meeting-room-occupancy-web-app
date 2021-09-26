import os
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from collections import Counter

app = Flask(__name__)
CORS(app)

app.config["DEBUG"] = True
client = MongoClient(
    "mongodb+srv://test:test@cluster0.vwlml.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NONE"
)

db = client.occupancyRecords
collection = db.occupancy

def full_list_maker(sensors_store, ts_store):
    sensor_List = sensors_dict_maker(sensors_store)
    ts_List = ts_dict_maker(ts_store)
    Full_list = []
    Full_list.append(sensor_List)
    Full_list.append(ts_List)
    return Full_list


def sensors_dict_maker(data_store):
    dataJson = []
    for data in data_store:
        if data.get("sensor"):
            sensor = data["sensor"]
            dataJson.append(sensor)
    data = list(dict.fromkeys(dataJson))
    dataDict = {"sensors_list": data}
    return dataDict
    
def ts_dict_maker(data_store):
    dataJson = []
    for data in data_store:
        if data.get("Ts"):
            Ts = data["Ts"]
            dataJson.append(Ts)
    data = list(dict.fromkeys(dataJson))
    dataDict = {"ts_list": data}
    return dataDict


def dataJsonMaker(Data_store):
    dataJson = []
    for data in Data_store:
        id = data["_id"]
        sensor = data["sensor"]
        In = int(data["In"])
        Out = int(data["Out"])
        Ts = data["Ts"]
        dataDict = {"id": str(id), "sensor": sensor, "In": In, "Out": Out, "Ts": Ts}
        dataJson.append(dataDict)
    return dataJson

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
    db["Ts"].insert_one({"Ts": Ts})
    return jsonify(
        {
            "status": "Data is posted to MongoDB!",
            "In": In,
            "Out": Out,
            "sensor": sensor,
            "Ts": Ts,
        }
    )

# curl -X GET 'http://127.0.0.1:5000/api/occupancy'
# or
# curl --request GET 'http://127.0.0.1:5000/api/occupancy?sensor=XYZ'
# or
# curl --request GET 'http://127.0.0.1:5000/api/occupancy?sensor=XYZ&atInstant=2018-11-14T14:00:00Z'
@app.route("/api/occupancy", methods=["GET"])
def occupancy():
    sensor_name = request.args.get("sensor")
    ts_value = request.args.get("atInstant")

    data_store = db["data"].find()
    sensors_store = db["sensors"].find()
    ts_store = db["Ts"].find()

    dataJson = dataJsonMaker(data_store)
    c = Counter()
    Full_list = full_list_maker(sensors_store, ts_store)

    if sensor_name and ts_value:
        for elem in dataJson:
            if elem["sensor"] == sensor_name and elem["Ts"] == ts_value:
                inside = int(elem.get("In")) - int(elem.get("Out"))
                break
        Dict = {"inside": inside}
        Full_list.append(Dict)
        return jsonify(Full_list)
    elif sensor_name:
        for elem in dataJson:
            if elem["sensor"] == sensor_name:
                c.update(elem)
        inside = int(c.get("In")) - int(c.get("Out"))
        Dict = {"inside": inside}
        Full_list.append(Dict)
        return jsonify(Full_list)
    else:
        return jsonify(Full_list)


if __name__ == "__main__":
    app.debug = True
    app.run()
