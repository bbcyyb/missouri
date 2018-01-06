# -*- coding: utf-8 -*-

from app import db, login_manager
from app.model import Post
from app.model import AnonymousUser
from app.model import Comment


@login_manager.user_loader
def load_user(user_id):
    from app.model import User
    return User.query.get(int(user_id))


login_manager.anonymous_user = AnonymousUser

db.event.listen(Post.body, 'set', Post.on_body_changed)
db.event.listen(Comment.body, 'set', Comment.on_body_changed)
