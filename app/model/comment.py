# -*- coding: utf-8 -*-
from app import model as curpkg


class Comment(curpkg.db.Model):
    __tablename__ = 'comments'
