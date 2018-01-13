# -*- coding:utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth

@auth.route("/", methods=['GET'])
def index():
    return '<h1>auth</h1>'