# -*- coding: utf-8 -*-
from datetime import datetime
from flask import url_for
from markdown import markdown
import bleach
from app import db



class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow)
    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship(
        'Comment', backref='post', lazy='dynamic')

    @staticmethod
    def from_json(json_body):
        title = json_body.get('title')
        body = json_body.get('body')
        if body is None or body == '':
            print 'error'
        return Post(title=title, body=body)

    def to_json(self):
        json_post = {
            'url': url_for('api.get_post', id=self.id,
                           _external=True),
            'title': self.title,
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp,
            'comment_count': self.comments.count()
        }
        return json_post

    @staticmethod
    def generate_fake(count=10):
        from random import seed, randint
        import forgery_py
        from .user import User

        seed()
        user_count = User.query.count()
        for i in range(count):
            u = User.query.offset(randint(0, user_count - 1)).first()
            p = Post(title=forgery_py.lorem_ipsum.sentence(),
                     body=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()

    @staticmethod
    def generate_title():
        from random import seed
        import forgery_py

        seed()
        posts = Post.query.all()
        for post in posts:
            if post.title is None:
                post.title = forgery_py.lorem_ipsum.sentence()
                db.session.add(post)
        db.session.commit()

    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                      'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                      'h1', 'h2', 'h3', 'p', 'span', 'code', 'pre',
                      'img', 'hr', 'div']
        allow_attributes = ['src', 'alt', 'href', 'class']
        target.body_html = bleach.linkify(
            bleach.clean(
                markdown(value,
                         output_format='html',
                         extensions=[
                             'markdown.extensions.extra',
                             'markdown.extensions.codehilite']),
                target=allow_tags,
                attributes=allow_attributes,
                strip=True))
