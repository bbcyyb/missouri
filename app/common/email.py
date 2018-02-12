# -*- coding:utf-8 -*-
import os
from flask import render_template
from flask import current_app
from flask_mail import Message
from threading import Thread
from .. import mail


def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kw):
    app = current_app._get_current_object()
    msg = Message(subject=subject, sender=app.config['MISSOURI_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', **kw)
    msg.html = render_template(template + '.html', **kw)
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
    return thr
