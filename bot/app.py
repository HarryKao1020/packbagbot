#引入機器人基礎機能
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, Dispatcher, CallbackQueryHandler

import configparser
import logging
import random
from os import path
from selenium import webdriver
from flask import Flask, request, render_template
import requests



import db
from place.PAPI import getNear, getPlace, getSearch

#=====================================================
#=======================Setting=======================
#=====================================================
#Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Initial Flask app
application = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))

NAMING, DIRECTION, COUNTY, TYPE_ONE, TYPE_TWO, TYPE_THREE, TRAFFIC, SEARCH_PLACE, PLACE, PLACE_TWO,HISTORY = range(11)
travelname     = {}  #紀錄使用者當前行程名稱
cntplace       = {}  #紀錄使用者安排景點數量
tmpplace       = {}  #暫存使用者選擇景點
placebuttontmp = {}  #暫存使用者按鈕資料
tmpplacedetail = {}  #紀錄地點詳細資訊
tmpregion      = {}  #紀錄地區
tmptypes       = {}  #紀錄類型次數
tmpcounty      = {}  #紀錄縣市
tmplat         = {}  #紀錄緯度
tmplng         = {}  #紀錄經度
#===============================================
#===================天氣用參數===================
#===============================================
city_code_list={  #各縣市ID
    "基隆":"10017", "台北":"63", "新北":"65", "桃園":"68", "新竹":"10018", "苗栗":"10005", "台中":"66", "南投":"10008", "彰化":"10007", "雲林":"10009", "嘉義":"10020", "台南":"67", "高雄":"64", "屏東":"10013", "台東":"10014", "花蓮":"10015", "宜蘭":"10002",
}

#===============================================
#===================網頁用參數===================
#===============================================
webUserID = ''     #webUserID = UserID
webtravelname = '' #webtravelname = 自行命名的行程名
webRandom = ''     #webRandom = 避免行程名重複
webUrl = ''        #webUrl = 產生的網址 (UserID+自行命名的景點+亂數)
detailUrl = ''     #detailUrl = 用來產生詳細景點資訊URL

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

# =====================================================
# ======================網頁首頁========================
# =====================================================
@application.route("/", methods=['GET'])
def home():
    return render_template("index.html")

@application.route("/<webUserID>/<webtravelname>")  # 傳入兩個參數
def all(webUserID, webtravelname):

    landmarks = getwebplace(webUserID, webtravelname)
    BigDetail = getwebDeatil(webUserID, webtravelname)
    webUrl = webUserID + '/' + webtravelname

    return render_template("all.html", places=landmarks, TravelName=webtravelname, ALLDetail=BigDetail, url=webUrl)

# ================第一個景點的個別詳細資料================
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

    return render_template("details1.html", places=landmarks, TravelName=webtravelname, d1Name=detail1Name, d1Address=detail1Address, d1Quality=detail1Quality, d1Tele=detail1Tele, d1Opt=detail1Opt, opT=weekDayStr, url=webUrl)

# ================第二個景點的個別詳細資料================
@application.route("/<webUserID>/<webtravelname>" + "/detail2")
def detail2_all(webUserID, webtravelname):

    landmarks = getwebplace(webUserID, webtravelname)

    detail2 = getwebDeatil(webUserID, webtravelname)[1]
    detail2Name = detail2['name']
    detail2Address = detail2['address']
    detail2Quality = detail2['quality']
    detail2Tele = detail2['tele']
    detail2Opt = detail2['openTime']
    weekday = str(detail2Opt)
    weekDayStr = weekday.split('\n')

    webUrl = webUserID + '/' + webtravelname

    return render_template("details2.html", places=landmarks, TravelName=webtravelname, d2Name=detail2Name, d2Address=detail2Address, d2Quality=detail2Quality, d2Tele=detail2Tele, d2Opt=detail2Opt, opT=weekDayStr, url=webUrl)

# ================第三個景點的個別詳細資料================
@application.route("/<webUserID>/<webtravelname>" + "/detail3")
def detail3_all(webUserID, webtravelname):

    landmarks = getwebplace(webUserID, webtravelname)

    detail3 = getwebDeatil(webUserID, webtravelname)[2]
    detail3Name = detail3['name']
    detail3Address = detail3['address']
    detail3Quality = detail3['quality']
    detail3Tele = detail3['tele']
    detail3Opt = detail3['openTime']
    weekday = str(detail3Opt)
    weekDayStr = weekday.split('\n')

    webUrl = webUserID + '/' + webtravelname

    return render_template("details3.html", places=landmarks, TravelName=webtravelname, d3Name=detail3Name, d3Address=detail3Address, d3Quality=detail3Quality, d3Tele=detail3Tele, d3Opt=detail3Opt, opT=weekDayStr, url=webUrl)

# ================第四個景點的個別詳細資料================
@application.route("/<webUserID>/<webtravelname>" + "/detail4")
def detail4_all(webUserID, webtravelname):

    landmarks = getwebplace(webUserID, webtravelname)

    detail4 = getwebDeatil(webUserID, webtravelname)[3]
    detail4Name = detail4['name']
    detail4Address = detail4['address']
    detail4Quality = detail4['quality']
    detail4Tele = detail4['tele']
    detail4Opt = detail4['openTime']
    weekday = str(detail4Opt)
    weekDayStr = weekday.split('\n')

    webUrl = webUserID + '/' + webtravelname

    return render_template("details4.html", places=landmarks, TravelName=webtravelname, d3Name=detail4Name, d1Address=detail4Address, d1Quality=detail4Quality, d1Tele=detail4Tele, d1Opt=detail4Opt, opT=weekDayStr, url=webUrl)

# ================第五個景點的個別詳細資料================
@application.route("/<webUserID>/<webtravelname>" + "/detail5")
def detail5_all(webUserID, webtravelname):

    landmarks = getwebplace(webUserID, webtravelname)

    detail5 = getwebDeatil(webUserID, webtravelname)[4]
    detail5Name = detail5['name']
    detail5Address = detail5['address']
    detail5Quality = detail5['quality']
    detail5Tele = detail5['tele']
    detail5Opt = detail5['openTime']
    weekday = str(detail5Opt)
    weekDayStr = weekday.split('\n')

    webUrl = webUserID + '/' + webtravelname

    return render_template("details5.html", places=landmarks, TravelName=webtravelname, d1Name=detail5Name, d1Address=detail5Address, d1Quality=detail5Quality, d1Tele=detail5Tele, d1Opt=detail5Opt, opT=weekDayStr, url=webUrl)


#===============================================
#=================== bot app ===================
#===============================================


@application.route('/hook', methods=['POST'])
def webhook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        dispatcher.process_update(update)
    return 'ok'


#===============================================
#===================機器人指令===================
#===============================================
def help_handler(bot, update): #/help 功能介紹
    update.message.reply_text('指令教學 \n/letsgo 立刻開始使用 \n/history 查詢歷史行程 \n/restart 遇到問題時刷新機器人')

def greet(bot, update):        #/start 機器人打招呼 
    update.message.reply_text('HI~我是旅泊包🎒 \n 我能依照你的喜好，推薦熱門景點給你')
    update.message.reply_text('準備要去旅行了嗎 ٩(ˊᗜˋ*)و \n立即輸入 /letsgo 開始使用！\n 如果要參考歷史行程請輸入 /history')

def restart(bot,update):       #/restart
    UserID = [update.message.from_user['id']]
    update.message.reply_text('完成')
    db.Deleterecord(UserID)
    return ConversationHandler.END

def warnnn(bot,update):
    reply_text=["(๑•́ ₃ •̀๑)旅泊包不懂","( ˘･з･)這是什麼意思","旅泊包沒學過這個( ´•̥̥̥ω•̥̥̥` )"]
    i = random.randint(0,3)
    update.message.reply_text(reply_text[i])

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

#===============================================
#=================history_conv==================
def history(bot, update):        #/history 查詢歷史行程
    UserID = update.message.from_user['id']

    Tnames = db.getTnames([UserID]) #出來是 tunlp ex:[('name1',),('name2',)]
    if Tnames:
        reply = '這是你過去安排的行程:\n'
        keyboard = []

        for Tname in Tnames:
            keyboard.append([InlineKeyboardButton(Tname[0], callback_data=Tname[0])],)

        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(reply,reply_markup=reply_markup)
    else:
        reply = '你還沒有安排拉'
        update.message.reply_text(reply)
        return ConversationHandler.END
    return HISTORY

def history_output(bot, update): #/history 查詢歷史行程：列出歷史行程的景點
    query = update.callback_query
    UserID = query.from_user['id']
    Tname = query.data
    
    landmarks = db.getPLACE([UserID,Tname])
    i = 1
    place_output = ""
    for landmark in landmarks:
        if landmark:
            place_output += str(i) +". "+landmark + "\n"
            i += 1
        else:
            break

    query.edit_message_text(place_output)
    return ConversationHandler.END

#===================================================================
#===========================機器人核心機能===========================
#===================================================================

def naming(bot, update):  #行程名稱取名
    logger.info("username: %s start",update.message.from_user)
    update.message.reply_text('先替這次的行程取個名字吧ε٩(๑> ₃ <)۶з')
    return NAMING

def start(bot, update): #選擇區域
    UserID = update.message.from_user['id']
    if update.message.text != '/return':
        travelname.update( { UserID : update.message.text} )
    
    logger.info("username: %s start",update.message.from_user)
    keyboard = [
        [InlineKeyboardButton("北部", callback_data='North'),
        InlineKeyboardButton("中部", callback_data='Central')],
        [InlineKeyboardButton("南部", callback_data='South'),
        InlineKeyboardButton("東部", callback_data='East')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('請問這次要去哪裡玩呢？',reply_markup=reply_markup)
    return DIRECTION

#================ 選擇縣市 ================
def selcounty(bot, update): #選擇縣市
    UserID = update.callback_query.from_user['id']
    query = update.callback_query
    
    tmpregion.update( {UserID:query.data} )
    query.answer()

    if tmpregion[UserID] == 'North':
        keyboard = [
            [InlineKeyboardButton("基隆", callback_data="基隆")],
            [InlineKeyboardButton("台北", callback_data="台北")],
            [InlineKeyboardButton("新北", callback_data="新北")],
            [InlineKeyboardButton("桃園", callback_data="桃園")],
            [InlineKeyboardButton("新竹", callback_data="新竹")]
        ]
    elif tmpregion[UserID] == 'Central':
        keyboard = [
        [InlineKeyboardButton("苗栗", callback_data="苗栗")],
        [InlineKeyboardButton("台中", callback_data="台中")],
        [InlineKeyboardButton("彰化", callback_data="彰化")],
        [InlineKeyboardButton("南投", callback_data="南投")],
        [InlineKeyboardButton("雲林", callback_data="雲林")]
    ]
    elif tmpregion[UserID] == 'South':
        keyboard = [
        [InlineKeyboardButton("嘉義", callback_data="嘉義")],
        [InlineKeyboardButton("台南", callback_data="台南")],
        [InlineKeyboardButton("高雄", callback_data="高雄")],
        [InlineKeyboardButton("屏東", callback_data="屏東")]
    ]
    elif tmpregion[UserID] == 'East':
        keyboard = [
        [InlineKeyboardButton("宜蘭", callback_data="宜蘭")],
        [InlineKeyboardButton("花蓮", callback_data="花蓮")],
        [InlineKeyboardButton("台東", callback_data="台東")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="請選擇縣市：",
        reply_markup=reply_markup
    )
    
    return COUNTY

def button(bot, update):  #確定選擇縣市
    UserID = update.callback_query.from_user['id']
    query = update.callback_query
    logger.info("username: %s chooses %s",update.callback_query.from_user['id'],query.data)
    tmpcounty.update( {UserID:query.data} )
    
    reply_text=["我也喜歡"+query.data+"🙆",
                "我超愛"+query.data+"👏",
                query.data+"確實是個好玩的地方👍"]
    i = random.randint(0,2)
    query.edit_message_text(reply_text[i]+"\n確認地點沒問題的話請幫我點選👇\n /chooseOK\n"+"如果想更換地點請幫我選👇\n /return\n")
    
    return COUNTY

#================ 景點類型(選三個) ================
def type_one(bot, update):
    UserID = update.message.from_user['id']

    db.setTname([UserID,travelname[UserID]]) #儲存旅遊名稱
    db.setCOUNTY([tmpcounty[UserID], UserID, travelname[UserID]]) #儲存縣市

    reply_keyboard=[['特色商圈','古蹟廟宇'],['人文藝術','景觀風景'],['休閒農業','戶外休閒'],['主題樂園']]
    update.message.reply_text('請問有什麼想去的景點類型呢？',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TYPE_ONE

def type_two(bot, update):
    UserID = update.message.from_user['id']
    Text = update.message.text
    Text = Text.replace(" ","")
    db.setTYPE_one([Text,UserID,travelname[UserID]])

    reply_keyboard=[['特色商圈','古蹟廟宇'],['人文藝術','景觀風景'],['休閒農業','戶外休閒'],['主題樂園'],['/done']]
    update.message.reply_text(f'你選擇的是「{Text}」，\n還有其他有興趣的類型嗎？\n如果沒有，請幫我選擇「/done」',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    if update.message.text != "/done":
        logger.info("%s is choose %s", update.message.from_user, update.message.text)

    return TYPE_TWO

def type_three(bot, update):
    UserID = update.message.from_user['id']
    Text = update.message.text
    Text = Text.replace(" ","")
    db.setTYPE_two([Text,UserID,travelname[UserID]])
    
    reply_keyboard=[['特色商圈','古蹟廟宇'],['人文藝術','景觀風景'],['休閒農業','戶外休閒'],['主題樂園'],['/done']]
    update.message.reply_text(f'你選擇的是「{Text}」，\n還有其他有興趣的類型嗎？\n如果沒有，請幫我選擇「/done」',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    if update.message.text != "/done":
        logger.info("%s is choose %s", update.message.from_user, update.message.text)

    return TYPE_THREE

#================ 交通方式 ================
def traffic(bot, update):
    UserID = update.message.from_user['id']
    Text = update.message.text
    cntplace.update( {UserID:1} )
    print(Text)
    if Text != '/done':
        Text = Text.replace(" ","")
        db.setTYPE_three([Text,UserID,travelname[UserID]])

    logger.info("type is %s form %s",update.message.text,update.message.from_user)
    reply_keyboard=[['大眾運輸🚌','其他🚂']]
    update.message.reply_text('想如何前往呢？',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TRAFFIC

def traffic2(bot, update):
    UserID = update.message.from_user['id']
    Text = update.message.text
    cntplace.update( {UserID:1} )
   

    logger.info("type is %s form %s",update.message.text,update.message.from_user)
    if tmpcounty[UserID] == "宜蘭" or tmpcounty[UserID] == "花蓮" or tmpcounty[UserID] == "台東" or tmpcounty[UserID] == "屏東" or tmpcounty[UserID] == "南投" or tmpcounty[UserID] == "基隆":
        reply_keyboard=[['客運🚌','火車🚂']]
    else:
        reply_keyboard=[['客運🚌','火車🚂','高鐵🚅']]
    update.message.reply_text('想如何前往呢？',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TRAFFIC

#================ 選擇景點(第一個) ================
def confirmbutton(bot, update):
    UserID = update.callback_query.from_user['id'] 
    query = update.callback_query
    print(tmpplace[UserID])
    
    db.setPlace(cntplace[UserID],[ tmpplace[UserID],UserID,travelname[UserID] ])
    print(tmpplacedetail[UserID])
    db.setPlacedetail(tmpplacedetail[UserID])

    cntplace[UserID]+=1
    print(cntplace[UserID])
    
    query.edit_message_text(text="如果要繼續選景點請輸入「 /next 」，\n如果完成行程請輸入「 /done 」")
    return PLACE

def placedetail(bot, update):  
    UserID = update.callback_query.from_user['id'] 
    query = update.callback_query
    query.answer()
    
    detail=getPlace(query.data)
    name = detail['name']
    rating = str(detail['rating'])
    address = detail['formatted_address']
    lat = detail['lat']
    lng = detail['lng']


    try:
        detail['weekday_text']
    except:
        time = "尚未提供營業時間" + "\n"
    else:
        time =  detail['weekday_text'][0]+"\n"+detail['weekday_text'][1]+"\n"+detail['weekday_text'][2]+"\n"+detail['weekday_text'][3]+"\n"+detail['weekday_text'][4]+"\n"+detail['weekday_text'][5]+"\n"+detail['weekday_text'][6]+"\n"

    try:
        detail['formatted_phone_number']
    except:
        phone = "尚未提供電話" + "\n"
    else:
        phone = detail['formatted_phone_number']

    tmpplace.update( {UserID:name} )
    tmpplacedetail.update( {UserID:[name,address,rating,phone,time]} )
    tmplat.update( {UserID:lat} )
    tmplng.update( {UserID:lng} )
    
    keyboard = [
        [InlineKeyboardButton("上一頁", callback_data="上一頁")],
        [InlineKeyboardButton("加入景點", callback_data=str(confirmbutton))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    query.edit_message_text(
        text="🔹名稱: "+name+"\n"+
        "🔹評價"+rating+" / 5\n"+
        "🔹地址: "+address+"\n"+
        "🔹電話："+phone+"\n"
        "🔹營業時間: \n"+ time
        ,
        reply_markup=reply_markup
    )

def returnplace(bot, update):
    UserID = update.callback_query.from_user['id']
    keyboard = placebuttontmp[UserID]
    query = update.callback_query
    markup = InlineKeyboardMarkup(keyboard)
    print(markup)
    query.edit_message_text('想開車去哪裡玩呢？',reply_markup=markup)

    return PLACE

#================ 選擇景點(第二個~結束) ================
def place_choose(bot, update):
    UserID = update.message.from_user['id']
    logger.info("%s prees 自行前往", UserID)

    types = db.getTYPE([UserID,travelname[UserID]])
    county = db.getCOUNTY([UserID,travelname[UserID]])
    try:
        lat = tmplat[UserID]
    except:
        lat = 0
    try:
        lng = tmplng[UserID]
    except:
        lng = 0
    loc = {'lat':lat,'lng':lng}
    print(types)
    if ((len(types)-1) == 0):
        i = 0
    else:
        i = random.randint(0,len(types)-1)
        while types[i]==None:
            i = random.randint(0,len(types)-1)
            
    print(types[i])
    
    places = getNear(county[0],types[i],loc) #取得景點名稱
    
    button = []
    for name in places:
        button.append([InlineKeyboardButton(name['name'], callback_data=name['place_id'])],)
    
    keyboard = button
    placebuttontmp.update({UserID:keyboard})
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('下列景點想去哪裡玩呢？',reply_markup=markup)

    return PLACE

def place_fork(bot,update):
    UserID = update.message.from_user['id']
    Text = update.message.text
    county = tmpcounty[UserID]
    logger.info("%s prees 自行搜尋景點", UserID)
    if county == "台北":
        if Text == "客運🚌":
            tmplat.update( {UserID:25.049320} )
            tmplng.update( {UserID:121.518621} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:25.047814} )
            tmplng.update( {UserID:121.516995} )
        else:
            tmplat.update( {UserID:25.047814} )
            tmplng.update( {UserID:121.516995} )
    elif county == "新北":
        if Text == "客運🚌":
            tmplat.update( {UserID:25.015554} )
            tmplng.update( {UserID:121.464969} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:25.015733} )
            tmplng.update( {UserID:121.463927} )
        else:
            tmplat.update( {UserID:25.014181} )
            tmplng.update( {UserID:121.463628} )
    elif county == "基隆":
        if Text == "客運🚌":
            tmplat.update( {UserID:25.132090} )
            tmplng.update( {UserID:121.739545} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:25.130151} )
            tmplng.update( {UserID:121.736903} )   
    elif county == "桃園":
        if Text == "客運🚌":
            tmplat.update( {UserID:24.953382} )
            tmplng.update( {UserID:121.224074} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:24.953475} )
            tmplng.update( {UserID:121.225736} )
        else:
            tmplat.update( {UserID:25.013033} )
            tmplng.update( {UserID:121.214855} )
    elif county == "新竹":
        if Text == "客運🚌":
            tmplat.update( {UserID:24.801126} )
            tmplng.update( {UserID:120.972365} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:24.801638} )
            tmplng.update( {UserID:120.971695} )
        else:
            tmplat.update( {UserID:24.808065} )
            tmplng.update( {UserID:121.040410} )
    elif county == "苗栗":
        if Text == "客運🚌":
            tmplat.update( {UserID:24.569533} )
            tmplng.update( {UserID:120.822915} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:24.570097} )
            tmplng.update( {UserID:120.822502} )
        else:
            tmplat.update( {UserID:24.605722} )
            tmplng.update( {UserID:120.825364} )
    elif county == "台中":
        if Text == "客運🚌":
            tmplat.update( {UserID:24.138225} )
            tmplng.update( {UserID:120.686876} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:24.136781} )
            tmplng.update( {UserID:120.822502} )
        else:
            tmplat.update( {UserID:24.111751} )
            tmplng.update( {UserID:120.615812} )
    elif county == "彰化":
        if Text == "客運🚌":
            tmplat.update( {UserID:23.962469} )
            tmplng.update( {UserID:120.568966} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:24.081675} )
            tmplng.update( {UserID:120.538539} )
        else:
            tmplat.update( {UserID:23.874338} )
            tmplng.update( {UserID:120.574738} )
    elif county == "南投":
        if Text == "客運🚌":
            tmplat.update( {UserID:23.905656} )
            tmplng.update( {UserID:120.689121} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:23.826967} )
            tmplng.update( {UserID:120.784819} )
    elif county == "雲林":
        if Text == "客運🚌":
            tmplat.update( {UserID:23.800189} )
            tmplng.update( {UserID:120.462193} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:23.711684} )
            tmplng.update( {UserID:120.541344} )
        else:
            tmplat.update( {UserID:23.735727} )
            tmplng.update( {UserID:120.415990} )
    elif county == "嘉義":
        if Text == "客運🚌":
            tmplat.update( {UserID:23.480174} )
            tmplng.update( {UserID:120.439450} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:23.479129} )
            tmplng.update( {UserID:120.441149} )
        else:
            tmplat.update( {UserID:23.453381} )
            tmplng.update( {UserID:120.323794} )
    elif county == "台南":
        if Text == "客運🚌":
            tmplat.update( {UserID:23.002249} )
            tmplng.update( {UserID:120.209059} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:22.997142} )
            tmplng.update( {UserID:120.212948} )
        else:
            tmplat.update( {UserID:22.924770} )
            tmplng.update( {UserID:120.285664} )
    elif county == "高雄":
        if Text == "客運🚌":
            tmplat.update( {UserID:22.637837} )
            tmplng.update( {UserID:120.303772} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:22.639344} )
            tmplng.update( {UserID:120.302461} )
        else:
            tmplat.update( {UserID:22.687204} )
            tmplng.update( {UserID:120.307615} )
    elif county == "屏東":
        if Text == "客運🚌":
            tmplat.update( {UserID:22.669372} )
            tmplng.update( {UserID:120.485327} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:22.668852} )
            tmplng.update( {UserID:120.486442} )
    elif county == "花蓮":
        if Text == "客運🚌":
            tmplat.update( {UserID:23.993399} )
            tmplng.update( {UserID:121.603858} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:23.993855} )
            tmplng.update( {UserID:121.602220} )
    elif county == "宜蘭":
        if Text == "客運🚌":
            tmplat.update( {UserID:24.750899} )
            tmplng.update( {UserID:121.759273} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:24.754673} )
            tmplng.update( {UserID:121.758048} )
    elif county == "台東":
        if Text == "客運🚌":
            tmplat.update( {UserID:22.752829} )
            tmplng.update( {UserID:121.147286} )
        elif Text == "火車🚂":
            tmplat.update( {UserID:22.793155} )
            tmplng.update( {UserID:121.123530} )


    update.message.reply_text('想要自己選擇景點請輸入景點名稱\n如果希望由旅泊包安排請點選👇\n/go')
    

    return SEARCH_PLACE
    
def search_placedetail(bot, update):  
    UserID = update.message.from_user['id']
    Text = update.message.text
    Text = Text.replace(" ","")
    
    detail=getSearch(Text)['result']
    name = detail['name']
    address = detail['formatted_address']

    try:
        detail['rating']
    except:
        rating = "暫無資料"
    else:
        rating = str(detail['rating']) 

    try:
        detail['weekday_text']
    except:
        time = "尚未提供營業時間" + "\n"
    else:
        time =  detail['weekday_text'][0]+"\n"+detail['weekday_text'][1]+"\n"+detail['weekday_text'][2]+"\n"+detail['weekday_text'][3]+"\n"+detail['weekday_text'][4]+"\n"+detail['weekday_text'][5]+"\n"+detail['weekday_text'][6]+"\n"

    try:
        detail['formatted_phone_number']
    except:
        phone = "尚未提供電話" + "\n"
    else:
        phone = detail['formatted_phone_number']


    tmpplace.update( {UserID:name} )
    tmpplacedetail.update( {UserID:[name,address,rating,phone,time]} )
    
    keyboard = [
        [InlineKeyboardButton("上一頁", callback_data="上一頁")],
        [InlineKeyboardButton("加入景點", callback_data=str(search_confirmbutton))],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        text="🔹名稱: "+name+"\n"+
        "🔹評價"+rating+" / 5\n"+
        "🔹地址: "+address+"\n"+
        "🔹電話："+phone+"\n"
        "🔹營業時間: \n"+ time
        ,
        reply_markup=reply_markup
    )

    
def search_confirmbutton(bot, update):
    UserID = update.callback_query.from_user['id'] 
    query = update.callback_query
    print(tmpplace[UserID])
    
    db.setPlace(cntplace[UserID],[ tmpplace[UserID],UserID,travelname[UserID] ])
    print(tmpplacedetail[UserID])
    db.setPlacedetail(tmpplacedetail[UserID])

    cntplace[UserID]+=1
    print(cntplace[UserID])
    
    query.edit_message_text(text="如果要繼續輸入景點直接填寫，\n如果由旅泊包安排請輸入「 /done 」")
    return SEARCH_PLACE

#================ bot 完成行程 ================
def done(bot,update):
    UserID = update.message.from_user['id']
    landmarks = db.getPLACE([UserID,travelname[UserID]])
    
    i = 1
    place_output = ""
    for landmark in landmarks:
        if landmark:
            place_output += str(i) +". "+landmark + "\n"
            i += 1
        else:
            break

    webUrl = '/' + str(UserID) + '/' + travelname[UserID]

    update.message.reply_text('旅泊包幫你安排好行程嘍')
    update.message.reply_text(place_output)
    update.message.reply_text('http://127.0.0.1:5000' + webUrl)
    update.message.reply_text('希望你喜歡旅泊包安排的行程🐾\n祝你玩得愉快！')
    print('http://127.0.0.1' + webUrl )

    getWeather(tmpcounty[UserID], update)
    
    return ConversationHandler.END

#===============================================
#===================天氣用方法===================
#===============================================
def getWeather(address, update):
    home_page = 'https://www.cwb.gov.tw/V8/C/W/County/County.html?CID='
    city_code = city_code_list[address] #與city_code_list的縣市資料對比數字
    url = home_page + city_code
    driver = webdriver.Chrome()
    driver.get(url) #啟動Chrome
    weatherAll = driver.find_element_by_xpath('/html/body/div/div/div/ul').text
    weatherDeatil = driver.find_element_by_xpath('/html/body/div/div/div/div/a').text
    driver.close() #關閉Chrome

    update.message.reply_text(weatherAll)
    update.message.reply_text(address + '的天氣狀況：' + weatherDeatil)

    return

#===============================================
#===================網頁用方法===================
#===============================================
# def getUserwebURL(UserID, travelname):
#     #產生亂數URL提供給使用者
#     webUserID = UserID
#     webtravelname = travelname
#     webRandom = random.choice('123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@$%^&*qwertyuiopasdfghjklzxcvbnm')
#     detailUrl = webtravelname + webRandom
#     ramdomUserID = ''
#     ramdomlist = []

#     seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
#     for i in range(8):
#         ramdomlist.append(random.choice(seed))
#         ramdomUserID = ''.join(ramdomlist)

#     Url =  "/" + ramdomUserID + "/" + webtravelname + webRandom

#     return Url

#=======================================================================
#==============================機器人主程式==============================
#=======================================================================
conv_handler = ConversationHandler(
        entry_points=[CommandHandler('letsgo', naming)],

        states={
            NAMING:[MessageHandler(Filters.text, start),],
            DIRECTION: [
                        CallbackQueryHandler(selcounty),
                        ],
            COUNTY: [ CallbackQueryHandler(start, pattern='^' + str(start) + '$'),
                        CallbackQueryHandler(button),
                        MessageHandler(Filters.regex('^(/chooseOK)$'), type_one),
                        MessageHandler(Filters.regex('^(/return)$'), start),
                        MessageHandler(Filters.regex('^(Ok)$'), type_one),
                        MessageHandler(Filters.regex('^(OK)$'), type_one)],
            TYPE_ONE: [
                        MessageHandler(Filters.text, type_two),],
            TYPE_TWO:[
                        CommandHandler('done', traffic),
                        MessageHandler(Filters.text, type_three),],
            TYPE_THREE:[
                        CommandHandler('done', traffic),
                        MessageHandler(Filters.text, traffic),],
            TRAFFIC:[
                    MessageHandler(Filters.regex('^(大眾運輸🚌)$'), traffic2),
                    MessageHandler(Filters.regex('^(客運🚌)$'), place_fork),
                    MessageHandler(Filters.regex('^(火車🚂)$'), place_fork),
                    MessageHandler(Filters.regex('^(高鐵🚅)$'), place_fork),
                    MessageHandler(Filters.regex('^(其他🚂)$'), place_fork),
            ],
            SEARCH_PLACE:[CommandHandler('restart', restart),
                CommandHandler('go',place_choose),
                CommandHandler('done', place_choose),
                MessageHandler(Filters.text, search_placedetail),
                CallbackQueryHandler(search_confirmbutton, pattern='^' + str(search_confirmbutton) + '$'),
                
            ],
            PLACE:[CommandHandler('restart', restart),
                CallbackQueryHandler(returnplace, pattern='^(上一頁)$'),
                CallbackQueryHandler(confirmbutton, pattern='^' + str(confirmbutton) + '$'),
                CallbackQueryHandler(placedetail),
                CommandHandler('next', place_choose),
                CommandHandler('done', done),
                MessageHandler(Filters.regex('^(下一個)$'), place_choose),
                MessageHandler(Filters.regex('^(完成)$'), done)],
        },
        fallbacks=[CommandHandler('restart', restart),MessageHandler(Filters.regex('^Done$'), done)]
    )

history_handler = ConversationHandler(
    entry_points = [CommandHandler('History', history)],
    states = {
        HISTORY:[CallbackQueryHandler(history_output),]
    },
    fallbacks=[]
)

#=================================================
#====================基礎機能設定==================
#=================================================

# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(conv_handler)
dispatcher.add_handler(history_handler)
dispatcher.add_handler(CommandHandler('help', help_handler))
dispatcher.add_handler(CommandHandler('start', greet))
dispatcher.add_handler(CommandHandler('restart', restart))
dispatcher.add_handler(MessageHandler(Filters.text, warnnn))

# Running server
if __name__ == "__main__":
    application.run(debug=True)