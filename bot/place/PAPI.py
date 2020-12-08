import googlemaps
import json
import random
gmaps = googlemaps.Client(key='AIzaSyDqdpn60A0oJ-L6loskqFIz6bD_X8cksFw')

def getNear(county,typess,loc):
    pre_rand=99
    rand = 0
    aName=[]
    radius = 3000
    cnt = 0

    while(len(aName)<5):
        if ((len(typess)-1) == 0):
            i = 0
        else:
            i = random.randint(0,len(typess)-1)
        while typess[i]==None:
            i = random.randint(0,len(typess)-1)
        types = typess[i]

        tmp_Name=[]
        cnt += 1
        if cnt == 3:
            if len(aName) == 0:
                radius +=500
                cnt = 0
        elif cnt == 6:
            break

        if  county == "台北": 
            if types == "特色商圈":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand=random.randint(0,2)
                sub_types=["夜市","商街", "市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand=random.randint(0,2)
                sub_types=["觀光果園","休閒農園","茶園"]
                
            elif types == "主題樂園":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand= random.randint(0,2)
                sub_types=["遊樂園","動物園","教育館"]
                
            elif types == "景觀風景":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand= random.randint(0,3)
                sub_types=["公園綠地","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["露營區","自行車道","登山步道","溫泉","植物園","生態園區"]

        elif county == "新北":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "形象商圈","市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,1)
                if rand == pre_rand:
                    rand= random.randint(0,1)
                sub_types=["教育館","海水浴場"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","燈塔","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,6)
                if rand == pre_rand:
                    rand= random.randint(0,6)
                sub_types=["露營區","自行車道","登山步道","溫泉","植物園","森林遊樂區","生態園區"]
        
        elif county == "基隆":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "形象商圈","市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand=random.randint(0,5)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場","茶園"]
                
            elif types == "主題樂園":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand= random.randint(0,2)
                sub_types=["遊樂園","海水浴場","教育館"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","展望台","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand= random.randint(0,4)
                sub_types=["露營區","自行車道","登山步道","生態園區","森林遊樂區"]
        
        elif county == "桃園":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "形象商圈", "市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand=random.randint(0,5)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場","茶園"]
                
            elif types == "主題樂園":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand= random.randint(0,4)
                sub_types=["遊樂園","水族館","動物園","教育館","海水浴場"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","展望台","自然保護區","風景區","觀景台","燈塔"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["露營區","自行車道","登山步道","植物園","生態園區","森林遊樂區"]
        
        elif county == "新竹":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "形象商圈", "市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand= random.randint(0,3)
                sub_types=["遊樂園","動物園","教育館","海水浴場"]
                
            elif types == "景觀風景":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand= random.randint(0,4)
                sub_types=["公園綠地","海邊","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["露營區","自行車道","登山步道","植物園","森林遊樂區","生態園區"]
        
        elif county == "苗栗":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "形象商圈", "市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand= random.randint(0,2)
                sub_types=["遊樂園","教育館","海水浴場"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","展望台","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand= random.randint(0,3)
                sub_types=["露營區","自行車道","登山步道","溫泉"]
        
        elif county == "台中":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "形象商圈", "市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand= random.randint(0,2)
                sub_types=["遊樂園","動物園","海水浴場"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","燈塔","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["露營區","自行車道","登山步道","生態園區","森林遊樂區","植物園"]
        
        elif county == "彰化":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "形象商圈", "市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,1)
                if rand == pre_rand:
                    rand= random.randint(0,1)
                sub_types=["遊樂園","教育館"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","燈塔","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand= random.randint(0,4)
                sub_types=["露營區","自行車道","登山步道","植物園","生態園區"]
        
        elif county == "南投":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "形象商圈", "市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["觀光工廠","農場","觀光果園","牧場"]
                
            elif types == "主題樂園":
                sub_types=["教育館"]
                
            elif types == "景觀風景":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand= random.randint(0,3)
                sub_types=["公園綠地","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["露營區","自行車道","登山步道","植物園","森林遊樂區","生態園區"]

        elif county == "雲林":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "形象商圈", "市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand= random.randint(0,2)
                sub_types=["遊樂園","教育館","海水浴場"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","燈塔","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand= random.randint(0,4)
                sub_types=["露營區","自行車道","登山步道","植物園","生態園區"]
        
        elif county == "嘉義":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "形象商圈", "市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand= random.randint(0,2)
                sub_types=["海水浴場","教育館","動物園"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","燈塔","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand= random.randint(0,4)
                sub_types=["露營區","自行車道","登山步道","植物園","生態園區"]

        elif county == "台南":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "形象商圈", "市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand= random.randint(0,2)
                sub_types=["動物園","教育館","海水浴場"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","燈塔","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand= random.randint(0,4)
                sub_types=["露營區","自行車道","登山步道","植物園","生態園區"]

        elif county == "高雄":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "形象商圈","市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand= random.randint(0,3)
                sub_types=["遊樂園","教育館","動物園","海水浴場"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","燈塔","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["露營區","自行車道","登山步道","植物園","森林遊樂區","生態園區"]

        elif county == "屏東":
            if types == "特色商圈":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand=random.randint(0,2)
                sub_types=["夜市","老街", "市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand= random.randint(0,2)
                sub_types=["遊樂園","教育館","海水浴場"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","燈塔","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["露營區","自行車道","登山步道","植物園","森林遊樂區","生態園區"]

        elif county == "宜蘭":
            if types == "特色商圈":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand=random.randint(0,2)
                sub_types=["夜市","老街", "市集"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand= random.randint(0,2)
                sub_types=["遊樂園","教育館","海水浴場"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","燈塔","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["露營區","自行車道","登山步道","植物園","森林遊樂區","生態園區"]

        elif county == "花蓮":
            if types == "特色商圈":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["夜市","老街", "市集", "百貨"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand= random.randint(0,2)
                sub_types=["遊樂園","教育館","動物園"]
                
            elif types == "景觀風景":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand= random.randint(0,4)
                sub_types=["公園綠地","燈塔","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["露營區","自行車道","登山步道","植物園","生態園區","森林遊樂區"]

        elif county == "台東":
            if types == "特色商圈":
                rand=random.randint(0,1)
                if rand == pre_rand:
                    rand=random.randint(0,1)
                sub_types=["夜市","老街"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,4)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","觀光果園","觀光漁港","牧場"]
                
            elif types == "主題樂園":
                sub_types=["教育館"]
                
            elif types == "景觀風景":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","燈塔","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,5)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["露營區","自行車道","登山步道","植物園","生態園區","森林遊樂區"]

        else :
            if types == "特色商圈":
                rand=random.randint(0,2)
                if rand == pre_rand:
                    rand=random.randint(0,2)
                sub_types=["夜市","老街", "形象商圈"]        
                
            elif types == "古蹟廟宇":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,3)
                sub_types=["寺廟","教堂","古蹟","軍事基地"]
                
            elif types == "人文藝術":
                rand=random.randint(0,3)
                if rand == pre_rand:    
                    rand=random.randint(0,3)
                sub_types=["文創園區","博物館","美術館","電影院"]
                
            elif types == "休閒農業":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand=random.randint(0,4)
                sub_types=["觀光工廠","農場","林場","漁場","牧場"]
                
            elif types == "主題樂園":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand= random.randint(0,1)
                sub_types=["遊樂園","水族館"]
                
            elif types == "景觀風景":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand= random.randint(0,5)
                sub_types=["公園綠地","海邊","展望台","自然保護區","風景區","觀景台"]
                
            elif types == "戶外休閒":
                rand=random.randint(0,3)
                if rand == pre_rand:
                    rand= random.randint(0,3)
                sub_types=["露營區","自行車道","登山步道","溫泉"]
        
        #關鍵字搜尋
        if loc == 0:
            geocode_result = gmaps.geocode(county+' '+sub_types[rand])
            loc = geocode_result[0]['geometry']['location']
            c = county+ ' '+sub_types[rand]
        else:
            c =sub_types[rand]
        #創建序列存放
        ids=[]
        
        #將半徑500公尺內的咖啡廳存放至ids序列
        
        # while (len(aName)==0):
        #     for place in gmaps.places_nearby(keyword=c,location=loc, radius = radius)['results']:
        #         ids.append(place['place_id'])
        #     radius += 500
        #     if radius > 5000:
                # break
        for place in gmaps.places_nearby(keyword=c,location=loc, radius = radius)['results']:
                ids.append(place['place_id'])
        
        #用set存放資料消除重複元素
        stores_info = []
        ids = list(set(ids))
        
        

        #存放半徑500公尺內咖啡廳的名稱、位置、總評分數量、評分
        for id in ids:
            stores_info.append(gmaps.place(place_id=id,fields=['name', 'place_id', 'formatted_phone_number', 'formatted_address', 'geometry/location', 'opening_hours', 'user_ratings_total', 'rating'], language='zh-TW')['result'])
        
        #除去評論數太少以致沒有評分的店家
        delete = []
        for i in stores_info:
            if 'rating' not in i:
                delete.append(i)
        for j in delete:
            stores_info.remove(j)
        
        #依照評分數值由高至低進行排序，若評分相同則比較總評分數量

        stores_info = sorted(stores_info,key=lambda x: (x['rating'],x['user_ratings_total']),reverse=True)

        #抓出每個地址的相關資料(沒用到就不用看)
        lat = []
        lng = []
        name = []
        rating = []
        urt = []

        for i in stores_info:
            lat.append(dict(dict(dict(i)['geometry'])['location'])['lat'])
            lng.append(dict(dict(dict(i)['geometry'])['location'])['lng'])
            name.append(dict(i)['name'])
            rating.append(dict(i)['rating'])
            urt.append(dict(i)['user_ratings_total'])
        
        sflag = 0
        for i in range(0,len(stores_info)):
            tmp_Name.append(stores_info[i])
        for i in tmp_Name:
            
            b = {'name':i['name'],'place_id':i['place_id'],'location':i['geometry']['location']}
            if len(aName)!=0:
                for j in aName:
                    if b['place_id'] == j['place_id']:
                        sflag = 1
                if sflag == 0:
                    if "店" not in b['name'] and "門市" not in b['name'] and "協會" not in b['name']  and "運動中心" not in b['name'] and "五金行" not in b['name'] and "百貨行" not in b['name']:
                        aName.append(b)
            else:
                aName.append(b)
            if len(aName)>=2:
                pre_rand=rand
                break
        pre_rand=rand
        
    return aName


def getPlace(a):
    getP = gmaps.place(place_id=a, fields=['name', 'formatted_address', 'formatted_phone_number', 'geometry/location', 'opening_hours', 'user_ratings_total', 'rating'] ,language='zh-TW')
    b = getP['result']
    c = {}
    for i in b:
        if i != 'geometry' and i != 'opening_hours':
            d = b[i]
            e = {i:d}
            c.update(e)
        elif i == 'opening_hours':
            d = b[i]
            e = {'weekday_text':d['weekday_text']}
            c.update(e)
        elif i == 'geometry':
            e = b[i]
            d = e['location']
            c.update(d)
    return c

def getSearch(county,place):
    query = county + place
    getS = gmaps.find_place(input=query, input_type='textquery', language='zh-TW')
    place_info = getS['candidates'][0]
    getP = gmaps.place(place_id=place_info['place_id'], fields=['name', 'formatted_address', 'formatted_phone_number', 'geometry/location', 'opening_hours', 'user_ratings_total', 'rating'] ,language='zh-TW')
    return getP