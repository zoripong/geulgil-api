# -*- coding: utf-8 -*-

# [START app]
import logging
import pymysql
from flask import Flask
import json

# [fourth function]
import collections
import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
# [fifth function]
# from konlpy.tag import Komoran  # Window용
from konlpy.tag import Twitter #Linux용
# [sixth function]
import requests


# app = Flask(__name__)
# app.debug=True

# [Start Class Modeling]
# [wordItem modeling]
class WordItem:
    def __init__(self):
        self.id = None;
        self.recommend = 0;

    def __init__(self, id, word, mean, part, category, meanKeyword, similarKeyword, recommend):
        self.id = id
        self.word = word
        self.mean = mean
        self.part = part
        self.category = category
        self.meanKeyword = meanKeyword  # list
        self.similarKeyword = similarKeyword  # list
        self.recommend = recommend

    def print(self):
        print(self.word)
        print(self.mean)
        print(self.part)
        print(self.category)
        print(self.meanKeyword)
        print(self.similarKeyword)
        print(self.recommend)

    def getId(self):
        return self.id

    def getWord(self):
        return self.word

    def getMean(self):
        return self.mean

    def getPart(self):
        return self.part

    def getCategory(self):
        return self.category

    def getMeanKeyword(self):
        return self.meanKeyword

    def getSimilarKeyword(self):
        return self.similarKeyword

    def getRecommend(self):
        return self.recommend


# [End Class Modeling]
# [Start YURI's function]
# [first function -> 검색어들과 관련된 단어들을 모두 가지고 옴]
def test_server(word):
    # words = words_sentence.split(':')
    word_json_dict = collections.OrderedDict()
    word_json_list = list()
    word_json_list = get_word_json(word)
    num = 0
    for i in word_json_list:
        num += 1
        word_json_dict['no'] = num
        word_json_dict['json'] = i
    result_json = collections.OrderedDict()
    result_json['response sign'] = "ok"
    result_json['result'] = word_json_dict
    return json.dumps(result_json, ensure_ascii=False, indent=4)


# [second function : 하나의 단어와 관련된 단어들을 가지고 옴]
def get_word_json(word):
    json_list = list()
    relatives = get_relatives(word)  # type
    for i in relatives:
        title = word  # type str
        word_json = {
            "title": title.decode('utf8'),
            "relatives": relatives
        }
        json_list.append(json.dumps(word_json, ensure_ascii=False, indent=4))

    return json_list


# [데이터 베이스에서 새로운 Word 데이터 요청시 호출 함수]
# [return : WordItem List]
def get_relatives(word):
    results = get_saemmul_data(word)

    relatives = list()
    for i in results:
        result = i
        item = WordItem(None, result['word'], result['mean'], result['part'], result['category'],
                        get_mean_words(result['mean']), get_similar_words(result['word'], result['mean']), None)
        relatives.append(item)
    return relatives


# [fourth function : 샘물 api에서 국어사전 정보 가져옴]
def get_saemmul_data(word):
    # 검색 단어
    requestWord = word

    # api 요청키 및 url
    key = "F635422D1CB1AFD64F654E7C547387F1"
    url = "https://opendict.korean.go.kr/api/search" + "?key=" + key + "&q=" + quote(requestWord) + "&num=10" \
          + "&advanced=y" + "&target=1" + "&method=exact"  # + "&sort=popular"+ "&type1=word"

    # header 정보 추가
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    }

    # url 요청 및 오픈
    req = urllib.request.Request(url, headers=headers)
    data = urllib.request.urlopen(req).read()

    # BeautifulSoup을 이용하여 파싱하기 위한 객체 생성
    xml = BeautifulSoup(data, "html.parser")
    dict_list = list()
    # item 검색
    for item in xml.findAll('item'):
        # print type(item)
        xmldict = collections.OrderedDict()
        xmldict['word'] = item.find('word').text  # 단어
        sense = item.find('sense')  # 의미를 포함하는 <>
        xmldict['mean'] = sense.find('definition').text  # 의미
        category = sense.find('cat')  # 카테고리
        if category != None:
            xmldict['category'] = category.text
        else:
            xmldict['category'] = None
        pos = sense.find('pos')  # 품사
        if pos != None:
            xmldict['part'] = pos.text
        else:
            xmldict['part'] = None
        dict_list.append(xmldict)
    return dict_list  # type list of dict


# fifth function
def get_mean_words(mean):
    include_word = list()
    include_word.append(konlpy.nouns(mean))
    return include_word


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
            # print(similar)
            similar_list.append(similar.text)
    return similar_list


# [END Yuri's function]

# [Start Doori's function]


# meanKeyword를 DB에 넣을 형식으로 바꿈
def meanForDB(meanKeyword):
    m = ""
    for i in meanKeyword[0]:
        m += i + ","
    return m


# similarKeyword를 DB에 넣을 형식으로 바꿈
def similarForDB(similarKeyword):
    s = ""
    for i in similarKeyword:
        s += i + ","
    return s


# searchWord가 DB에 있는지 확인 후 없으면 insert
def insertDB(conn, cursor, searchWord):
    cursor.execute("select * from item where word='" + searchWord + "'")

    if (cursor.rowcount == 0):
        wordItem = get_relatives(searchWord)
        for i in wordItem:
            cursor.execute("select * from item where mean='" + i.mean + "'")
            if (cursor.rowcount == 0):
                m = meanForDB(i.meanKeyword)
                s = similarForDB(i.similarKeyword)
                data = (i.word, i.mean, '', m, s)
                cursor.execute(
                    "insert into item(word,mean,part,meankeyword,similarkeyword,recommend) values(%s, %s, %s, %s, %s, 0)",
                    data)
                conn.commit()

#commonCase
def commonCase(cursor, apiItem, searchWord):
    cursor.execute("select * from item where word ='searchWord'")
    for i in range(cursor.rowcount):
        fetch = cursor.fetchone()
        if (fetch != None):
            wordItem = {}
            wordItem['id'] = fetch[0]
            wordItem['word'] = fetch[1]
            wordItem['mean'] = fetch[2]
            wordItem['part'] = fetch[3]
            mk = fetch[4].split(",")
            del (mk[len(mk) - 1])
            wordItem['meankeyword'] = mk
            sk = fetch[5].split(",")
            del (sk[len(sk) - 1])
            wordItem['similarkeyword'] = sk
            wordItem['recommend'] = fetch[6]

            samesoundCnt = 0
            for j in range(0, len(apiItem['relatives'])):
                if (apiItem['relatives'][j]['id'] == fetch[1]):
                    sameidCnt = 0
                    for k in range(0, len(apiItem['relatives'][j]['samesound'])):
                        if (apiItem['relatives'][j]['samesound'][k]['id'] == fetch[0]):
                            sameidCnt += 1
                            samesoundCnt += 1
                            break
                    if (sameidCnt >= 1):
                        break
                    apiItem['relatives'][j]['samesound'].append(wordItem)
                    samesoundCnt += 1
                    break

            if (samesoundCnt == 0):
                same = {'id': fetch[1], 'samesound': [wordItem]}
                apiItem['relatives'].append(same)

    return apiItem


# case1:searchWord가 의미에 포함되어 있는 단어
def case1(cursor, apiItem, searchWord):
    cursor.execute(
        "select * from item where similarkeyword like '" + searchWord + ",%' or similarkeyword like '%," + searchWord + ",%'")
    for i in range(cursor.rowcount):
        fetch = cursor.fetchone()
        if (fetch != None):
            wordItem = {}
            wordItem['id'] = fetch[0]
            wordItem['word'] = fetch[1]
            wordItem['mean'] = fetch[2]
            wordItem['part'] = fetch[3]
            mk = fetch[4].split(",")
            del (mk[len(mk) - 1])
            wordItem['meankeyword'] = mk
            sk = fetch[5].split(",")
            del (sk[len(sk) - 1])
            wordItem['similarkeyword'] = sk
            wordItem['recommend'] = fetch[6]

            samesoundCnt = 0
            for j in range(0, len(apiItem['relatives'])):
                if (apiItem['relatives'][j]['id'] == fetch[1]):
                    sameidCnt = 0
                    for k in range(0, len(apiItem['relatives'][j]['samesound'])):
                        if (apiItem['relatives'][j]['samesound'][k]['id'] == fetch[0]):
                            sameidCnt += 1
                            samesoundCnt += 1
                            break
                    if (sameidCnt >= 1):
                        break
                    apiItem['relatives'][j]['samesound'].append(wordItem)
                    samesoundCnt += 1
                    break

            if (samesoundCnt == 0):
                same = {'id': fetch[1], 'samesound': [wordItem]}
                apiItem['relatives'].append(same)

    return apiItem


# case2:searchWord가 유사어키워드에 포함되어있는 단어
def case2(cursor, apiItem, searchWord):
    cursor.execute(
        "select * from item where meankeyword like '" + searchWord + ",%' or meankeyword like '%," + searchWord + ",%'")
    for i in range(cursor.rowcount):
        fetch = cursor.fetchone()
        if (fetch != None):
            wordItem = {}
            wordItem['id'] = fetch[0]
            wordItem['word'] = fetch[1]
            wordItem['mean'] = fetch[2]
            wordItem['part'] = fetch[3]
            mk = fetch[4].split(",")
            del (mk[len(mk) - 1])
            wordItem['meankeyword'] = mk
            sk = fetch[5].split(",")
            del (sk[len(sk) - 1])
            wordItem['similarkeyword'] = sk
            wordItem['recommend'] = fetch[6]

            samesoundCnt = 0

            for j in range(0, len(apiItem['relatives'])):
                if (apiItem['relatives'][j]['id'] == fetch[1]):
                    sameidCnt = 0
                    for k in range(0, len(apiItem['relatives'][j]['samesound'])):
                        if (apiItem['relatives'][j]['samesound'][k]['id'] == fetch[0]):
                            sameidCnt += 1
                            samesoundCnt += 1
                            break
                    if (sameidCnt >= 1):
                        break
                    apiItem['relatives'][j]['samesound'].append(wordItem)
                    samesoundCnt += 1
                    break

            if (samesoundCnt == 0):
                same = {'id': fetch[1], 'samesound': [wordItem]}
                apiItem['relatives'].append(same)

    return apiItem

# case3:searchWord의 유사어키워드가 유사어키워드에 포함되어있는 단어
def case3(cursor, apiItem, sKeyword):
    for i in sKeyword:
        cursor.execute("select * from item where similarkeyword like '" + i + ",%' or similarkeyword like '%," + i + ",%'")
        for j in range(cursor.rowcount):
            fetch = cursor.fetchone()
            if (fetch != None):
                wordItem = {}
                wordItem['id'] = fetch[0]
                wordItem['word'] = fetch[1]
                wordItem['mean'] = fetch[2]
                wordItem['part'] = fetch[3]
                mk = fetch[4].split(",")
                del (mk[len(mk) - 1])
                wordItem['meankeyword'] = mk
                sk = fetch[5].split(",")
                del (sk[len(sk) - 1])
                wordItem['similarkeyword'] = sk
                wordItem['recommend'] = fetch[6]

                samesoundCnt = 0

                for k in range(0, len(apiItem['relatives'])):
                    if (apiItem['relatives'][k]['id'] == fetch[1]):
                        sameidCnt = 0
                        for l in range(0, len(apiItem['relatives'][k]['samesound'])):
                            if (apiItem['relatives'][k]['samesound'][l]['id'] == fetch[0]):
                                sameidCnt += 1
                                samesoundCnt += 1
                                break
                        if (sameidCnt >= 1):
                            break
                        apiItem['relatives'][k]['samesound'].append(wordItem)
                        samesoundCnt += 1
                        break

                if (samesoundCnt == 0):
                    same = {'id': fetch[1], 'samesound': [wordItem]}
                    apiItem['relatives'].append(same)

    return apiItem


# filter가 유사어일 경우 --경우의 수 1 //유사어일 경우 이 함수 호출
def dbforsimilar(searchWord):
    conn = pymysql.connect(host='52.78.168.169', port=3306, user='root', passwd='Geulgil123!', db='geulgil',
                           charset='utf8')
    cursor = conn.cursor()

    # searchWord가 DB에 없다면 insert
    insertDB(conn, cursor, searchWord)

    # searchWord의 의미키워드 배열 생성
    cursor.execute("select similarkeyword from item where word ='" + searchWord + "'")
    sKeyword = []
    for j in range(cursor.rowcount):
        fetch = cursor.fetchone()[0]
        if (fetch != ''):
            sKeyword = fetch.split(",")
            del sKeyword[len(sKeyword) - 1]

    apiItem = {'title': searchWord, 'relatives': []}


    #commonCase:searchWord
    apiItem = commonCase(cursor, apiItem, searchWord)

    # case1:searchWord가 유사어에 포함되어 있는 단어
    apiItem = case1(cursor, apiItem, searchWord)

    # case3:searchWord의 유사어가 유사어에 포함되어 있는 단어
    apiItem = case3(cursor, apiItem, sKeyword)

    jsonString = json.dumps(apiItem, indent=4)

    cursor.close()
    conn.close()

    return jsonString


# filter가 의미일 경우 --경우의 수 2,4//포함어일경우 이 함수 호출
def dbformean(searchWord):
    conn = pymysql.connect(host='52.78.168.169', port=3306, user='root', passwd='Geulgil123!', db='geulgil',
                           charset='utf8')
    cursor = conn.cursor()

    # searchWord가 DB에 없다면 insert
    insertDB(conn, cursor, searchWord)

    apiItem = {'title': searchWord, 'relatives': []}

    # commonCase:searchWord
    apiItem = commonCase(cursor, apiItem, searchWord)

    # case2:searchWord가 의미키워드에 포함되어있는 단어
    apiItem = case2(cursor, apiItem, searchWord)
    jsonString = json.dumps(apiItem, indent=4)

    cursor.close()
    conn.close()

    return jsonString


# [END Doori's function]

konlpy = Twitter()

app = Flask(__name__)
app.debug=True

#data = dbformean("사랑")
# print(data)


@app.route('/')
def main():
    return 'Hello, We are Geulgil Developer XD'

@app.route('/nouns/<string:str>/')
def natural_language(str):
    # jpype.attachThreadToJVM()
    list = konlpy.nouns(str)
    result = ''
    for i in list:
        result += i +':'
    return result

@app.route('/request/<string:str>/<isMean>/')
def response(str, isMean):
    if(isMean == 'true'):
        return dbformean(str)
    else:
        return dbforsimilar(str)

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
    # app.run()
