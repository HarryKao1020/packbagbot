#==================================================================
#=============================Setting==============================
#==================================================================
from flask import Flask, request, jsonify, render_template
import db
import sqlite3

# _name_ 代表目前執行的模組
application=Flask(__name__) 

@application.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@application.route("/<webUserID>/<webtravelname>")   #傳入兩個參數
def all(webUserID, webtravelname):
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

    webUrl = webUserID + '/' + webtravelname

    return render_template("all.html", places = landmarks, TravelName = webtravelname, ALLDetail = BigDetail, url = webUrl)

#=====================================================
#=======================網頁機能=======================
#=====================================================
def getwebplace(ID, TName):
    #取出景點名字
    Rawlandmarks = db.getPLACE([ID, TName])
    # 過濾none值的所有景點
    landMarkArray = list(filter(None,Rawlandmarks))

    # 把'\r\n'都過濾
    landmarks=[]
    for i in range(0,len(landMarkArray)):
        r=(str(landMarkArray[i])).rstrip('\r\n')
        landmarks.append(r)

    return landmarks

def getwebDeatil(ID, TName):
    # url名字需要
    dt=["detail1","detail2","detail3","detail4","detail5","detail6"]

    landmarks = getwebplace(ID, TName)

    # 把list轉成dict
    BigDetail=[]
    for i in range(0,len(landmarks)):
        addresses= db.getPlaceDetail([landmarks[i]])
        newAddresses=list(filter(None,addresses))
        newAddresses.insert(0,landmarks[i]) #把景點名稱也加進來
        newAddresses.insert(5, TName + "/" + dt[i]) #加入URL
        RawPlaceDetail = ['name','address', 'quality', 'tele', 'openTime','url']
        dictDetail=dict(zip(RawPlaceDetail, newAddresses))
        BigDetail.append(dictDetail)
        # print(newAddresses) 
    
    return BigDetail

#================第一個景點的個別詳細資料================
@application.route("/<webUserID>/<webtravelname>" + "/detail1")
def detail1_all(webUserID, webtravelname):

    landmarks = getwebplace(webUserID, webtravelname)

    detail1 = getwebDeatil(webUserID, webtravelname)[0]
    detail1Name = detail1['name']
    detail1Address = detail1['address']
    detail1Quality = detail1['quality']   
    detail1Tele = detail1['tele']
    detail1Opt = detail1['openTime']
    weekday = str(detail1Opt)
    weekDayStr = weekday.split('\n')

    webUrl = webUserID + '/' + webtravelname

    return render_template("details1.html", places = landmarks ,TravelName = webtravelname, d1Name=detail1Name, d1Address=detail1Address, d1Quality=detail1Quality, d1Tele=detail1Tele, d1Opt=detail1Opt, opT=weekDayStr, url=webUrl)

#================第二個景點的個別詳細資料================
@application.route("/<webUserID>/<webtravelname>" +  "/detail2")
def detail2_all(webUserID, webtravelname):

    landmarks = getwebplace(webUserID, webtravelname)

    detail2 = getwebDeatil(webUserID, webtravelname)[0]
    detail2Name = detail2['name']
    detail2Address = detail2['address']
    detail2Quality = detail2['quality']   
    detail2Tele = detail2['tele']
    detail2Opt = detail2['openTime']
    weekday = str(detail2Opt)
    weekDayStr = weekday.split('\n')

    webUrl = webUserID + '/' + webtravelname

    return render_template("details2.html", places = landmarks ,TravelName = webtravelname, d1Name=detail2Name, d1Address=detail2Address, d1Quality=detail2Quality, d1Tele=detail2Tele, d1Opt=detail2Opt, opT=weekDayStr, url=webUrl)

#================第三個景點的個別詳細資料================
@application.route("/<webUserID>/<webtravelname>" +  "/detail3")
def detail3_all(webUserID, webtravelname):

    landmarks = getwebplace(webUserID, webtravelname)

    detail3 = getwebDeatil(webUserID, webtravelname)[0]
    detail3Name = detail3['name']
    detail3Address = detail3['address']
    detail3Quality = detail3['quality']   
    detail3Tele = detail3['tele']
    detail3Opt = detail3['openTime']
    weekday = str(detail3Opt)
    weekDayStr = weekday.split('\n')

    webUrl = webUserID + '/' + webtravelname

    return render_template("details3.html", places = landmarks ,TravelName = webtravelname, d1Name=detail3Name, d1Address=detail3Address, d1Quality=detail3Quality, d1Tele=detail3Tele, d1Opt=detail3Opt, opT=weekDayStr, url=webUrl)

#================第四個景點的個別詳細資料================
@application.route("/<webUserID>/<webtravelname>" +  "/detail4")
def detail4_all(webUserID, webtravelname):

    landmarks = getwebplace(webUserID, webtravelname)

    detail4 = getwebDeatil(webUserID, webtravelname)[0]
    detail4Name = detail4['name']
    detail4Address = detail4['address']
    detail4Quality = detail4['quality']   
    detail4Tele = detail4['tele']
    detail4Opt = detail4['openTime']
    weekday = str(detail4Opt)
    weekDayStr = weekday.split('\n')

    webUrl = webUserID + '/' + webtravelname

    return render_template("details4.html", places = landmarks ,TravelName = webtravelname, d1Name=detail4Name, d1Address=detail4Address, d1Quality=detail4Quality, d1Tele=detail4Tele, d1Opt=detail4Opt, opT=weekDayStr, url=webUrl)

#================第五個景點的個別詳細資料================
@application.route("/<webUserID>/<webtravelname>" +  "/detail5")
def detail5_all(webUserID, webtravelname):

    landmarks = getwebplace(webUserID, webtravelname)

    detail5 = getwebDeatil(webUserID, webtravelname)[0]
    detail5Name = detail5['name']
    detail5Address = detail5['address']
    detail5Quality = detail5['quality']   
    detail5Tele = detail5['tele']
    detail5Opt = detail5['openTime']
    weekday = str(detail5Opt)
    weekDayStr = weekday.split('\n')

    webUrl = webUserID + '/' + webtravelname

    return render_template("details5.html", places = landmarks ,TravelName = webtravelname, d1Name=detail5Name, d1Address=detail5Address, d1Quality=detail5Quality, d1Tele=detail5Tele, d1Opt=detail5Opt, opT=weekDayStr, url=webUrl)

#=====================================================
#=======================執行程式=======================
if __name__ == "__main__":
    application.run(host='127.0.0.1', port=80)