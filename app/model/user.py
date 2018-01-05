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

    def can(self, permissions):
        return self.itsrole is not None and \
            (self.itsrole.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTRATOR)

    def ping(self):
        self.last_seen = curpkg.datetime.utcnow()
        curpkg.db.session.add(self)
        curpkg.db.session.commit()

    def gravatar(self, size=100, default='identicon', rating='g'):
        if curpkg.request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = curpkg.hashlib.md5(self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&r={rating}&d={default}' \
            .format(url=url, hash=hash, size=size,
                    rating=rating, default=default)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = curpkg.generate_password_hash(password)

    def verify_password(self, password):
        return curpkg.check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration=3600):
        s = curpkg.Serializer(
            curpkg.current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    def generate_confirm_token(self, expiration=3600):
        s = curpkg.Serializer(
            curpkg.current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = curpkg.Serializer(curpkg.current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        curpkg.db.session.add(self)
        curpkg.db.session.commit()
        return True

    @staticmethod
    def generate_fake(count=10):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True))
            curpkg.db.session.add(u)
            try:
                curpkg.db.session.commit()
            except IntegrityError:
                curpkg.db.session.rollback()

    @staticmethod
    def add_self_follows():
        for user in User.query.all():
            if not user.is_following(user):
                user.follow(user)
                curpkg.db.session.add(user)
                curpkg.db.session.commit()

    @staticmethod
    def verify_auth_token(token):
        s = curpkg.Serializer(curpkg.current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])
