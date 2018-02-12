# -*- coding: utf-8 -*-

from .. import db
from .. import login_manager
from .post import Post
from ..model.user import User
from .anonymous_user import AnonymousUser
from .comment import Comment


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


login_manager.anonymous_user = AnonymousUser

db.event.listen(Post.body, 'set', Post.on_body_changed)
db.event.listen(Comment.body, 'set', Comment.on_body_changed)
