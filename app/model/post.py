# -*- coding: utf-8 -*-
from app import model as curpkg


class Post(curpkg.db.Model):
    __tablename__ = 'posts'
