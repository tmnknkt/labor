from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user


lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    if current_user.is_authenticated:
        return render_template('lab8/lab8.html', login=current_user.login)
    else:
        return render_template('lab8/lab8.html', login=None)


@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or login_form.strip() == '':
        return render_template('lab8/login.html',
                            error='Введите логин')

    if not password_form or password_form.strip() == '':
        return render_template('lab8/login.html',
                            error='Введите пароль')

    user = users.query.filter_by(login=login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=False)
            return redirect('/lab8/')

    return render_template('lab8/login.html',
                          error='Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or login_form.strip() == '':
        return render_template('lab8/register.html',
                            error='Имя пользователя не может быть пустым')

    if not password_form or password_form.strip() == '':
        return render_template('lab8/register.html',
                            error='Пароль не может быть пустым')

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template('lab8/register.html',
                            error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect('/lab8/')


@lab8.route('/lab8/articles')
@login_required
def articles():
    return "Список статей"


@lab8.route('/lab8/create')
def create_article():
    return "Создание статьи"


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')