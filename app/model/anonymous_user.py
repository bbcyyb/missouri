# -*- coding: utf-8 -*-
from app import model as curpkg


class AnonymousUser(curpkg.AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False
