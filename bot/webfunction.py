#==================================================================
#=============================Setting==============================
#==================================================================
from flask import Flask, request, jsonify, render_template
import random
import db

from app import logger
from app import NAMING, DIRECTION, COUNTY, TYPE_ONE, TYPE_TWO, TYPE_THREE, TRAFFIC, SEARCH_PLACE, PLACE, PLACE_TWO,HISTORY
from app import travelname, cntplace, tmpplace, placebuttontmp, tmpplacedetail, tmpregion, tmptypes, tmpcounty
from app import webUrl, webUserID, webtravelname, webRandom, webUrl, detailUrl
from place.PAPI import getNear, getPlace, getSearch

# _name_ 代表目前執行的模組
application=Flask(__name__) 

# #取出自行命名的行程名字
# Tname = db.getTnames([webUserID]) 

# #取出景點名字
# Rawlandmarks = db.getPLACE([webUserID, webtravelname])
# # 過濾none值的所有景點
# landMarkArray = list(filter(None,Rawlandmarks))

# # 把'\r\n'都過濾
# landmarks=[]
# for i in range(0,len(landMarkArray)):
#     r=(str(landMarkArray[i])).rstrip('\r\n')
#     landmarks.append(r)

# # 把list轉成dict
# BigDetail=[]
#     for i in range(0,len(landmarks)):
#         addresses= db.getPlaceDetail([landmarks[i]])
#         newAddresses=list(filter(None,addresses))
#         newAddresses.insert(0,landmarks[i]) #把景點名稱也加進來
#         newAddresses.insert(5,webtravelname+"/"+dt[i]) #加入URL
#         RawPlaceDetail = ['name','address', 'quality', 'tele', 'openTime','url']
#         dictDetail=dict(zip(RawPlaceDetail,newAddresses))
#         BigDetail.append(dictDetail)

# --------URL=使用者ID+TNAME ------------
webUserID = '1144120088'
webtravelname = '放棄'
# webRandom = random.choice('123456789!@$%^&*_qwertyuiopasdfghjklzxcvbnm')
webUrl =  "/" + webUserID + "/" + webtravelname
print(webUrl)
# 函式裝飾:以函式為基礎 提供附加功能
@application.route("/",methods=['GET'])
def home():
    return render_template("index.html")
#=====================================================
#=======================網頁機能=======================
#=====================================================

@application.route(webUrl, methods=['GET'])
def all():
    #取出自行命名的行程名字
    Tname = db.getTnames([webUserID]) 

    # url名字需要
    dt=["detail1","detail2","detail3","detail4","detail5","detail6"]

    #取出景點名字
    Rawlandmarks = db.getPLACE([webUserID, webtravelname])
    # 過濾none值的所有景點
    landMarkArray = list(filter(None,Rawlandmarks))

    # 把'\r\n'都過濾
    landmarks=[]
    for i in range(0,len(landMarkArray)):
        r=(str(landMarkArray[i])).rstrip('\r\n')
        landmarks.append(r)

    # 把list轉成dict
    BigDetail=[]
    for i in range(0,len(landmarks)):
        addresses= db.getPlaceDetail([landmarks[i]])
        newAddresses=list(filter(None,addresses))
        newAddresses.insert(0,landmarks[i]) #把景點名稱也加進來
        newAddresses.insert(5,webtravelname+"/"+dt[i]) #加入URL
        RawPlaceDetail = ['name','address', 'quality', 'tele', 'openTime','url']
        dictDetail=dict(zip(RawPlaceDetail,newAddresses))
        BigDetail.append(dictDetail)
        # print(newAddresses)   

    #計算共需要幾個景點細項頁面
    # detailNum = len(landmarks)
    # if detailNum

    return render_template("all.html", places = landmarks ,TravelName = Tname, ALLDetail = BigDetail,url=webUrl)

#=======================================================
#========================景點細項========================
#=======================================================
# ----------------------------共用---------------------------
#取出自行命名的行程名字
Tname = db.getTnames([webUserID]) 

#取出景點名字
Rawlandmarks = db.getPLACE([webUserID, webtravelname])
# 過濾none值的所有景點
landMarkArray = list(filter(None,Rawlandmarks))

# 把'\r\n'都過濾
landmarks=[]
for i in range(0,len(landMarkArray)):
    r=(str(landMarkArray[i])).rstrip('\r\n')
    landmarks.append(r)

# 把list轉成dict
BigDetail=[]
for i in range(0,len(landmarks)):
    addresses= db.getPlaceDetail([landmarks[i]])
    newAddresses=list(filter(None,addresses))
    newAddresses.insert(0,landmarks[i]) #把景點名稱也加進來
    

    RawPlaceDetail = ['name','address', 'quality', 'tele', 'openTime']
    dictDetail=dict(zip(RawPlaceDetail,newAddresses))
    BigDetail.append(dictDetail)



#================第一個景點的個別詳細資料================
@application.route( webUrl + "/detail1", methods=['GET'])
def detail1_all():

    detail1=BigDetail[0]
    detail1Name=detail1['name']
    detail1Address=detail1['address']
    detail1Quality=detail1['quality']   
    detail1Tele=detail1['tele']
    detail1Opt=detail1['openTime']
    weekday=str(detail1Opt)
    weekDayStr=weekday.split('\n')

    return render_template("details1.html", places = landmarks ,TravelName = Tname, d1Name=detail1Name,d1Address=detail1Address,d1Quality=detail1Quality,d1Tele=detail1Tele,d1Opt=detail1Opt,opT=weekDayStr,url=webUrl)

#================第二個景點的個別詳細資料================
@application.route( webUrl + "/detail2", methods=['GET'])
def detail2_all():

    detail2=BigDetail[1]
    detail2Name=detail2['name']
    detail2Address=detail2['address']
    detail2Quality=detail2['quality']   
    detail2Tele=detail2['tele']
    detail2Opt=detail2['openTime']
    weekday=str(detail2Opt)
    weekDayStr=weekday.split('\n')

    return render_template("details2.html", places = landmarks ,TravelName = Tname, d2Name=detail2Name,d2Address=detail2Address,d2Quality=detail2Quality,d2Tele=detail2Tele,d2Opt=detail2Opt,opT=weekDayStr,url=webUrl)

#================第三個景點的個別詳細資料================
@application.route( webUrl + "/detail3", methods=['GET'])
def detail3_all():

    detail3=BigDetail[2]
    detail3Name=detail3['name']
    detail3Address=detail3['address']
    detail3Quality=detail3['quality']   
    detail3Tele=detail3['tele']
    detail3Opt=detail3['openTime']
    weekday=str(detail3Opt)
    weekDayStr=weekday.split('\n')

    return render_template("details3.html", places = landmarks ,TravelName = Tname, d3Name=detail3Name,d3Address=detail3Address,d3Quality=detail3Quality,d3Tele=detail3Tele,d3Opt=detail3Opt,opT=weekDayStr,url=webUrl)

#================第四個景點的個別詳細資料================
@application.route( webUrl + "/detail4", methods=['GET'])
def detail4_all():

    detail4=BigDetail[3]
    detail4Name=detail4['name']
    detail4Address=detail4['address']
    detail4Quality=detail4['quality']   
    detail4Tele=detail4['tele']
    detail4Opt=detail4['openTime']
    weekday=str(detail4Opt)
    weekDayStr=weekday.split('\n')

    return render_template("details4.html", places = landmarks ,TravelName = Tname, d4Name=detail4Name,d4Address=detail4Address,d4Quality=detail4Quality,d4Tele=detail4Tele,d4Opt=detail4Opt,opT=weekDayStr,url=webUrl)

#================第五個景點的個別詳細資料================
@application.route( webUrl + "/detail5", methods=['GET'])
def detail5_all():

    detail5=BigDetail[3]
    detail5Name=detail5['name']
    detail5Address=detail5['address']
    detail5Quality=detail5['quality']   
    detail5Tele=detail5['tele']
    detail5Opt=detail5['openTime']
    weekday=str(detail5Opt)
    weekDayStr=weekday.split('\n')

    return render_template("details5.html", places = landmarks ,TravelName = Tname, d5Name=detail5Name,d5Address=detail5Address,d5Quality=detail5Quality,d5Tele=detail5Tele,d5Opt=detail5Opt,opT=weekDayStr,url=webUrl)

#=====================================================
#=======================執行程式=======================
if __name__=="__main__":
    application.run(port=80)


print('http://127.0.0.1:80/' + webUrl + "/detail1")