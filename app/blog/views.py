# -*- coding: utf-8 -*-
from flask import render_template
from . import blogA
from ..model.permission import Permission

@blogA.route('/', methods=['GET'])
def index():
    print Permission.COMMENT
    return render_template('index.html')


@blogA.route('/blog', methods=['GET'])
def blog():
    return render_template('index.html')
