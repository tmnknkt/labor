from flask import Flask, url_for, request, redirect, abort, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
import datetime

app = Flask(__name__)


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')


app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)


# Глобальная переменная для хранения лога (в реальном приложении лучше использовать БД)
access_log = []


@app.errorhandler(404)
def not_found(err):
    # Получаем данные о запросе
    client_ip = request.remote_addr
    access_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url
    user_agent = request.headers.get('User-Agent', 'Неизвестно')
    
    # Добавляем запись в лог
    log_entry = {
        'ip': client_ip,
        'time': access_time,
        'url': requested_url,
        'user_agent': user_agent
    }
    access_log.append(log_entry)
    
    # Формируем HTML с логом
    log_html = '<h3>История обращений к несуществующим страницам:</h3>'
    log_html += '<table border="1" style="margin: 20px auto; border-collapse: collapse;">'
    log_html += '<tr><th>Время</th><th>IP-адрес</th><th>Запрошенный URL</th><th>User-Agent</th></tr>'
    
    for entry in reversed(access_log[-10:]):  # Показываем последние 10 записей
        log_html += f'''
        <tr>
            <td>{entry['time']}</td>
            <td>{entry['ip']}</td>
            <td>{entry['url']}</td>
            <td style="max-width: 300px; overflow: hidden; text-overflow: ellipsis;">{entry['user_agent']}</td>
        </tr>
        '''
    
    log_html += '</table>'
    
    pat = url_for("static", filename="pp.jpg")
    
    return f'''
<!DOCTYPE html>
<html>
<head>
    <title>404 - Страница не найдена</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1 {{
            color: red;
            font-size: 50px;
        }}
        .info {{
            background: #f5f5f5;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
            text-align: left;
            display: inline-block;
        }}
        img {{
            width: 200px;
            margin: 20px;
        }}
        table {{
            font-size: 14px;
            width: 100%;
        }}
        th {{
            background: #e0e0e0;
            padding: 10px;
        }}
        td {{
            padding: 8px;
            border-bottom: 1px solid #ddd;
        }}
        .navigation {{
            margin: 20px 0;
        }}
        .navigation a {{
            margin: 0 10px;
            padding: 10px 20px;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <h1>404</h1>
    <h2>Страница не найдена</h2>
    
    <div class="info">
        <strong>Информация о запросе:</strong><br>
        IP-адрес: {client_ip}<br>
        Дата и время: {access_time}<br>
        Запрошенный URL: {requested_url}<br>
        Браузер: {user_agent}
    </div>
    
    <img src="{pat}" alt="Ошибка 404">
    
    <div class="navigation">
        <a href="/">Вернуться на главную страницу</a>
    </div>
    
    {log_html}

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
            <a href="/lab1">Первая лабораторная</a><br>
            <a href="/lab2">Вторая лабораторная</a><br>
            <a href="/lab3">Третья лабораторная</a><br>
            <a href="/lab4">Четвертая лабораторная</a><br>
            <a href="/lab5">Пятая лабораторная</a><br>
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


@app.errorhandler(500)
def internal_server_error(error):
    return '''
<html>
<body>
    <h1>500 - Ошибка сервера</h1>
    <p>На сервере произошла внутренняя ошибка.</p>
    <p>Попробуйте обновить страницу или вернуться позже.</p>
</body>
</html>
''', 500