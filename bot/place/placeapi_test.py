from PAPI import *
#第三欄位可以放經緯度，若不知道經緯度輸入0為預設
print(getNear('台北',['特色商圈','主題樂園'],{'lat': 25.0554229, 'lng': 121.514996}))

#print(getPlace('ChIJA87dBm2pQjQRLP8becy1VXE'))
#print(getSearch('台北','華山')['result'])