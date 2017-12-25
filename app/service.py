# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from app.common import util


app = Flask(__name__)
config = util.load_config()

bootstrap = Bootstrap(app)


@app.route('/')
def hello_world():
    return render_template('index.html', name="kevin yu")


if __name__ == '__main__':
    app.run()
