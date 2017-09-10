#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import render_template, url_for, flash, redirect, session, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from config import POSTS_PER_PAGE
from .forms import LoginForm, RegForm, PostForm
from .models import User, Post
from hashlib import md5
from datetime import datetime

@app.before_request
def before_request():
    g.user = current_user


@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
@app.route('/index/<int:page>',methods = ['GET', 'POST'])
@login_required
def index(page = 1):
    user = g.user
    form = PostForm()
    if form.validate_on_submit():
        body = form.body.data
        # p = Post(body = body, timestamp = datetime.utcnow(), author=g.user)
        p = Post(body = body, timestamp = datetime.utcnow(), user_id=g.user.get_id())
        db.session.add(p)
        db.session.commit()
        # form.body.data = ''
        # 防止重复提交
        return redirect(url_for('index'))
    # posts = Post.query.filter_by(user_id=g.user.get_id())[::-1]
    # posts = Post.query.filter_by(author=g.user)[::-1]
    posts = Post.query.filter_by(author=g.user).order_by(Post.timestamp.desc())
    posts = posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('index.html',
        title = 'Home',
        user = user,
        form = form,
        posts = posts)

#从数据库加载用户
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login', methods = ['GET', 'POST'])
# @oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated:
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
    if g.user.is_authenticated:
        logout_user()
    form = RegForm()
    if form.validate_on_submit():
        if User.query.filter_by(username = form.username.data).first() != None:
            flash('This user already exists, please change your username!')
        elif not form.pw_check():
            print(form.password.data,form.password2.data)
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

@app.route('/user/<username>', methods = ['GET', 'POST'])
@app.route('/user/<username>/<int:page>', methods = ['GET', 'POST'])
def user(username, page = 1):
    if User.query.filter_by(username = username).first() != None:
        user = User.query.filter_by(username = username).first()
        posts = Post.query.filter_by(author = user).order_by(Post.timestamp.desc())
        posts = posts.paginate(page, POSTS_PER_PAGE, False)
        return render_template('user.html',
            title = 'Home',
            user = user,
            posts = posts)
    flash('Sorry, this user does not exist!')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))