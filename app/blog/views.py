# -*- coding: utf-8 -*-
from flask import render_template
from . import blog
from ..models import Permission


@blog.route('/', methods=['GET'])
def index():
    print Permission.COMMENT
    return render_template('index.html')

@blog.route('/blog', methods=['GET'])
def blog():
    return render_template('index.html')
