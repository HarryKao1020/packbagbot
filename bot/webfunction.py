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

    landmarks = getwebplace(ID, TName)

    # 把list轉成dict
    BigDetail = []
    for i in range(0, len(landmarks)):
        addresses = db.getPlaceDetail([landmarks[i]])
        # print("景點:"+landmarks[i])
        mapUrl = getMap(landmarks[i])
        # print("MAPurl:"+mapUrl)
        newAddresses = list(filter(None, addresses))
        newAddresses.insert(0, landmarks[i])         # 把景點名稱也加進來
        newAddresses.insert(5, TName + "/" + dt[i])  # 加入URL 
        newAddresses.insert(6, mapUrl)               # 加入MapURL

        if i < len(landmarks)-1:
            Time = getTime(landmarks[i], landmarks[i+1]) + '分鐘'
        else:
            Time = "回家囉"

        newAddresses.insert(7, Time)

        RawPlaceDetail = ['name', 'address','quality', 'tele', 'openTime', 'url', 'mapUrl', 'Time']
        dictDetail = dict(zip(RawPlaceDetail, newAddresses))
        BigDetail.append(dictDetail)

    return BigDetail

#===========取經緯度資料===========
def getLocation(location):
    url = "https://maps.googleapis.com/maps/api/geocode/json?address="+location+"&key=AIzaSyDYnRmUfEmD5AHscwduwGgpyMPRHKxKwpc&language=zh-TW"
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
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + origin + "&destinations=" + destination + "=&key=AIzaSyAZZSdiWrwGceupgus3xLLNjcg6Vdi5TkQ"
    r = requests.get(url, verify=False)
    list_of_dicts = r.json()
    # 取時間
    timer = list_of_dicts["rows"][0]["elements"][0]["duration"]["text"]
    timer = timer.split('min')[0] #去除min
    print(timer)
    return timer
