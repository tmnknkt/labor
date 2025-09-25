from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    pat = url_for("static", filename="pp.jpg")
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>404 - Страница не найдена</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
        }
        h1 {
            color: red;
            font-size: 50px;
        }
        img {
            width: 200px;
            margin: 20px;
        }
    </style>
</head>
<body>
    <h1>404</h1>
    <h2>Страница не найдена</h2>
    <p>Извините, такой страницы не существует.</p>
    <img src="''' + pat + '''">
</body>
</html>
''', 404

@app.route("/")
@app.route('/index')
def index():
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>НГТУ, ФБ, Лабораторные работы</title>
</head>
<body>
    <div class="container">
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        
        <nav>
            <a href="/lab1">Первая лабораторная</a>
        </nav>
                
        <footer>
            <p>Атаманкина Екатерина Романовна</p>
            <p>ФБИ-33</p>
            <p>3 курс</p>
            <p>2025</p>
        </footer>
    </div>
</body>
</html>
'''

@app.route('/lab1')
def lab1():
    return '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>НГТУ, ФБ, Первая лабораторная</title>
</head>
<body>
    <div class="container">
        <header>
            <h1>Лабораторная 1</h1>
        </header>
        
        <div>
        Flask — фреймворк для создания веб-приложений на языке
программирования Python, использующий набор инструментов
Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
называемых микрофреймворков — минималистичных каркасов
веб-приложений, сознательно предоставляющих лишь самые базовые возможности. <br>
            <a href="/">Ссылка на корень сайта</a><br>
        </div>
        <nav>
            <a href="/lab1/info">Информация</a><br>
            <a href="/lab1/web">Web</a><br>
            <a href="/lab1/image">Картинка</a><br>
            <a href="/lab1/counter">Счетчик</a><br>
            <a href="/lab1/created">Created</a><br>
        </nav>
                
        <footer>
            <p>Атаманкина Екатерина Романовна</p>
            <p>ФБИ-33</p>
            <p>3 курс</p>
            <p>2025</p>
        </footer>
    </div>
</body>
</html>
'''

@app.route("/lab1/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask<h1>
                <a href="/author">author</a>
            </body>
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8'
            }

@app.route("/lab1/author")
def author():
    name = "Атаманкина Екатерина Романовна"
    group = "ФБИ-33"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факультет: """ + faculty + """</p>
                <a href="/lab1/web">web</a>
            </body>
        </html>"""

@app.route("/lab1/image")
def image():
    path = url_for("static", filename="oak.jpg")
    css_path = url_for("static", filename="lab1.css") 
    return '''
<!doctype>
<html>
    <head>
        <link rel="stylesheet" href="''' + css_path + '''">
    </head>
    <body>
        <h1>Картинка</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1

    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
        <hr>
        Дата и время: ''' + str(time) + '''<br>
        Запрошенный адрес: ''' + url + '''<br>
        Ваш IP-адрес: ''' + client_ip + '''<br>
        <hr>
        <a href="''' + url_for('clear_counter') + '''">Очистить счетчик</a>
    </body>
</html>
'''

@app.route('/lab1/clear_counter')
def clear_counter():
    global count
    count = 0
    return redirect(url_for('counter'))

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

@app.route("/lab1/created")
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Создано успешно</h1>
        <div><i>Что-то создано...</i></div>
    </body>
<html>
''', 201

@app.route('/lab1/400')
def bad_request():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>400 Bad Request</title>
</head>
<body>
    <h1>400 Bad Request</h1>
    <p>Сервер не может обработать запрос из-за синтаксической ошибки.</p>
    <p>Пожалуйста, проверьте правильность запроса.</p>
</body>
</html>
''', 400

@app.route('/lab1/401')
def unauthorized():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>401 Unauthorized</title>
</head>
<body>
    <h1>401 Unauthorized</h1>
    <p>Для доступа к этой странице требуется аутентификация.</p>
    <p>Пожалуйста, предоставьте действительные учетные данные.</p>
</body>
</html>
''', 401

@app.route('/lab1/402')
def payment_required():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>402 Payment Required</title>
</head>
<body>
    <h1>402 Payment Required</h1>
    <p>Для доступа к этому ресурсу требуется оплата.</p>
    <p>Данный код зарезервирован для будущего использования.</p>
</body>
</html>
''', 402

@app.route('/lab1/403')
def forbidden():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>403 Forbidden</title>
</head>
<body>
    <h1>403 Forbidden</h1>
    <p>Доступ к этому ресурсу запрещен.</p>
    <p>У вас недостаточно прав для просмотра этой страницы.</p>
</body>
</html>
''', 403

@app.route('/lab1/405')
def method_not_allowed():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>405 Method Not Allowed</title>
</head>
<body>
    <h1>405 Method Not Allowed</h1>
    <p>Метод запроса не поддерживается для данного ресурса.</p>
    <p>Пожалуйста, используйте допустимый HTTP-метод.</p>
</body>
</html>
''', 405

@app.route('/lab1/418')
def im_a_teapot():
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>418 I'm a teapot</title>
</head>
<body>
    <h1>418 I'm a teapot</h1>
    <p>Я - чайник и не могу заваривать кофе.</p>
    <p>Это шутливый код состояния HTTP из RFC 2324.</p>
</body>
</html>
''', 418