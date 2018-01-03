# -*- coding: utf-8 -*-
from app.model.permission import Permission
from app.model.follow import Follow
from app.model.role import Role
from app.model.post import Post
from app import model as curpkg


class User(curpkg.UserMixin, curpkg.db.Model):
    __tablename__ = 'users'
    id = curpkg.db.Column(curpkg.db.Integer, primary_key=True)
    username = curpkg.db.Column(curpkg.db.String, nullable=True)
    password = curpkg.db.Column(curpkg.db.String, nullable=True)
    email = curpkg.db.Column(curpkg.db.String, nullable=True, unique=True)
    role_id = curpkg.db.Column(
        curpkg.db.Integer, curpkg.db.ForeignKey('roles.id'))
    password_hash = curpkg.db.Column(curpkg.db.String, nullable=True)
    confirmed = curpkg.db.Column(curpkg.db.Boolean, default=False)
    name = curpkg.db.Column(curpkg.db.String(64))
    location = curpkg.db.Column(curpkg.db.String(64))
    about_me = curpkg.db.Column(curpkg.db.Text())
    member_since = curpkg.db.Column(
        curpkg.db.DateTime, default=curpkg.datetime.utcnow)
    last_seen = curpkg.db.Column(
        curpkg.db.DateTime, default=curpkg.datetime.utcnow)
    posts = curpkg.db.relationship('Post', backref='author', lazy='dynamic',
                                   cascade='all, delete-orphan')
    followed = curpkg.db.relationship('Follow', foreign_keys=[Follow.follower_id], backref=curpkg.db.backref(
        'follower', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    followers = curpkg.db.relationship('Follow', foreign_keys=[Follow.followed_id], backref=curpkg.db.backref(
        'followed', lazy='joined'), lazy='dynamic', cascade='all, delete-orphan')
    comments = curpkg.db.relationship(
        'Comment', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.itsrole is None:
            if self.email == curpkg.current_app.config['MISSOURI_ADMIN']:
                self.itsrole = Role.query.filter_by(
                    Permission.ADMINISTRATOR).first()
            else:
                self.itsrole = Role.query.filter_by(default=True).first()

    def to_join(self):
        user_json = {
            'url': curpkg.url_for('api.get_user', id=self.id, _external=True),
            'username': self.username,
            'member_since': self.username,
            'last_seen': self.last_seen,
            'post_count': self.posts.count()
        }
        return user_json

    def follow(self, user):
        if not self.is_following(user):
            follow = Follow(follower=self, followed=user)
            curpkg.db.session.add(follow)
            curpkg.db.session.commit()

    def unfollow(self, user):
        follow = self.followed.filter_by(followed_id=user.id).first()
        if follow is not None:
            curpkg.db.session.delete(follow)
            curpkg.db.session.commit()

    def is_following(self, user):
        return self.followed.filter_by(followed_id=user.id).first() is not None

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    @property
    def followed_posts(self):
        return Post.query.join(Follow, Follow.followed_id == Post.author_id) \
            .filter(Follow.folower_id == self.id)
