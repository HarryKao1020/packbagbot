from app import webUrl, webUserID, webtravelname, detailUrl
from flask import Flask, request, jsonify, render_template
import random
import db

# _name_ 代表目前執行的模組
application=Flask(__name__) 

# ------------- 程式區 -----------------------

#相關變數
#webUserID = UserID
#webtravelname = 自行命名的行程名
#webRandom = 避免行程名重複
#webUrl = 產生的網址 (UserID+自行命名的景點+亂數)
#addres = 地址
#star = 評分
#tele = 電話
#openTime = 營業時間
#placeDatail1
#placeDatail2
#placeDatail3
#placeDatail4
#placeDatail5

# --------URL=8個亂數+TNAME+1個亂數------------
# webUserID = UserID
# webtravelname = Tname
# webRandom = random.choice('123456789!abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@$%^&*qwertyuiopasdfghjklzxcvbnm')
# detailUrl = webtravelname+webRandom
# ramdomUserID = ''
# ramdomlist = []
# seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^()_-"

# for i in range(8):
#     ramdomlist.append(random.choice(seed))
#     ramdomUserID = ''.join(ramdomlist)

# webUrl =  "/" + ramdomUserID + "/" + webtravelname + webRandom
# print(webUrl)

# ----------------------------------------
# 函式裝飾:以函式為基礎 提供附加功能
@application.route("/",methods=['GET'])
def home():
    return render_template("index.html")



# 代表我們要處理的網站路徑
# 轉換成json格式(地圖經緯度)
# @application.route("/cities/all",methods=['GET'])
# def cities_all():
#     return jsonify(cities)


# ----------- 核心程式-- 景點上去index.html -------------------
@application.route(webUrl, methods=['GET'])
def all():
    #取出自行命名的行程名字
    Tname = db.getTnames([webUserID]) 

    # url名字需要
    dt=["detail1","detail2","detail3","detail4","detail5","detail6"]

    #取出景點名字
    Rawlandmarks = list(db.getPLACE([webUserID, webtravelname]))
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
        newAddresses.insert(5,detailUrl+"/"+dt[i]) #加入URL
        RawPlaceDetail = ['name','address', 'quality', 'tele', 'openTime','url']
        dictDetail=dict(zip(RawPlaceDetail,newAddresses))
        BigDetail.append(dictDetail)
        # print(newAddresses)   

    #計算共需要幾個景點細項頁面
    # detailNum = len(landmarks)
    # if detailNum

    return render_template("all.html", places = landmarks ,TravelName = Tname, ALLDetail = BigDetail,url=webUrl)


# ----------------------------共用---------------------------
#取出自行命名的行程名字
Tname = db.getTnames([webUserID]) 

#取出景點名字
Rawlandmarks = list(db.getPLACE([webUserID, webtravelname]))
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

# ------------------------------     Detail1 -----------------------------------------------------------
#帶入景點細項參數
@application.route( webUrl + "/detail1", methods=['GET'])
def detail1_all():
# -----第一個景點的個別詳細資料---------
    detail1=BigDetail[0]
    detail1Name=detail1['name']
    detail1Address=detail1['address']
    detail1Quality=detail1['quality']   
    detail1Tele=detail1['tele']
    detail1Opt=detail1['openTime']
    weekday=str(detail1Opt)
    weekDayStr=weekday.split('\n')


    return render_template("details1.html", places = landmarks ,TravelName = Tname, d1Name=detail1Name,d1Address=detail1Address,d1Quality=detail1Quality,d1Tele=detail1Tele,d1Opt=detail1Opt,opT=weekDayStr,url=webUrl)
#-----------------------------------------------------------  

# ------------------------------     Detail2 -----------------------------------------------------------
#帶入景點細項參數
@application.route(webUrl+"/detail2", methods=['GET'])
def detail2_all():
# -----第二個景點的個別詳細資料---------
    detail2=BigDetail[1]
    detail2Name=detail2['name']
    detail2Address=detail2['address']
    detail2Quality=detail2['quality']   
    detail2Tele=detail2['tele']
    detail2Opt=detail2['openTime']
    weekday=str(detail2Opt)
    weekDayStr=weekday.split('\n')


    return render_template("details2.html", places = landmarks ,TravelName = Tname, d2Name=detail2Name,d2Address=detail2Address,d2Quality=detail2Quality,d2Tele=detail2Tele,d2Opt=detail2Opt,opT=weekDayStr,url=webUrl)
#-----------------------------------------------------------  
# ------------------------------     Detail3 -----------------------------------------------------------
#帶入景點細項參數
@application.route(webUrl+"/detail3", methods=['GET'])
def detail3_all():
# -----第二個景點的個別詳細資料---------
    detail3=BigDetail[2]
    detail3Name=detail3['name']
    detail3Address=detail3['address']
    detail3Quality=detail3['quality']   
    detail3Tele=detail3['tele']
    detail3Opt=detail3['openTime']
    weekday=str(detail3Opt)
    weekDayStr=weekday.split('\n')


    return render_template("details3.html", places = landmarks ,TravelName = Tname, d3Name=detail3Name,d3Address=detail3Address,d3Quality=detail3Quality,d3Tele=detail3Tele,d3Opt=detail3Opt,opT=weekDayStr,url=webUrl)
#-----------------------------------------------------------  

# ------------------------------     Detail4 -----------------------------------------------------------
#帶入景點細項參數
@application.route(webUrl + "/detail4", methods=['GET'])
def detail4_all():
# -----第二個景點的個別詳細資料---------
    detail4=BigDetail[3]
    detail4Name=detail4['name']
    detail4Address=detail4['address']
    detail4Quality=detail4['quality']   
    detail4Tele=detail4['tele']
    detail4Opt=detail4['openTime']
    weekday=str(detail4Opt)
    weekDayStr=weekday.split('\n')


    return render_template("details4.html", places = landmarks ,TravelName = Tname, d4Name=detail4Name,d4Address=detail4Address,d4Quality=detail4Quality,d4Tele=detail4Tele,d4Opt=detail4Opt,opT=weekDayStr,url=webUrl)
#-----------------------------------------------------------  
# ------------------------------     Detail5 -----------------------------------------------------------
#帶入景點細項參數
@application.route(webUrl + "/detail5", methods=['GET'])
def detail5_all():
# -----第二個景點的個別詳細資料---------
    detail5=BigDetail[4]
    detail5Name=detail5['name']
    detail5Address=detail5['address']
    detail5Quality=detail5['quality']   
    detail5Tele=detail5['tele']
    detail5Opt=detail5['openTime']
    weekday=str(detail5Opt)
    weekDayStr=weekday.split('\n')


    return render_template("details5.html", places = landmarks ,TravelName = Tname, d5Name=detail5Name,d5Address=detail5Address,d5Quality=detail5Quality,d5Tele=detail5Tele,d5Opt=detail5Opt,opT=weekDayStr,url=webUrl)
#-----------------------------------------------------------  


print('http://127.0.0.1:5000' + webUrl )

# 如果test.py為主程式 讓Web API 跑起來
if __name__=="__main__":
    application.run()

