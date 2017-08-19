# [START app]
import logging

from flask import Flask
from konlpy.tag import Komoran
import json

app = Flask(__name__)
app.debug=True
komoran = Komoran()


# first function
def test_server(words_sentence):
    words = words_sentence.split(':')
    word_json_list = list()
    for i in words:
        i.strip()
        word_json_list.append(get_word_json(i))
    result_json = {
        "respone sign" : "ok",
        "result" : word_json_list
    }
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
    word = word
    mean = result['mean']
    part = result['part']
    category = result['category']
    mean_words = get_mean_words(mean)
    similar_words = get_similar_words(word)
    relatives = {
        "word" : word,
        "mean" : mean,
        "part" : part,
        "category" : category,
        "mean keywords" : mean_words,
        "similar keywords" : similar_words,
        "recommend" : 0
    }
    return relatives

#TODO : REQUEST API
# fourth function
def get_saemmul_data(word):
    result = {
        'mean' : '보통 남자를 대접하여 이르는 말',
        'category' : 'null',
        'part' : '명사'
    }
    #MEAN
    #CATEGORY
    #PART

    return result   # type dict

# fifth function
def get_mean_words(mean):
    return komoran.nouns(unicode(mean))     #type list

#TODO : CRAWLING
# sixth function
def get_similar_words(word):
    result = ['미스터', '남자', '양반']
    return result   #type list

#[flask start]
@app.route('/')
def hello():
    return 'Hello, We are GuelGil Developer <3'

@app.route('/noun/<string:str>')
def natural_noun(str):
    list = komoran.nouns(unicode(str))
    result = json.dumps(list, indent=4, ensure_ascii=False)
    # result = ""
    # for i in list:
    #     result += i
    #     result += "\t"
    return result


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500


if __name__ == '__main__':
    app.debug=True
    app.run(host="0.0.0.0")
    # app.run()

# [END app]
