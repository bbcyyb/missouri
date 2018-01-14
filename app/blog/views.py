# -*- coding: utf-8 -*-
from flask import render_template
from . import blog


@blog.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@blog.route('/blog', methods=['GET'])
def blog():
    return render_template('index.html')
