# -*- coding: utf-8 -*-
from flask import render_template
from flask import make_response
from flask import redirect
from flask import request
from flask import url_for
from flask import current_app
from flask import abort
from flask import flash
from flask_login import current_user
from flask_login import login_required
from flask_sqlalchemy import get_debug_queries
from . import blog as app
from .forms import CommentForm
from .forms import PostForm
from .forms import EditProfileForm
from .forms import EditProfileAdministratorForm
from .. import db
from ..model.permission import Permission
from ..model.post import Post
from ..model.comment import Comment
from ..model.user import User
from ..model.role import Role
from ..common.decorators import permission_required


COOKIE_MAX_AGE = 30 * 24 * 60 * 60


@app.route('/', methods=['GET','POST'])
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
@login_required
def show_all():
    response = make_response(redirect(url_for('blog.index')))
    response.set_cookie('show_followed', '', max_age=COOKIE_MAX_AGE)
    return response


@app.route('/followed')
@login_required
def show_followed():
    response = make_response(redirect(url_for('blog.index')))
    response.set_cookie('show_followed', '2', max_age=COOKIE_MAX_AGE)
    return response


@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    post = Post.query.get_or_404(id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(body=form.body.data,
                          post=post,
                          author=current_user._get_current_object(),
                          )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('blog.post', id=post.id, page=-1))
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = (post.comments.count() - 1) / 10 + 1
    pagination = post.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=10, error_out=False
    )
    comments = pagination.items
    return render_template('post.html', posts=[post], form=form,
                           comments=comments, pagination=pagination)


@app.route('/blog', methods=['GET', 'POST'])
@login_required
def blog():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('blog.html', form=form)


@app.route('/admin')
@login_required
@permission_required(Permission.ADMINISTRATOR)
def for_admin_only():
    return u'Administrator Entrance'


@app.route('/moderator')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def for_moderator_only():
    return u'Administrator Entrance'


@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@app.route('/follow/<username>')
def follow(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        flash(u'没有该用户')
        return redirect(url_for('blog.index'))
    if current_user.is_following(u):
        flash(u'已经关注了该用户')
        return redirect(url_for('blog.user', username=username))
    current_user.follow(u)
    flash(u'关注了 %s' % username)
    return redirect(url_for('blog.user', username=username))


@app.route('/unfollow/<username>')
def unfollow(username):
    u = User.query.filter_by(username=username).first()
    if u is None:
        flash(u'没有该用户')
        return redirect(url_for('blog.index'))
    if u.is_followed_by(current_user):
        current_user.unfollow(u)
        flash(u'取消对 %s 的关注' % username)
        return redirect(url_for('blog.user', username=username))


@app.route('/followers/<username>')
def followers(username):
    u = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    pagination = u.followers.paginate(page, per_page=10, error_out=False)
    follows = [{'user': item.follower, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', title=u'的粉丝', user=u, pagination=pagination, follows=follows)


@app.route('/followed-by/<username>')
def followed_by(username):
    u = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    pagination = u.followed.paginate(page, per_page=10, error_out=False)
    follows = [{'user': item.followed, 'timestamp': item.timestamp}
               for item in pagination.items]
    return render_template('followers.html', title=u'的关注', user=u, pagination=pagination, follows=follows)


@app.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        flash(u'你的个人信息已经被更改')
        db.session.add(current_user)              # 更新个人资料
        db.session.commit()
        return redirect(url_for('blog.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@app.route('/edit-profile/<int:id>', methods=['POST'])
@login_required
@permission_required(Permission.ADMINISTRATOR)
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdministratorForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.itsrole = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash(u'该用户的信息已经更新了')
        return redirect(url_for('blog.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)


@app.route('/edit/<int:id>')
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
            not current_user.can(Permission.ADMINISTRATOR):
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog.post', id=post.id))
    form = PostForm()
    form.title.data = post.title
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@app.route('/moderate', methods=['GET'])
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    page = request.args.get('page', 1, type=int)
    pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(
        page, per_page=10, error_out=False)
    comments = pagination.items
    return render_template('moderate.html',
                           comments=comments, pagination=pagination, page=page)


@app.route('/moderate/disable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_disable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = True
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('blog.moderate', page=request.args.get('page', 1, type=int)))


@app.route('/moderate/enable/<int:id>')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate_enable(id):
    comment = Comment.query.get_or_404(id)
    comment.disabled = False
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('blog.moderate', page=request.args.get('page', 1, type=int)))


@app.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)


@app.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server,shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return '-----Shutting down------'


@app.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['MISSOURI_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response
