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


from bot import *
from webfunction import *
import db
from place.PAPI import getNear, getPlace, getSearch

#=====================================================
#=======================Setting=======================
#=====================================================
#Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# # Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
# logger = logging.getLogger(__name__)

# Initial Flask app
application = Flask(__name__)

# Initial bot by Telegram access token
bot = telegram.Bot(token=(config['TELEGRAM']['ACCESS_TOKEN']))

NAMING, DIRECTION, COUNTY, TYPE_ONE, TYPE_TWO, TYPE_THREE, TRAFFIC, SEARCH_PLACE, PLACE, PLACE_TWO,HISTORY = range(11)


#===============================================
#===================網頁用參數===================
#===============================================
webUserID = ''     #webUserID = UserID
webtravelname = '' #webtravelname = 自行命名的行程名
webRandom = ''     #webRandom = 避免行程名重複
webUrl = ''        #webUrl = 產生的網址 (UserID+自行命名的景點+亂數)
detailUrl = ''     #detailUrl = 用來產生詳細景點資訊URL



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
                CommandHandler('exit', done)
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
    application.run(host='0.0.0.0',debug=True)