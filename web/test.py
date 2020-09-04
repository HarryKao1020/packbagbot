from flask import Flask, request,jsonify
from flask import render_template
import random
import db


# ---------------找出各景點----------------------------
Rawlandmarks = list(db.getPLACE(['1144120088','ASD']))
# 過濾none值的所有景點
landMarkArray = list(filter(None,Rawlandmarks))

webUserID='1144120088'
webtravelname = 'ASD'
# 把'\r\n'都過濾
landmarks=[]
for i in range(0,len(landMarkArray)):
    r=(str(landMarkArray[i])).rstrip('\r\n')
    landmarks.append(r)
dt=["detail1","detail2","detail3","detail4","detail5","detail6"]
# --------------把各景點detail分別裝進list---------------
BigDetail=[]
for i in range(0,len(landmarks)):
    addresses= db.getPlaceDetail([landmarks[i]])
    
    newAddresses=list(filter(None,addresses))
    
    
    newAddresses.insert(0,landmarks[i])
    newAddresses.insert(5,webUserID+"/"+webtravelname+"/"+dt[i])


    RawPlaceDetail = ['name','address', 'quality', 'tele', 'openTime','url']
        
    dictDetail=dict(zip(RawPlaceDetail,newAddresses))
    BigDetail.append(dictDetail)

print(BigDetail)

detail1=BigDetail[0]
# print(detail1)
weekday=str(detail1['openTime'])

weekDayStr=weekday.split('\n')
# print(weekDayStr)
    # # 只有她的地址
    # print(addresses[0])
    # # quality
    # print(addresses[1])
    # tel
    # print(addresses[2])
    # #opentime
    # print(addresses[3])

