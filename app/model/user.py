# -*- coding: utf-8 -*-
from .. import db, login_manager
from flask_login import UserMixin, AnonymousUserMixin


class User(UserMixin, db.Model):
    pass
