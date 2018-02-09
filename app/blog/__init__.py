# -*- coding:utf-8 -*-
from flask import Blueprint, current_app
from flask_sqlalchemy import get_debug_queries
from ..model.permission import Permission

blog = Blueprint('blog', __name__)


@blog.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@blog.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['MISSOURI_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.nParameters, query.duration,
                   query.context)
            )
    return response


from . import views
