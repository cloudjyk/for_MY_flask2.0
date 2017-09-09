#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# config initialed
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

lm = LoginManager()
lm.init_app(app)
#设置登录视图，很关键
lm.login_view = 'login'
######
# from flask_openid import OpenID
# import os
# from config import basedir
# oid = OpenID(app, os.path.join(basedir, 'tmp'))
######

from app import views, forms, models
from config import USER_LIST

# for i in USER_LIST:
#     u = models.User(username=i['username'], password=i['password'], email=i['email'])
#     db.session.add(u)
# db.session.commit()