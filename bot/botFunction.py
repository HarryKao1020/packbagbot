#telegram基礎機能
import telegram
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater,  Filters, ConversationHandler, Dispatcher, CallbackQueryHandler , CommandHandler, MessageHandler

#其餘套件
from os import path
from selenium import webdriver
import configparser
import logging
import random

import db
import app
from app import *
# from app import logger
# from app import NAMING, DIRECTION, COUNTY, TYPE_ONE, TYPE_TWO, TYPE_THREE, TRAFFIC, SEARCH_PLACE, PLACE, PLACE_TWO,HISTORY
# from app import travelname, cntplace, tmpplace, placebuttontmp, tmpplacedetail, tmpregion, tmptypes, tmpcounty
# from app import city_code_list, weatherDeatil, weatherAll
# from app import webUserID, webtravelname, webRandom, webUrl, detailUrl
from place.PAPI import getNear, getPlace, getSearch

# __all__  = ['help_handler', 'greet', 'restart', 'warnnn', 'error', 'history', 'history_output', 'naming']

# from flask import Flask, request, render_template

#===============================================
#===================機器人指令===================
#===============================================
def help_handler(bot, update): #/help 功能介紹
    update.message.reply_text('指令教學 \n/letsgo 立刻開始使用 \n/history 查詢歷史行程 \n/restart 遇到問題時刷新機器人')

def greet(bot, update): #/start 機器人打招呼 
    update.message.reply_text('HI~我是旅泊包🎒 \n 我能依照你的喜好，推薦熱門景點給你')
    update.message.reply_text('準備要去旅行了嗎 ٩(ˊᗜˋ*)و \n立即輸入 /letsgo 開始使用！\n 如果要參考歷史行程請輸入 /history')

def restart(bot,update): #/restart
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
    app.logger.warning('Update "%s" caused error "%s"', update, context.error)

#######    history_conv            #######
def history(bot, update):#查詢行程
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

#===============================================
#===================機器人機能===================
#===============================================
def naming(bot, update):  #行程名稱取名
    app.logger.info("username: %s start", update.message.from_user)
    update.message.reply_text('請先替這次行程取個名字')
    return NAMING

def start(bot, update): #選擇區域
    UserID = update.message.from_user['id']
    if update.message.text != '/return':
        travelname.update( { UserID : update.message.text} )
    
    app.logger.info("username: %s start",update.message.from_user)
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
    app.logger.info("username: %s chooses %s",update.callback_query.from_user['id'],query.data)
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

    reply_keyboard=[['特色商圈','古蹟廟宇'],['人文藝術','景觀風景'],['休閒農業','戶外休閒'],['主題樂園','無礙障旅遊']]
    update.message.reply_text('請問有什麼想去的景點類型呢？',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TYPE_ONE

def type_two(bot, update):
    UserID = update.message.from_user['id']
    Text = update.message.text
    Text = Text.replace(" ","")
    db.setTYPE_one([Text,UserID,travelname[UserID]])

    reply_keyboard=[['特色商圈','古蹟廟宇'],['人文藝術','景觀風景'],['休閒農業','戶外休閒'],['主題樂園','無礙障旅遊'],['/done']]
    update.message.reply_text(f'你選擇的是「{Text}」，\n還有其他有興趣的類型嗎？\n如果沒有，請幫我選擇「/done」',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    if update.message.text != "/done":
        app.logger.info("%s is choose %s", update.message.from_user, update.message.text)

    return TYPE_TWO

def type_three(bot, update):
    UserID = update.message.from_user['id']
    Text = update.message.text
    Text = Text.replace(" ","")
    db.setTYPE_two([Text,UserID,travelname[UserID]])
    
    reply_keyboard=[['特色商圈','古蹟廟宇'],['人文藝術','景觀風景'],['休閒農業','戶外休閒'],['主題樂園','無礙障旅遊'],['/done']]
    update.message.reply_text(f'你選擇的是「{Text}」，\n還有其他有興趣的類型嗎？\n如果沒有，請幫我選擇「/done」',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    if update.message.text != "/done":
        app.logger.info("%s is choose %s", update.message.from_user, update.message.text)

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

    app.logger.info("type is %s form %s",update.message.text,update.message.from_user)
    reply_keyboard=[['大眾運輸🚌','其他🚂']]
    update.message.reply_text('想如何前往呢？',reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return TRAFFIC

def traffic2(bot, update):
    UserID = update.message.from_user['id']
    Text = update.message.text
    cntplace.update( {UserID:1} )
    print(Text)
    if Text != '/done':
        Text = Text.replace(" ","")
        db.setTYPE_three([Text,UserID,travelname[UserID]])

    app.logger.info("type is %s form %s",update.message.text,update.message.from_user)
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

def placedetail(bot, update):  #按鈕暫時無作用
    UserID = update.callback_query.from_user['id'] 
    query = update.callback_query
    query.answer()
    
    detail=getPlace(query.data)
    name = detail['name']
    rating = str(detail['rating'])
    address = detail['formatted_address']

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

def placeforcar(bot, update):
    UserID = update.message.from_user['id']
    logger.info("%s prees 自行前往", UserID)

    types = db.getTYPE([UserID,travelname[UserID]])
    county = db.getCOUNTY([UserID,travelname[UserID]])
    print(types)
    
    if ((len(types)-1) == 0):
        i = 0
    else:
        i = random.randint(0,len(types)-1)
        while types[i]==None:
            i = random.randint(0,len(types)-1)
    
    places = getNear(county[0],types[i]) #取得景點名稱
    
    button = []
    for name in places:
        button.append([InlineKeyboardButton(name['name'], callback_data=name['placeid'])],)
    keyboard = button
    placebuttontmp.update({UserID:keyboard})
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('想開車去哪裡玩呢？',reply_markup=markup)

    return PLACE

#================ 選擇景點(第二個~結束) ================
def place_choose(bot, update):
    UserID = update.message.from_user['id']
    app.logger.info("%s prees 自行前往", UserID)

    types = db.getTYPE([UserID,travelname[UserID]])
    county = db.getCOUNTY([UserID,travelname[UserID]])
    print(types)
    if ((len(types)-1) == 0):
        i = 0
    else:
        i = random.randint(0,len(types)-1)
        while types[i]==None:
            i = random.randint(0,len(types)-1)
            
    print(types[i])

    places = getNear(county[0],types[i]) #取得景點名稱
    
    button = []
    for name in places:
        button.append([InlineKeyboardButton(name['name'], callback_data=name['placeid'])],)
    
    keyboard = button
    placebuttontmp.update({UserID:keyboard})
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('下列景點想去哪裡玩呢？',reply_markup=markup)

    return PLACE

def place_fork(bot,update):
    UserID = update.message.from_user['id']
    app.logger.info("%s prees 自行前往", UserID)

    update.message.reply_text('想要自己選擇景點請輸入景點名稱\n如果希望由旅泊包安排請點選👇\n/go')
    
    return SEARCH_PLACE
    
def search_placedetail(bot, update):  #按鈕暫時無作用
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

    webUrl = getUserwebURL(UserID, travelname[UserID])
    # callFlask()
    update.message.reply_text('旅泊包幫你安排好行程嘍')
    update.message.reply_text(place_output)
    update.message.reply_text('http://127.0.0.1:5000' + webUrl)
    update.message.reply_text('希望你喜歡旅泊包安排的行程🐾\n祝你玩得愉快！')
    print('http://127.0.0.1:5000' + webUrl )

    getWeather(tmpcounty[UserID])
    update.message.reply_text(weatherAll)
    update.message.reply_text(tmpcounty[UserID] + '的天氣狀況：' + weatherDeatil)
    
    return ConversationHandler.END

#===============================================
#====================天氣提示====================
#===============================================
def getWeather(address):
    home_page = 'https://www.cwb.gov.tw/V8/C/W/County/County.html?CID='
    city_code = city_code_list[address] #與city_code_list的縣市資料對比數字
    url = home_page + city_code
    driver = webdriver.Chrome()
    driver.get(url) #啟動Chrome
    weatherAll = driver.find_element_by_xpath('/html/body/div/div/div/ul').text
    weatherDeatil = driver.find_element_by_xpath('/html/body/div/div/div/div/a').text
    driver.close() #關閉Chrome

    return

#===============================================
#===================網頁用方法===================
#===============================================
def getUserwebURL(UserID, travelname):
    #產生亂數URL提供給使用者
    webUserID = UserID
    webtravelname = travelname
    webRandom = random.choice('123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@$%^&*qwertyuiopasdfghjklzxcvbnm')
    detailUrl = webtravelname + webRandom
    ramdomUserID = ''
    ramdomlist = []

    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(8):
        ramdomlist.append(random.choice(seed))
        ramdomUserID = ''.join(ramdomlist)

    Url =  "/" + ramdomUserID + "/" + webtravelname + webRandom

    return Url

# def callFlask():
#     # Running server
#     if __name__ == "__main__":
#         app.run(debug=True)
