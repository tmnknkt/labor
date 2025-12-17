from flask import Blueprint, render_template, request, jsonify, abort

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений \n приводят человечество к продовольственному кризису, коллектив \n исследователей и учёных отправляется сквозь червоточину \n (которая предположительно соединяет области пространства-времени \n через большое расстояние) в путешествие, чтобы превзойти прежние \n ограничения для космических путешествий человека и найти планету \n с подходящими для человечества условиями."
    },
    {
        "title": "The Shawshank Redemption",
        "title_ru": "Побег из Шоушенка",
        "year": 1994,
        "description": "Бухгалтер Энди Дюфрейн обвинён в убийстве собственной \n жены и её любовника. Оказавшись в тюрьме под названием Шоушенк, он \n сталкивается с жестокостью и беззаконием, царящими по обе стороны \n решётки. Каждый, кто попадает в эти стены, становится их рабом до \n конца жизни. Но Энди, обладающий живым умом и доброй душой, \n находит подход как к заключённым, так и к охранникам, добиваясь их \n особого к себе расположения."
    },
    {
        "title": "The Dark Knight",
        "title_ru": "Тёмный рыцарь",
        "year": 2008,
        "description": "Когда Бэтмен и комиссар Гордон сталкиваются с новым врагом, хаотичным Джокером, они понимают, что их битва за Готэм только начинается. Джокер стремится доказать, что даже самые благородные люди могут пасть под натиском отчаяния и хаоса."
    },
    {
        "title": "Pulp Fiction",
        "title_ru": "Криминальное чтиво",
        "year": 1994,
        "description": "Две банды убийц, боксёр-неудачник, жена гангстера и пара случайных грабителей впутываются в череду непредсказуемых и комичных событий в Лос-Анджелесе."
    },
    {
        "title": "Forrest Gump",
        "title_ru": "Форрест Гамп",
        "year": 1994,
        "description": "Жизнь Форреста Гампа, человека с низким IQ, который, тем не менее, становится свидетелем и участником ключевых событий американской истории второй половины XX века."
    }
]


def normalize_film_data(film_data):

    if 'title_ru' in film_data and film_data['title_ru']:

        if 'title' not in film_data or not film_data['title'] or film_data['title'].strip() == '':
            film_data['title'] = film_data['title_ru']
    return film_data


def ensure_films_consistency():
    for film in films:
        if 'title' not in film or not film['title'] or film['title'].strip() == '':
            if 'title_ru' in film and film['title_ru']:
                film['title'] = film['title_ru']


ensure_films_consistency()


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404, description=f"Фильм с ID {id} не найден. Доступные ID: от 0 до {len(films)-1}")
    
    return jsonify(films[id])


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return jsonify({
            "error": "Film not found",
            "message": f"Фильм с ID {id} не найден. Доступные ID: от 0 до {len(films)-1}"
        }), 404
    
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return jsonify({
            "error": "Film not found",
            "message": f"Фильм с ID {id} не найден. Доступные ID: от 0 до {len(films)-1}"
        }), 404
    
    film = request.get_json()
    
    if not film:
        return jsonify({
            "error": "Bad request",
            "message": "Тело запроса должно содержать JSON данные фильма"
        }), 400
    
    film = normalize_film_data(film)
    
    if 'title_ru' not in film or film['title_ru'] == '':
        return jsonify({"title_ru": "Заполните русское название"}), 400
    
    if film['description'] == '':
        return jsonify({"description": "Заполните описание"}), 400

    films[id] = film
    
    return jsonify(films[id]), 200


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    
    if not film:
        abort(400, description="Тело запроса должно содержать JSON данные фильма")
    
    film = normalize_film_data(film)
    
    if 'title_ru' not in film or film['title_ru'] == '':
        return jsonify({"title_ru": "Заполните русское название"}), 400
    
    if 'description' not in film or film['description'] == '':
        return jsonify({"description": "Заполните описание"}), 400
    
    films.append(film)
    
    new_id = len(films) - 1
    return jsonify({"id": new_id}), 201