from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 설치 먼저 해야겠죠?)
client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbsparta  # 'dbsparta'라는 이름의 db를 사용합니다. 'dbsparta' db가 없다면 새로 만듭니다.
# MongoDB를 사용하기 위한 필수 값

import requests
from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713', headers=headers)
#지니 인기 페이지 가져오기

soup = BeautifulSoup(data.text, 'html.parser')

tr_1 = soup.select('#body-content > div.newest-list > div > table > tbody > tr')
# 음악 정보?가 있는 tr 가져오기 : copy > copy selector
# 첫번째 tr이라고 찍어주는 부분 삭제해서 마지막 위치 값을 'tr'로 잡아주기

#body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.title.ellipsis
                                                        #today 밑 tr 까지는 찍어줬으니 그 이후 부분 선택해서 타이틀 가져오기
for tr in tr_1:
    title = tr.select_one('td.info > a.title.ellipsis').text.strip()
    #tr_1에서 가져오는 정보 중에 title만 날것의 모양 > .text 붙여서 텍스트만 노출 > .strip()으로 공백 제거해서 가져오기

    # body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.number
                                                            #순위 정보도 마잔가지로 tr 이후 값만 선택해서 가져오기
    rank = tr.select_one('td.number').text[0:2].strip()
    #.text로 텍스트만 노출 > [0:2]로 앞에 두 글자만 가져올꺼야 선언 > .strip()으로 공백 잘라줘

    # body-content > div.newest-list > div > table > tbody > tr:nth-child(1) > td.info > a.artist.ellipsis
                                                            #아티스트 정보도 마찬가지로 tr 이후 값만 선택해서 가져오기
    artist = tr.select_one('td.info > a.artist.ellipsis').text

    doc = {
        'rank' : rank,      #db 'rank' 컬럼에 rank 값 넣기
        'title' : title,    #db 'title' 컬럼에 title 값 넣기
        'artist' : artist   #db 'artist' 컬럼에 artist 값 넣기
    }
    db.genie.insert_one(doc)    #genie에 doc를 넣읍시다
    #robo 3t에서 확인하기, run 진행 전 mongodb run 상태인지 확인 필수
    