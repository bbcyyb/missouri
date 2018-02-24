# -*- coding: utf-8 -*-
from app import db
from datetime import datetime
from flask import url_for
from markdown import markdown
import bleach


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow)
    disabled = db.Column(db.Boolean)
    post_id = db.Column(
        db.Integer, db.ForeignKey('posts.id'))
    author_id = db.Column(
        db.Integer, db.ForeignKey('users.id'))

    @staticmethod
    def from_json(json_body):
        body = json_body.get('body')
        if body is None or body == '':
            print 'error'
        return Comment(body=body)

    def to_json(self):
        comment_json = {
            'url': url_for('api.get_comment', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp
        }
        return comment_json

    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'code',
                      'em', 'strong']
        target.body_html = bleach.linkify(
            bleach.clean(
                markdown(value, output_format='html'),
                tags=allow_tags, strip=True))
