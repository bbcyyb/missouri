# -*- coding:utf-8 -*-
from flask import render_template
from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from flask_login import current_user
from . import auth as app
from .forms import LoginForm
from .forms import RegisterForm
from .. import db
from ..model.user import User
from ..common.email import send_mail


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(url_for('blog.index'))
        flash(u'帐号或者密码错误')
    return render_template('login.html', title=u'登录', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash(u'您已退出登陆')
    return redirect(url_for('auth.login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data, email=form.email.data)
        # hard code to make email confirmation is passed.
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        User.add_self_follows()
        #token = user.generate_confirm_token()
        #send_mail(user.email, u'请确认您的帐号', 'confirm',
        #          user=user, token=token)
        #flash(u'有一份邮件已经发往您的邮箱')
        return redirect(url_for('auth.login'))
    else:
        return render_template('login.html', title=u'注册', form=form)


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('blog.index'))
    if current_user.confirm(token):
        flash(u'感谢您的确认')
    else:
        flash(u'链接已经失效或者过期')
    return redirect(url_for('blog.index'))


@app.before_app_request
def before_request():
    if request.endpoint != 'static':
        if current_user.is_authenticated:
            current_user.ping()
            if not current_user.confirmed \
                    and request.endpoint[:5] != 'auth.':
                return redirect(url_for('auth.unconfirmed'))


@app.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('blog.index'))
    return render_template('unconfirmed.html')


@app.route('/resend_email')
@login_required
def resend_email():
    token = current_user.generate_confirm_token()
    send_mail(current_user.email, u'确认您的帐号', 'confirm',
              user=current_user, token=token)
    flash(u'一份新的邮件已经发往您的邮箱')
    return redirect(url_for('blog.index'))
