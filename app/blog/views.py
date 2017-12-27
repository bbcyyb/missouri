# -*- coding: utf-8 -*-
from flask import render_template
from . import blog


@blog.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html', name="kevin yu")
