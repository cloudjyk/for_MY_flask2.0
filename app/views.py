#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect
from app import app
from .forms import LoginForm

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
# @login_required
def index():
    return render_template('index.html',
                           title='Home')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.username.data == 'cloud' and form.password.data == '1989422':
        flash('Login requested for user="' + form.username.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    print(type(form.username))
    print(form.password)
    return render_template('login.html', title = 'Sign In', form = form)