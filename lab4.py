from flask import Blueprint, render_template, request, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div', methods=['GET', 'POST'])
def div():
    if request.method == 'POST':
        x1 = request.form.get('x1')
        x2 = request.form.get('x2')
        if x1 == '' or x2 == '':
            return render_template('lab4/div-form.html', error='Оба поля должны быть заполнены!')
        
        x1 = int(x1)
        x2 = int(x2)
        
        if x2 == 0:
            return render_template('lab4/div-form.html', error='Деление на ноль невозможно!')
        
        result = x1 / x2
        return render_template('lab4/div-form.html', x1=x1, x2=x2, result=result)
    else:
        return render_template('lab4/div-form.html')
    

@lab4.route('/lab4/sum', methods=['GET', 'POST'])
def sum():
    x1 = request.form.get('x1', '')
    x2 = request.form.get('x2', '')
    result = None
    
    if request.method == 'POST':
        x1_num = int(x1) if x1 != '' else 0
        x2_num = int(x2) if x2 != '' else 0
        result = x1_num + x2_num
    
    return render_template('lab4/sum-form.html', 
                         x1=x1, x2=x2, result=result)


@lab4.route('/lab4/mult', methods=['GET', 'POST'])
def mult():
    x1 = request.form.get('x1', '')
    x2 = request.form.get('x2', '')
    result = None
    
    if request.method == 'POST':
        x1_num = int(x1) if x1 != '' else 1
        x2_num = int(x2) if x2 != '' else 1
        result = x1_num * x2_num
    
    return render_template('lab4/mult-form.html', 
                         x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub', methods=['GET', 'POST'])
def sub():
    x1 = request.form.get('x1', '')
    x2 = request.form.get('x2', '')
    error = None
    result = None
    
    if request.method == 'POST':
        if x1 == '' or x2 == '':
            error = 'Оба поля должны быть заполнены!'
        else:
            try:
                x1_num = int(x1)
                x2_num = int(x2)
                result = x1_num - x2_num
            except ValueError:
                error = 'Введите целые числа!'
    
    return render_template('lab4/sub-form.html', 
                         x1=x1, x2=x2, result=result, error=error)


@lab4.route('/lab4/pow', methods=['GET', 'POST'])
def pow():
    x1 = request.form.get('x1', '')
    x2 = request.form.get('x2', '')
    error = None
    result = None
    
    if request.method == 'POST':
        if x1 == '' or x2 == '':
            error = 'Оба поля должны быть заполнены!'
        else:
            try:
                x1_num = int(x1)
                x2_num = int(x2)
                
                if x1_num == 0 and x2_num == 0:
                    error = 'Ноль в нулевой степени не определен!'
                else:
                    result = x1_num ** x2_num
            except ValueError:
                error = 'Введите целые числа!'
    
    return render_template('lab4/pow-form.html', 
                         x1=x1, x2=x2, result=result, error=error)


tree_count = 0


@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1

    return redirect('/lab4/tree')



users = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Борис', 'gender': 'male'},
    {'login': 'katya', 'password': '177', 'name': 'Екатерина', 'gender': 'female'},
    {'login': 'pop', 'password': '111', 'name': 'Петр', 'gender': 'male'},
]


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            user_name = ''
            for user in users:
                if user['login'] == login:
                    user_name = user['name']
                    break
            return render_template('lab4/login.html', authorized=authorized, name=user_name)
        else:
            authorized = False
            return render_template('lab4/login.html', authorized=authorized)

    login = request.form.get('login', '')
    password = request.form.get('password', '')

    if not login:
        return render_template('lab4/login.html', error='Не введён логин', login=login, authorized=False)
    if not password:
        return render_template('lab4/login.html', error='Не введён пароль', login=login, authorized=False)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, login=login, authorized=False)


@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')