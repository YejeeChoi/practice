import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

naver_movie='https://movie.naver.com/movie/running/current.nhn'
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(naver_movie,headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
soup = BeautifulSoup(data.text, 'html.parser')

movies = soup.select('.lst_detail_t1 > li')
# print(movies)

for movie in movies:
    if not movie.select('dt.tit') == None:
        for title_info in movie.select('dt.tit'):
            title = title_info.a.text
            link = naver_movie + title_info.a.attrs['href']
            # print(title)
            director = ', '.join([d.text for d in movie.select('span.link_txt')[1].select('a')])
            if len(movie.select('span.num')) > 1:
                rate = movie.select('span.num')[1].text
                # print(rate)
            img = movie.select('div.thumb > a > img')[0].attrs['src'].split('?')[0]

    doc = {}
    doc['Title'] = title
    doc['Director'] = director
    doc['Ticket Rate'] = rate
    doc['Image'] = img
    doc['Page Link'] = link
    db.movies.insert_one(doc)