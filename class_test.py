
from flask import Flask
from konlpy.tag import Twitter #Window용
from konlpy.tag import Komoran
# >>> komoran = Komoran()

app = Flask(__name__)
app.debug=True
konlpy = Komoran() #Window

def get_mean_words(mean):
    return konlpy.nouns(mean)

@app.route('/')
def test():
    return "Hello, We are GeulGil Developer :3"

@app.route('/nouns/<string:str>')
def natural_language(str):
    return get_mean_words(str)

if __name__ == '__main__':
    app.debug = True
    # app.run(host="0.0.0.0")
    app.run()
