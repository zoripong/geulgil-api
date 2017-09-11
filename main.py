# Copyright 2016 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START app]
import logging

from flask import Flask
from konlpy.tag import *
import json

app = Flask(__name__)
app.debug=True
komoran = Komoran()


@app.route('/')
def hello():
    return 'Hello, We are GuelGil Developer <3 - Python3'

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

# [END app]
