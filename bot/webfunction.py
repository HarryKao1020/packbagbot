# ==================================================================
# =============================Setting==============================
# ==================================================================
from flask import Flask, request, jsonify, render_template
import db
import sqlite3
from selenium import webdriver
import requests
import json

# =====================================================
# =======================網頁機能=======================
# =====================================================

#===========獲得景點名稱===========
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

#===========獲得景點細項===========
def getwebDeatil(ID, TName):
    # url名字需要
    dt = ["detail1", "detail2", "detail3", "detail4", "detail5"]

    landmarks = getwebplace(ID, str(TName))

    # 把list轉成dict
    BigDetail = []
    for i in range(0, len(landmarks)):

        # print("景點:"+landmarks[i])
        mapUrl = getMap(landmarks[i])
        # print("MAPurl:"+mapUrl)

        if i < len(landmarks)-1:
            # 傳入地址，獲得行車時間
            addresses = db.getPlaceDetail([landmarks[i]])
            addresses2 = db.getPlaceDetail([landmarks[i+1]])
            Time = getTime(addresses[0], addresses2[0]) + '分鐘'
        else:
            addresses = db.getPlaceDetail([landmarks[i]])
            Time = "回家囉"

        newAddresses = list(filter(None, addresses))
        newAddresses.insert(0, landmarks[i])         # 把景點名稱也加進來
        newAddresses.insert(5, TName + "/" + dt[i])  # 加入URL 
        newAddresses.insert(6, mapUrl)               # 加入MapURL
        newAddresses.insert(7, Time)                 # 加入Time

        RawPlaceDetail = ['name', 'address','quality', 'tele', 'openTime', 'url', 'mapUrl', 'Time']
        dictDetail = dict(zip(RawPlaceDetail, newAddresses))
        BigDetail.append(dictDetail)

    return BigDetail

#===========取經緯度資料===========
def getLocation(location):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address=" + location + "&key=1201089449:AIzaSyBCfFGAnQ-o2WCGtwHA3USnMsZ7eB2lN60&language=zh-TW"
    print(url)

    r = requests.get(url, verify=False)

    list_of_dicts = r.json()
    latN = list_of_dicts["results"][0]["geometry"]["location"]["lat"] # 取經度
    lngN = list_of_dicts["results"][0]["geometry"]["location"]["lng"] # 取緯度

    print(latN,lngN)

#===========取得地圖資料===========
def getMap(loc):
    url = "http://maps.google.com/maps?f=q&hl=zh-TW&geocode=&q=" + loc
    return url

#===========取得前往時間===========
def getTime(origin, destination):
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + origin + "&destinations=" + destination + "=&key=AIzaSyBCfFGAnQ-o2WCGtwHA3USnMsZ7eB2lN60"
    r = requests.get(url, verify=False)
    list_of_dicts = r.json()
    # 取時間
    timer = list_of_dicts["rows"][0]["elements"][0]["duration"]["text"]
    timer = timer.split('min')[0] #去除min
    print(timer)
    return timer