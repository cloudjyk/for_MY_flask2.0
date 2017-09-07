#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import render_template, url_for, flash, redirect, session, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, RegForm
from .models import User
from hashlib import md5

@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
# @login_required
def index():
    return render_template('index.html',
                           title='Home')

@app.route('/login', methods = ['GET', 'POST'])
# @oid.loginhandler
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        if User.query.filter_by(username = form.username.data).first() == None:
            flash('invalid user!')
        elif User.query.filter_by(username = form.username.data).first().password == md5(form.password.data.encode('utf-8')).hexdigest():
            flash('Login successfully for user:"' + form.username.data + '", remember_me=' + str(form.remember_me.data))
            login_user(User.query.filter_by(username = form.username.data).first(), form.remember_me.data)
            return redirect('/index')
    return render_template('login.html', title = 'Sign In', form = form)

@app.route('/register', methods = ['GET', 'POST'])
# @oid.loginhandler
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegForm()
    if form.validate_on_submit():
        if User.query.filter_by(username = form.username.data).first() != None:
            flash('This user already exists, please change your username!')
        elif not form.pw_check():
            flash('Passwords should be the same, please check!')
        elif not form.email_check():
            flash('Invalid email address!')
        else:
            u = User(username=form.username.data, password=md5(form.password.data.encode('utf-8')).hexdigest(), email=form.email.data)
            db.session.add(u)
            db.session.commit()
            flash('Register successfully for user:"' + form.username.data + '", remember_me=' + str(form.remember_me.data))
            return redirect(url_for('login'))
    return render_template('Register.html', title = 'Sign In', form = form)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))