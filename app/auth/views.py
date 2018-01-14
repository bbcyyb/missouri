# -*- coding:utf-8 -*-
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth


@auth.route("/auth/login", methods=['GET'])
def login():
    return '<h1>login</h1>'


@auth.route('/auth/logout', methods=['GET'])
def logout():
    return '<h1>logout</h1>'


@auth.route('/auth/register', methods=['GET'])
def register():
    return '<h1>register</h1>'
