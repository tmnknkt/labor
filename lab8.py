from flask import Blueprint, render_template, request, session, redirect, current_app, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from db import db
from db.models import users, articles as ArticleModel
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import or_ , func


lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == 'on'

    if not login_form or login_form.strip() == '':
        return render_template('lab8/login.html', error='Введите логин')

    if not password_form or password_form.strip() == '':
        return render_template('lab8/login.html', error='Введите пароль')

    user = users.query.filter_by(login=login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember)
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
    
    login_user(new_user, remember=False)
    return redirect('/lab8/')


@lab8.route('/lab8/articles')
@login_required
def articles():
    # Получаем статьи текущего пользователя
    user_articles = ArticleModel.query.filter_by(login_id=current_user.id).all()
    return render_template('lab8/articles.html', articles=user_articles)


@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'GET':
        return render_template('lab8/create.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not article_text:
        return render_template('lab8/create.html', 
                             error='Заполните все обязательные поля')
    
    new_article = ArticleModel(
        login_id=current_user.id,
        title=title,
        article_text=article_text,
        is_favorite=is_favorite,
        is_public=is_public
    )
    
    db.session.add(new_article)
    db.session.commit()
    
    return redirect('/lab8/articles')


@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = ArticleModel.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        return redirect('/lab8/articles')
    
    if request.method == 'GET':
        return render_template('lab8/edit.html', article=article)
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = request.form.get('is_favorite') == 'on'
    is_public = request.form.get('is_public') == 'on'
    
    if not title or not article_text:
        return render_template('lab8/edit.html', 
                             article=article,
                             error='Заполните все обязательные поля')
    
    article.title = title
    article.article_text = article_text
    article.is_favorite = is_favorite
    article.is_public = is_public
    
    db.session.commit()
    
    return redirect('/lab8/articles')


@lab8.route('/lab8/delete/<int:article_id>')
@login_required
def delete_article(article_id):
    article = ArticleModel.query.get_or_404(article_id)
    
    if article.login_id != current_user.id:
        return redirect('/lab8/articles')
    
    db.session.delete(article)
    db.session.commit()
    
    return redirect('/lab8/articles')


@lab8.route('/lab8/public')
def public_articles():
    public_articles_list = ArticleModel.query.filter_by(is_public=True).all()
    return render_template('lab8/public.html', articles=public_articles_list)


@lab8.route('/lab8/search', methods=['GET', 'POST'])
def search_articles():
    if request.method == 'GET':
        return render_template('lab8/search.html')
    
    search_query = request.form.get('search_query', '').strip()
    
    if not search_query:
        return render_template('lab8/search.html', 
                             error='Введите поисковый запрос',
                             articles=[])
    

    search_lower = search_query.lower()
    
    if current_user.is_authenticated:
        articles_list = ArticleModel.query.filter(
            or_(
                ArticleModel.login_id == current_user.id,
                ArticleModel.is_public == True
            )
        ).filter(
            or_(
                func.lower(ArticleModel.title).contains(search_lower),
                func.lower(ArticleModel.article_text).contains(search_lower)
            )
        ).all()
    else:
        articles_list = ArticleModel.query.filter_by(is_public=True).filter(
            or_(
                func.lower(ArticleModel.title).contains(search_lower),
                func.lower(ArticleModel.article_text).contains(search_lower)
            )
        ).all()
    
    return render_template('lab8/search.html', 
                         articles=articles_list,
                         search_query=search_query)


@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')