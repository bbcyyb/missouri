# -*- coding:utf-8 -*-
from flask import Blueprint

blog = Blueprint('blog', __name__)

import views, errors