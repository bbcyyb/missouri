# -*- coding: utf-8 -*-

from flask import Flask
from common import util

app= Flask(__name__)
config = util.load_config()
print config["port"]

@app.route('/')
def hello_world():
    return 'hello world'

if __name__ == '__main__':
    app.run()
