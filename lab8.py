from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    login = request.form.get('login')
    return render_template('lab8/lab8.html', login=session.get('login'))


@lab8.route('/lab8/login')
def login():
    return "Страница входа"


@lab8.route('/lab8/register')
def register():
    return "Страница регистрации"


@lab8.route('/lab8/articles')
def articles():
    return "Список статей"


@lab8.route('/lab8/create')
def create_article():
    return "Создание статьи"