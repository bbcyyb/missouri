
# -*- coding: utf-8 -*-
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, request, url_for
from datetime import datetime
import hashlib
from markdown import markdown
import bleach
from .. import db, login_manager