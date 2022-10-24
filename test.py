import json 
import requests
from datetime import date
from distutils.log import debug


year = date.today().year
url = f'http://api.themoviedb.org/3/discover/movie?api_key=1aeb8d4ebab949e8b09e793158af3cad&primary_release_year={year}&sort_by=popularity.desc'

data = requests.get(url)
        
# print(data, type(data)) #확인해보면 클래스가 출력된다.-> 인터넷에 검색해서 calss 를 제대로 출력해볼 것 

# #대용량 데이터의 경우, 2000만건 데이터를 싹 바꿔서 xml로 변환시키면 파일 하나가 된다. 그걸 json 형태로 바꿔서 스토리지에 저장하면 용량이 훨씬 줄어든다. 현장의 방법이다. 

# print(data.json()['results'])
# # data.json()  하거나 json.load(data.text) 해도 된다. 

genres = json.loads(requests.get("https://api.themoviedb.org/3/genre/movie/list?api_key=1aeb8d4ebab949e8b09e793158af3cad&language=en-US").text)

genre_id = f'https://api.themoviedb.org/3/discover/movie?api_key=1aeb8d4ebab949e8b09e793158af3cad&with_genres=28&sort_by=popularity.desc'
       
data_1 = json.loads(requests.get(genre_id).text)
print(data_1)
