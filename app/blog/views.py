# -*- coding: utf-8 -*-
from flask import render_template
from flask import request
from flask_login import current_user
from . import blog
from ..model.permission import Permission
from ..model.post import Post


@blog.route('/')
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
        page, per_page=10, error_out=False)
    posts = pagination.items
    return render_template(
        'index.html',
        show_followed=show_followed,
        posts=posts,
        pagination=pagination)


@blog.route('/all')
def show_all():
    return render_template('index.html')


@blog.route('/followed')
def show_followed():
    pass


@blog.route('/post/<int:id>', methods=['POST'])
def post(id):
    pass


@blog.route('/blog')
def blog():
    pass


@blog.route('/admin')
def for_admin_only():
    return '管理者进入'


@blog.route('/user/<username>')
def user(username):
    pass


@blog.route('/follow/<username>')
def follow(username):
    pass


@blog.route('/unfollow/<username>')
def unfollow(username):
    pass


@blog.route('/followers/<username>')
def followers(username):
    pass


@blog.route('/followed-by/<username>')
def followed_by(username):
    pass


@blog.route('/edit-profile', methods=['POST'])
def edit_profile():
    pass


@blog.route('/edit-profile/<int:id>', methods=['POST'])
def edit_profile_admin(id):
    pass


@blog.route('/edit/<int:id>')
def edit(id):
    pass


@blog.route('/moderate', methods=['POST'])
def moderate():
    pass


@blog.route('/moderate/disable/<int:id>')
def moderate_disable(id):
    pass


@blog.route('/moderate/enable/<int:id>')
def moderate_enable(id):
    pass


def inject_permissions():
    return dict(Permission=Permission)


@blog.route('/shutdown')
def server_shutdown():
    pass


@blog.after_app_request
def after_request(response):
    pass
