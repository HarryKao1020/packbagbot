import csv

city_code_list={ #縣市ID清單
    "基隆":"10017", "台北":"63", "新北":"65", "桃園":"68", "新竹":"10018", "苗栗":"10005", "台中":"66", "南投":"10008", "彰化":"10007", "雲林":"10009", "嘉義":"10020", "台南":"67", "高雄":"64", "屏東":"10013", "台東":"10014", "花蓮":"10015", "宜蘭":"10002",
}
city_code={ #縣市ID清單
    "基隆":"1", "台北":"2", "新北":"3", "桃園":"4", "新竹":"5", "苗栗":"6", "台中":"7", "南投":"8", "彰化":"9", "雲林":"10", "嘉義":"11", "台南":"12", "高雄":"13", "屏東":"14", "台東":"15", "花蓮":"16", "宜蘭":"17",
}

#取得天氣資訊
# def webtextInf(inf):
#     inf=int(inf)
#     file =open('weather.csv','r')
#     lines=file.readlines()
#     file.close()
#     row=[]#定義行陣列
#     for line in lines:
#         row.append(line.split(','))

#     # 基隆=16*1 ; 台北=16*2 以此類推
#     webtext=row[16*int(inf)]

#     return webtext


def webtextInf(address):
    #數值轉換。例如：基隆=1；台北=2。
    citynum = city_code[address]
    citynum = int(citynum)

    #開啟CSV並讀取檔案
    file =open('weather.csv','r')
    lines=file.readlines()
    file.close()
    row=[]#定義行陣列
    for line in lines:
        row.append(line.split(','))

    # 基隆=16*1 ; 台北=16*2 以此類推
    webtext = row[16*citynum]
    # update.message.reply_text(address + '的天氣狀況：' + webtext)

    return webtext

temp=[]
city=input("輸入查詢")

print(webtextInf(city))


