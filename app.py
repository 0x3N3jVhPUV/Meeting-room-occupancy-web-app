import os
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
app.config["DEBUG"] = True
client = MongoClient(
    "mongodb+srv://test:test@cluster0.vwlml.mongodb.net/?ssl=true&ssl_cert_reqs=CERT_NONE"
)
# client = MongoClient('mongodb+srv://test:test@cluster0.vwlml.mongodb.net/myFirstDatabase?retryWrites=true&w=majority')

db = client.occupancyRecords
collection = db.occupancy
CORS(app)


# curl -X GET http://192.168.1.16:5000/api/occupancy
# @app.route("/api/occupancy", methods=["GET"])
# def get_data():
#     print("data_store = ", data_store)
#     dataJson = []
#     for data in data_store:
#         In = data["in"]
#         Out = data["out"]
#         Sensor = data["sensor"]
#         Ts = data["ts"]
#         dataDict = {
#             "In": In,
#             "Out": Out,
#             "Sensor": Sensor,
#             "Ts": Ts,
#         }
#         dataJson.append(dataDict)
#     return jsonify(dataJson)


# curl --header "Content-Type: application/json" -X POST -d '{"sensor":"abc","ts":"2018-11-14T13:34:49Z","in":3,"out":2}' http://192.168.1.16:5000/api/webhook
@app.route("/api/webhook", methods=["POST"])
def post_data():
    body = request.json
    In = body["in"]
    Out = body["out"]
    Sensor = body["sensor"]
    Ts = body["ts"]
    db["data"].insert_one({"In": In, "out": out, "sensor": sensor, "Ts": Ts})
    return jsonify(
        {
            "status": "Data is posted to MongoDB!",
            "In": In,
            "out": out,
            "sensor": sensor,
            "Ts": Ts,
        }
    )


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", debug=True)

if __name__ == "__main__":
    app.debug = True
    app.run()
