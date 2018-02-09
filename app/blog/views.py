# -*- coding: utf-8 -*-
from flask import render_template
from flask import make_response
from flask import redirect
from flask import request
from flask import url_for
from flask import current_app
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from . import blog as app
from ..model.permission import Permission
from ..model.post import Post


COOKIE_MAX_AGE = 30 * 24 * 60 * 60


@app.route('/', methods=['GET'])
def index():
    show_followed = False
    if current_user.is_authenticated:
        show_followed = bool(request.cookies.get('show_followed'))
    if show_followed:
        query = current_user.followed_posts
    else:
        query = Post.query
        page = request.args.get('page', 1, type=int)
    pagination = query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=10,
        error_out=False)
    posts = pagination.items
    return render_template('index.html', show_followed=show_followed,
                           posts=posts, pagination=pagination)


@app.route('/all')
def show_all():
    response = make_response(redirect(url_for('blog.index')))
    response.set_cookie('show_followed', '', max_age=COOKIE_MAX_AGE)
    return response


@app.route('/followed')
def show_followed():
    response = make_response(redirect(url_for('blog.index')))
    response.set_cookie('show_followed', '2', max_age=COOKIE_MAX_AGE)
    return response


@app.route('/post/<int:id>', methods=['POST'])
def post(id):
    pass


@app.route('/blog')
def blog():
    pass


@app.route('/admin')
def for_admin_only():
    return u'管理者进入'


@app.route('/user/<username>')
def user(username):
    pass


@app.route('/follow/<username>')
def follow(username):
    pass


@app.route('/unfollow/<username>')
def unfollow(username):
    pass


@app.route('/followers/<username>')
def followers(username):
    pass


@app.route('/followed-by/<username>')
def followed_by(username):
    pass


@app.route('/edit-profile', methods=['POST'])
def edit_profile():
    pass


@app.route('/edit-profile/<int:id>', methods=['POST'])
def edit_profile_admin(id):
    pass


@app.route('/edit/<int:id>')
def edit(id):
    pass


@app.route('/moderate', methods=['POST'])
def moderate():
    pass


@app.route('/moderate/disable/<int:id>')
def moderate_disable(id):
    pass


@app.route('/moderate/enable/<int:id>')
def moderate_enable(id):
    pass


def inject_permissions():
    return dict(Permission=Permission)


@app.route('/shutdown')
def server_shutdown():
    pass


@app.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['MISSOURI_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response
