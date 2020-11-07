import PAPI
#第三欄位可以放經緯度，若不知道經緯度輸入0為預設
print(PAPI.getNear('台北','特色商圈',{'lat': 25.0554229, 'lng': 121.514996}))