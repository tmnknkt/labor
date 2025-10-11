from flask import Blueprint, url_for, request, redirect, abort, render_template
import datetime
lab1 = Blueprint('lab2', __name__)


@app.route('/lab2/a')
def a():
    return 'без слэша'


@app.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = [
    {'name': 'роза', 'price': 150},
    {'name': 'тюльпан', 'price': 80},
    {'name': 'незабудка', 'price': 50},
    {'name': 'ромашка', 'price': 40}
]


@app.route ('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        abort(404)
    else:
        return render_template('flower_detail.html', 
                             flower=flower_list[flower_id], 
                             flower_id=flower_id,
                             total_flowers=len(flower_list))


@app.route ('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return render_template('flower_added.html', name=name,
                           flower_list=flower_list,
                           new_id=len(flower_list)-1)


@app.route('/lab2/add_flower/')
def add_flower_form():
    flower_name = request.args.get('flower_name', '').strip()
    if not flower_name:
        abort(400, description="Вы не задали имя цветка")
    
    flower_list.append({'name': flower_name, 'price': 0})
    return redirect('/lab2/all_flowers')


@app.route('/lab2/all_flowers')
def all_flowers():
    return render_template('all_flowers.html', 
                         flowers=flower_list, 
                         count=len(flower_list))


@app.route('/lab2/del_flower/<int:num>')
def del_flower(num):
    if num < 0 or num >= len(flower_list):
        abort(404)
    flower_list.pop(num)
    return redirect('/lab2/all_flowers')


@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect('/lab2/all_flowers')


@app.route('/lab2/example')
def example():
    name = 'Атаманкина Екатерина'
    number_lr = 'Лабораторная работа 2'
    group = 'ФБИ-33'
    year = '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html'
                           , 
                         name=name, 
                         number_lr=number_lr, 
                         group=group, 
                         year=year,
                         fruits=fruits
                         )


@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')


@app.route('/lab2/filters')
def filterd():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)


@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    operations = {
        'Сложение': a + b,
        'Вычитание': a - b,
        'Умножение': a * b,
        'Деление': a / b if b != 0 else 'Ошибка: деление на ноль',
        'Возведение в степень': a ** b
    }
    
    return render_template('calculator.html', 
                         a=a, 
                         b=b, 
                         operations=operations)


@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))


@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(url_for('calc', a=a, b=1))


books = [
    {'title': 'Мастер и Маргарита', 'author': 'Михаил Булгаков', 'genre': 'Роман', 'pages': 480},
    {'title': 'Преступление и наказание', 'author': 'Фёдор Достоевский', 'genre': 'Психологический роман', 'pages': 672},
    {'title': 'Война и мир', 'author': 'Лев Толстой', 'genre': 'Эпопея', 'pages': 1225},
    {'title': '1984', 'author': 'Джордж Оруэлл', 'genre': 'Антиутопия', 'pages': 328},
    {'title': 'Гарри Поттер и философский камень', 'author': 'Джоан Роулинг', 'genre': 'Фэнтези', 'pages': 432},
    {'title': 'Три товарища', 'author': 'Эрих Мария Ремарк', 'genre': 'Роман', 'pages': 480},
    {'title': 'Маленький принц', 'author': 'Антуан де Сент-Экзюпери', 'genre': 'Философская сказка', 'pages': 96},
    {'title': 'Шерлок Холмс', 'author': 'Артур Конан Дойл', 'genre': 'Детектив', 'pages': 320},
    {'title': 'Убить пересмешника', 'author': 'Харпер Ли', 'genre': 'Роман воспитания', 'pages': 416},
    {'title': 'Гордость и предубеждение', 'author': 'Джейн Остин', 'genre': 'Любовный роман', 'pages': 480}
]


@app.route('/lab2/books')
def books_list():
    return render_template('books.html', books=books)


dog_breeds = [
    {
        'name': 'Лабрадор-ретривер',
        'description': 'Дружелюбная, энергичная порода. Отличный компаньон для семьи.',
        'image': 'labrador.jpg'
    },
    {
        'name': 'Немецкая овчарка',
        'description': 'Умная, преданная собака. Часто используется в полиции и армии.',
        'image': 'german_shepherd.jpg'
    },
    {
        'name': 'Золотистый ретривер',
        'description': 'Добродушная, интеллигентная порода. Любит детей и игры.',
        'image': 'golden_retriever.jpg'
    },
    {
        'name': 'Французский бульдог',
        'description': 'Компактная, дружелюбная собака с большими ушами.',
        'image': 'french_bulldog.jpg'
    },
    {
        'name': 'Бигль',
        'description': 'Энергичная гончая с отличным нюхом. Любит исследовать территорию.',
        'image': 'beagle.jpg'
    },
    {
        'name': 'Пудель',
        'description': 'Умная, элегантная порода. Бывает разных размеров.',
        'image': 'poodle.jpg'
    },
    {
        'name': 'Ротвейлер',
        'description': 'Сильная, уверенная собака. Нуждается в ранней социализации.',
        'image': 'rottweiler.jpg'
    },
    {
        'name': 'Йоркширский терьер',
        'description': 'Маленькая, но смелая собака с длинной шелковистой шерстью.',
        'image': 'yorkshire.jpg'
    },
    {
        'name': 'Такса',
        'description': 'Смелая и любопытная порода с длинным телом и короткими лапами.',
        'image': 'dachshund.jpg'
    },
    {
        'name': 'Сибирский хаски',
        'description': 'Энергичная ездовая собака с голубыми глазами и густой шерстью.',
        'image': 'husky.jpg'
    },
    {
        'name': 'Доберман',
        'description': 'Элегантная, преданная порода с отличными охранными качествами.',
        'image': 'doberman.jpg'
    },
    {
        'name': 'Боксер',
        'description': 'Энергичная, игривая собака с выразительной мордой.',
        'image': 'boxer.jpg'
    },
    {
        'name': 'Шпиц',
        'description': 'Пушистая, жизнерадостная собака с лисьей мордочкой.',
        'image': 'spitz.jpg'
    },
    {
        'name': 'Чихуахуа',
        'description': 'Самая маленькая порода собак. Смелая и преданная.',
        'image': 'chihuahua.jpg'
    },
    {
        'name': 'Мопс',
        'description': 'Добродушная, компактная порода с морщинистой мордой.',
        'image': 'pug.jpg'
    },
    {
        'name': 'Акита-ину',
        'description': 'Японская порода, известная преданностью и достоинством.',
        'image': 'akita.jpg'
    },
    {
        'name': 'Корги',
        'description': 'Невысокая пастушья собака с умным выражением морды.',
        'image': 'corgi.jpg'
    },
    {
        'name': 'Шарпей',
        'description': 'Уникальная порода с синеватым языком и многочисленными складками.',
        'image': 'sharpei.jpg'
    },
    {
        'name': 'Далматин',
        'description': 'Элегантная собака с характерным пятнистым окрасом.',
        'image': 'dalmatian.jpg'
    },
    {
        'name': 'Самоед',
        'description': 'Пушистая белая собака с "улыбающимся" выражением морды.',
        'image': 'samoyed.jpg'
    }
]


@app.route('/lab2/dogs')
def dogs_list():
    return render_template('dogs.html', dogs=dog_breeds)