# -*- coding: utf-8 -*-
from app import model as curpkg


class Follow(curpkg.db.Model):
    __tablename__ = 'follows'
    follower_id = curpkg.db.Column(
        curpkg.db.Integer, curpkg.db.ForeignKey('users.id'), primary_key=True)
    followed_id = curpkg.db.Column(
        curpkg.db.Integer, curpkg.db.ForeignKey('users.id'), primary_key=True)
    timestamp = curpkg.db.Column(
        curpkg.db.DateTime, default=curpkg.datetime.utcnow)
