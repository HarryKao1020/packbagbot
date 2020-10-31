from flask import Flask, request, jsonify, render_template
import db
import sqlite3
from selenium import webdriver
import requests
import json
# _name_ 代表目前執行的模組
application = Flask(__name__)

def getwebplace(ID, TName):
    # 取出景點名字
    Rawlandmarks = db.getPLACE([ID, TName])
    # 過濾none值的所有景點
    landMarkArray = list(filter(None, Rawlandmarks))

    # 把'\r\n'都過濾
    landmarks = []
    for i in range(0, len(landMarkArray)):
        r = (str(landMarkArray[i])).rstrip('\r\n')
        landmarks.append(r)

    return landmarks

def getMap(loc):
    url="http://maps.google.com/maps?f=q&hl=zh-TW&geocode=&q="+loc
    return url


def getwebDeatil(ID, TName):
    # url名字需要
    dt = ["detail1", "detail2", "detail3", "detail4", "detail5", "detail6"]

    landmarks = getwebplace(ID, TName)

    # 把list轉成dict
    BigDetail = []
    for i in range(0, len(landmarks)):
        addresses = db.getPlaceDetail([landmarks[i]])
        print("景點:"+landmarks[i])
        mapUrl=getMap(landmarks[i])
        print("MAPurl:"+mapUrl)
        newAddresses = list(filter(None, addresses))
        newAddresses.insert(0, landmarks[i])  # 把景點名稱也加進來
        newAddresses.insert(5, TName + "/" + dt[i])  # 加入URL
        newAddresses.insert(6,mapUrl)
        RawPlaceDetail = ['name', 'address','quality', 'tele', 'openTime', 'url','mapUrl']
        dictDetail = dict(zip(RawPlaceDetail, newAddresses))
        BigDetail.append(dictDetail)
        # print(newAddresses)

    return BigDetail

print(getwebDeatil(1135510968,520))



