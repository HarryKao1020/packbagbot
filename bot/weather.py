from selenium import webdriver
import csv

city_code_list={ #縣市ID清單
    "基隆":"10017", "台北":"63", "新北":"65", "桃園":"68", "新竹":"10018", "苗栗":"10005", "台中":"66", "南投":"10008", "彰化":"10007", "雲林":"10009", "嘉義":"10020", "台南":"67", "高雄":"64", "屏東":"10013", "台東":"10014", "花蓮":"10015", "宜蘭":"10002",
}
itemlist = ["基隆","台北","新北","桃園","新竹","苗栗","台中","南投","彰化","雲林","嘉義","台南","高雄","屏東","台東","花蓮","宜蘭"]

for i in range(len(itemlist)):
    city_code = city_code_list[itemlist[i]] #與city_code_list的縣市資料對比數字
    home_page = 'https://www.cwb.gov.tw/V8/C/W/County/County.html?CID='
    url = home_page + city_code
    driver = webdriver.Chrome()
    driver.get(url) #啟動Chrome

    weatherAll = driver.find_element_by_xpath('/html/body/div/div/div/ul').text
    weatherDeatil = driver.find_element_by_xpath('/html/body/div/div/div/div/a').text
    driver.close() #關閉Chrome

    if i == 0:

        with open("weather.csv", "w",encoding='gb18030') as csvfile:
            wr = csv.writer(csvfile)
            wr.writerow(["縣市", "溫度", "細項"])
            wr.writerow([itemlist[i], weatherAll, weatherDeatil])
        print( itemlist[i] + '存完了' )

    else:

        with open("weather.csv", "a",encoding='gb18030') as csvfile:
            wr = csv.writer(csvfile)
            wr.writerow([itemlist[i], weatherAll, weatherDeatil])
        print( itemlist[i] + '哈哈哈存完了' )


print('全部存完la')