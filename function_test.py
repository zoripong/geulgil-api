# -*- coding: utf-8 -*-

import requests
import urllib2
from bs4 import BeautifulSoup
import collections
from konlpy.tag import Mecab

def test_1(word):
    key = "F635422D1CB1AFD64F654E7C547387F1"
    requestWord = urllib2.quote(word.encode('utf8'))
    url = "https://opendict.korean.go.kr/api/search" + "?key=" + key + "&q=" + requestWord + "&num=10" \
          + "&sort=popular" + "&advanced=y" + "&target=1" + "&method=exact" + "&type1=word";
    user_agent = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)"
    req = urllib2.Request(url)
    req.add_header("User-agent", user_agent)
    response = urllib2.urlopen(req)
    xml = BeautifulSoup(response, "html.parser")
    dict_list = list()
    for item in xml.findAll('item'):
        # print type(item)
        xmldict = collections.OrderedDict()
        xmldict['word'] = item.find('word').text
        sense = item.find('sense')
        xmldict['mean'] = sense.find('definition').text
        category = sense.find('cat')
        if category != None:
            xmldict['category'] = category.text
        else:
            xmldict['category'] = None
        pos = sense.find('pos')
        if pos != None:
            xmldict['part'] = pos.text
        else:
            xmldict['part'] = None
        dict_list.append(xmldict)

    return dict_list

# [TODO : function parameter]
# word = u"필기"
# mean = u"글씨를 씀."

def test_2(word, mean) :
    url = "http://krdic.naver.com/search.nhn?dic_where=krdic&query="+word
    req = requests.get(url)
    html = req.content
    soup = BeautifulSoup(html.decode('utf-8','replace'), 'html.parser')
    similar_list = list()
    for tag in soup.find_all('span', text=mean):
        for similar in tag.parent.parent.parent.find_all('a', 'syno'):
            similar_list.append(similar.text)
    return similar_list

def test_3(mean):
    include_word = list()
    include_word.append(mecab.nouns(unicode(mean, 'utf8')))

    return include_word
word = u"필기"
mecab = Mecab()

word_list = test_1(word)

# print word_list

for word_li in word_list:
    mean = str(word_li['mean'].encode('utf8'))
    print test_2(word, mean) #유사어 리스트
    print test_3(mean) #포함어 리스트

