#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    """docstring for LoginForm"""
    # def __init__(self, arg):
    #     super(LoginForm, self).__init__()
    #     self.arg = arg
    username = StringField('username',validators=[DataRequired()])
    password = StringField('password',validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default = True)

class RegForm(FlaskForm):
    """docstring for LoginForm"""
    # def __init__(self, arg):
    #     super(LoginForm, self).__init__()
    #     self.arg = arg
    username = StringField('username',validators=[DataRequired()])
    password = StringField('password',validators=[DataRequired()])
    password2 = StringField('password2',validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default = True)
    def pw_check(self):
        if self.password == self.password2:
            return True
    def email_check(self):
        return True

class PostForm(FlaskForm):
    body = StringField('body',validators=[DataRequired()])
