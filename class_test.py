
from flask import Flask
from konlpy.tag import Twitter #Window용
from konlpy.tag import Komoran
import json
import logging
import jpype
# >>> komoran = Komoran()


app = Flask(__name__)
app.debug=True
konlpy = Twitter() #Window

@app.route('/')
def test():
    return "Hello, We are GeulGil Developer :3"

@app.route('/nouns/<string:str>')
def natural_language(str):
    jpype.attachThreadToJVM()
    list = konlpy.nouns(str)
    return list


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

if __name__ == '__main__':
    app.debug = True
    # app.run(host="0.0.0.0")
    app.run()
