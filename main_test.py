#-*- coding: utf-8 -*-

from konlpy.tag import *
import json
import collections
import urllib2
from bs4 import BeautifulSoup

# first function
def test_server(words_sentence):
    words = words_sentence.split(':')
    word_json_dict = collections.OrderedDict()
    num = 0
    for i in words:
        i.strip()
        word_json_dict[num] = get_word_json(i)
        num+=1

    result_json = collections.OrderedDict()
    result_json['respone sign'] = "ok"
    result_json['result'] = word_json_dict
    return json.dumps(result_json, ensure_ascii=False, indent=4)

# second function
def get_word_json(word):
    title = word  # type str
    relatives = get_relatives(word)  # type
    word_json = {
        "title" : title,
        "relatives" :relatives
    }
    return json.dumps(word_json, ensure_ascii=False, indent=4)

 #TODO 값이 여러 개일 경우도 처리,,,, saemmul 의 결과가 여러개일 경우......
# third function
def get_relatives(word):
    result = get_saemmul_data(word)
    mean_words = get_mean_words(result['word'])
    similar_words = get_similar_words(result['word'])
    relatives = collections.OrderedDict()
    relatives['word'] = result['word']
    relatives['mean'] = result['mean']
    relatives['category'] = result['category']
    relatives['part'] = result['part']
    relatives['mean keywords'] = mean_words
    relatives['similar keywords'] = similar_words
    relatives['recommend'] = 0
    return relatives


# fourth function
def get_saemmul_data(word):
    key = "F635422D1CB1AFD64F654E7C547387F1"
    requestWord = urllib2.quote(word)
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
    return dict_list     # type list of dict

# fifth function
def get_mean_words(mean):
    # return komoran.nouns(unicode(mean))     #type list
    return ['보통', '남자', '대접', '말']

#TODO : CRAWLING
# sixth function
def get_similar_words(word):
    result = ['미스터', '남자', '양반']
    return result   #type list

komoran = Komoran()
respone = test_server("신사")
print respone
print type(respone)