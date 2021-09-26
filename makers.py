import os
import json
from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from collections import Counter

def full_List_Maker(sensors_store, ts_store):
    sensor_List = list_Maker(sensors_store)
    ts_List = list_Maker(ts_store)
    Full_list = []
    Full_list.append(sensor_List)
    Full_list.append(ts_List)
    return Full_list

def list_Maker(data_store):
    sensorJson = []
    tsJson = []
    for data in data_store:
        if data.get("sensor"):
            sensor = data["sensor"]
            sensorJson.append(sensor)
        elif data.get("Ts"):
            Ts = data["Ts"]
            tsJson.append(Ts)
    sensor_list = list(dict.fromkeys(sensorJson))
    ts_list = list(dict.fromkeys(tsJson))
    dataDict = {"sensors_list": sensor_list, "Ts_list": ts_list }
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