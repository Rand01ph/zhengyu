#!/usr/bin/env python
# encoding: utf-8

from .. import admin, redis

from flask_admin.contrib import rediscli
from flask_admin.contrib.sqla import ModelView

from ..models.user import db, User

# Add administrative views here
admin.add_view(rediscli.RedisCli(redis))
admin.add_view(ModelView(User, db.session))
