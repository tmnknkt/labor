from flask import Flask, url_for
app = Flask(__name__)

@app.route("/")
@app.route("/web")
def web():
    return """<!doctype html>
        <html>
            <body>
                <h1>web-сервер на flask<h1>
                <a href="/author">author</a>
            </body>
        </html>"""

@app.route("/author")
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
                <a href="/web">web</a>
            </body>
        </html>"""

@app.route("/image")
def image():
    path = url_for("static", filename="oak.jpg")
    return '''
<!doctype>
<html>
    <body>
        <h1>Картинка</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''