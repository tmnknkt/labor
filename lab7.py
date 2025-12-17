from flask import Blueprint, render_template, request, jsonify, abort
from datetime import datetime
import sqlite3
from os import path

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


def db_connect():
    try:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        raise

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


def normalize_film_data(film_data):
    if not film_data:
        return film_data
    
    if 'title_ru' in film_data and film_data['title_ru']:
        if 'title' not in film_data or not film_data['title'] or film_data['title'].strip() == '':
            film_data['title'] = film_data['title_ru']
    
    if 'title' in film_data and film_data['title']:
        if 'title_ru' not in film_data or not film_data['title_ru'] or film_data['title_ru'].strip() == '':
            film_data['title_ru'] = film_data['title']
    
    return film_data


def validate_film_data(film_data, is_update=False):
    errors = {}
    
    if 'title_ru' not in film_data or not film_data['title_ru'] or film_data['title_ru'].strip() == '':
        errors['title_ru'] = 'Заполните русское название'
    elif len(film_data['title_ru'].strip()) > 255:
        errors['title_ru'] = 'Русское название не должно превышать 255 символов'
    
    if 'title' not in film_data or not film_data['title'] or film_data['title'].strip() == '':
        errors['title'] = 'Заполните оригинальное название'
    elif len(film_data['title'].strip()) > 255:
        errors['title'] = 'Оригинальное название не должно превышать 255 символов'
    
    if 'year' not in film_data:
        errors['year'] = 'Укажите год выпуска'
    else:
        try:
            year = int(film_data['year'])
            current_year = datetime.now().year
            if year < 1895:
                errors['year'] = 'Год должен быть не менее 1895'
            elif year > current_year:
                errors['year'] = f'Год не может быть больше {current_year}'
        except (ValueError, TypeError):
            errors['year'] = 'Год должен быть числом'
    
    if 'description' not in film_data or not film_data['description'] or film_data['description'].strip() == '':
        errors['description'] = 'Заполните описание'
    else:
        desc_len = len(film_data['description'].strip())
        if desc_len == 0:
            errors['description'] = 'Заполните описание'
        elif desc_len > 2000:
            errors['description'] = 'Описание не должно превышать 2000 символов'
    
    return errors


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    try:
        cur.execute("SELECT * FROM films ORDER BY id")
        films = cur.fetchall()
        
        result = []
        for film in films:
            result.append(dict(film))
        
        return jsonify(result)
    except Exception as e:
        print(f"Ошибка при получении фильмов: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    try:
        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
        film = cur.fetchone()
        
        if not film:
            abort(404, description=f"Фильм с ID {id} не найден")
        
        return jsonify(dict(film))
    except Exception as e:
        print(f"Ошибка при получении фильма: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    conn, cur = db_connect()
    try:
        cur.execute("SELECT id FROM films WHERE id = ?", (id,))
        if not cur.fetchone():
            return jsonify({
                "error": "Film not found",
                "message": f"Фильм с ID {id} не найден"
            }), 404
        
        cur.execute("DELETE FROM films WHERE id = ?", (id,))
        return '', 204
    except Exception as e:
        print(f"Ошибка при удалении фильма: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    film = request.get_json()
    
    if not film:
        return jsonify({
            "error": "Bad request",
            "message": "Тело запроса должно содержать JSON данные фильма"
        }), 400
    
    film = normalize_film_data(film)
    
    errors = validate_film_data(film, is_update=True)
    if errors:
        return jsonify(errors), 400
    
    conn, cur = db_connect()
    try:
        cur.execute("SELECT id FROM films WHERE id = ?", (id,))
        if not cur.fetchone():
            return jsonify({
                "error": "Film not found",
                "message": f"Фильм с ID {id} не найден"
            }), 404
        
        cur.execute("""
            UPDATE films 
            SET title = ?, title_ru = ?, year = ?, description = ? 
            WHERE id = ?
        """, (
            film['title'].strip(),
            film['title_ru'].strip(),
            int(film['year']),
            film['description'].strip(),
            id
        ))
        
        cur.execute("SELECT * FROM films WHERE id = ?", (id,))
        updated_film = cur.fetchone()
        
        return jsonify(dict(updated_film)), 200
    except Exception as e:
        print(f"Ошибка при обновлении фильма: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500
    finally:
        db_close(conn, cur)


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    if not film:
        return jsonify({
            "error": "Bad request",
            "message": "Тело запроса должно содержать JSON данные фильма"
        }), 400
    
    film = normalize_film_data(film)
    
    errors = validate_film_data(film)
    if errors:
        return jsonify(errors), 400
    
    conn, cur = db_connect()
    try:
        cur.execute("""
            INSERT INTO films (title, title_ru, year, description) 
            VALUES (?, ?, ?, ?)
        """, (
            film['title'].strip(),
            film['title_ru'].strip(),
            int(film['year']),
            film['description'].strip()
        ))
        
        new_id = cur.lastrowid
        
        return jsonify({"id": new_id}), 201
    except Exception as e:
        print(f"Ошибка при добавлении фильма: {e}")
        return jsonify({"error": "Ошибка сервера"}), 500
    finally:
        db_close(conn, cur)


