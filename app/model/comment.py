# -*- coding: utf-8 -*-
from app import model as curpkg


class Comment(curpkg.db.Model):
    __tablename__ = 'comments'
    id = curpkg.db.Column(curpkg.db.Integer, primary_key=True)
    body = curpkg.db.Column(curpkg.db.Text)
    body_html = curpkg.db.Column(curpkg.db.Text)
    timestamp = curpkg.db.Column(
        curpkg.db.DateTime, default=curpkg.datetime.utcnow)
    disabled = curpkg.db.Column(curpkg.db.Boolean)
    post_id = curpkg.db.Column(
        curpkg.db.Integer, curpkg.db.ForeignKey('posts.id'))
    author_id = curpkg.db.Column(
        curpkg.db.Integer, curpkg.db.ForeignKey('users.id'))

    @staticmethod
    def from_json(json_body):
        body = json_body.get('body')
        if body is None or body == '':
            print 'error'
        return Comment(body=body)

    def to_json(self):
        comment_json = {
            'url': curpkg.url_for('api.get_comment', id=self.id, _external=True),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': self.timestamp
        }
        return comment_json

    @staticmethod
    def on_body_changed(target, value, oldvalue, initiator):
        allow_tags = ['a', 'abbr', 'acronym', 'b', 'code',
                      'em', 'strong']
        target.body_html = curpkg.bleach.linkify(curpkg.bleach.clean(curpkg.markdown(value, output_format='html'),
                                                                     tags=allow_tags, strip=True))
