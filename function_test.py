# -*- coding: utf-8 -*-

#[fourth function]
import collections
import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
#[fifth function]
from konlpy.tag import Twitter #Window용

import requests



# [fifth function : konlpy를 이용하여 의미 중 명사만 추출]
def get_mean_words(mean):
    include_word = list()
    include_word.append(konlpy.nouns(mean))
    return include_word


# fifth function test
konlpy = Twitter() #Window
# print (get_mean_words("줄기나 가지가 목질로 된 여러해살이 식물."))

# [sixth function : 네이버 크롤링해서 유사어 가져옴]
def get_similar_words(word, mean):
    url = "http://krdic.naver.com/search.nhn?dic_where=krdic&query=" + quote(word)
    req = requests.get(url)
    html = req.content
    soup = BeautifulSoup(html.decode('utf-8', 'replace'), 'html.parser')
    similar_list = list()
    for tag in soup.find_all('span', text=mean):
        for e in tag.parent.parent.parent.findAll('sup'):
            e.extract()
        for similar in tag.parent.parent.parent.findAll('a', 'syno'):
            print(similar)
            similar_list.append(similar.text)
    return similar_list

# sixth function test
# print(get_similar_words("필기", "글씨를 씀."))

# [fourth function : 샘물 api에서 국어사전 정보 가져옴]
def get_saemmul_data(word):

    #검색 단어
    requestWord = word

    #api 요청키 및 url
    key = "F635422D1CB1AFD64F654E7C547387F1"
    url = "https://opendict.korean.go.kr/api/search" + "?key=" + key + "&q=" + quote(requestWord) + "&num=100" \
           + "&advanced=y" + "&target=1" + "&method=exact" #+ "&sort=popular"+ "&type1=word"

    #header 정보 추가
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    # url 요청 및 오픈
    req = urllib.request.Request(url, headers = headers)
    data = urllib.request.urlopen(req).read()

    #BeautifulSoup을 이용하여 파싱하기 위한 객체 생성
    xml = BeautifulSoup(data, "html.parser")
    dict_list = list()
    #item 검색
    for item in xml.findAll('item'):
        # print type(item)
        xmldict = collections.OrderedDict()
        xmldict['word'] = item.find('word').text #단어
        sense = item.find('sense') #의미를 포함하는 <>
        xmldict['mean'] = sense.find('definition').text #의미
        category = sense.find('cat') #카테고리
        if category != None:
            xmldict['category'] = category.text
        else:
            xmldict['category'] = None
        pos = sense.find('pos') #품사
        if pos != None:
            xmldict['part'] = pos.text
        else:
            xmldict['part'] = None
        dict_list.append(xmldict)
    return dict_list     # type list of dict



# fourth function test
# print (get_saemmul_data("나무"))