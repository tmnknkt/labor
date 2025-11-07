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



user_list = [
    {'login': 'alex', 'password': '123', 'name': 'Алексей', 'gender': 'male'},
    {'login': 'bob', 'password': '555', 'name': 'Борис', 'gender': 'male'},
    {'login': 'katya', 'password': '177', 'name': 'Екатерина', 'gender': 'female'},
    {'login': 'pop', 'password': '111', 'name': 'Петр', 'gender': 'male'},
]


@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab4/register.html')
    
    login = request.form.get('login', '')
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    name = request.form.get('name', '')
    
    if not login:
        return render_template('lab4/register.html', error='Не введён логин', login=login, name=name)
    if not password:
        return render_template('lab4/register.html', error='Не введён пароль', login=login, name=name)
    if not confirm_password:
        return render_template('lab4/register.html', error='Не введено подтверждение пароля', login=login, name=name)
    if not name:
        return render_template('lab4/register.html', error='Не введено имя', login=login, name=name)
    if password != confirm_password:
        return render_template('lab4/register.html', error='Пароли не совпадают', login=login, name=name)
    
    for user in user_list:
        if user['login'] == login:
            return render_template('lab4/register.html', error='Логин уже существует', login=login, name=name)
    
    user_list.append({
        'login': login,
        'password': password,
        'name': name
    })
    
    return redirect('/lab4/login')

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login_session = session['login']
            user_name = ''
            for user in user_list:
                if user['login'] == login_session:
                    user_name = user['name']
                    break
            return render_template('lab4/login.html', authorized=authorized, name=user_name)
        else:
            authorized = False
            return render_template('lab4/login.html', authorized=authorized)

    login_form = request.form.get('login', '')
    password = request.form.get('password', '')

    if not login_form:
        return render_template('lab4/login.html', error='Не введён логин', login=login_form, authorized=False)
    if not password:
        return render_template('lab4/login.html', error='Не введён пароль', login=login_form, authorized=False)

    for user in user_list:
        if login_form == user['login'] and password == user['password']:
            session['login'] = login_form
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, login=login_form, authorized=False)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/users')
def users():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    return render_template('lab4/users.html', users=user_list, current_user=session['login'])

@lab4.route('/lab4/delete_user', methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    login = session['login']
    global user_list

    user_list = [user for user in user_list if user['login'] != login]
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/edit_user', methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    if request.method == 'GET':
        current_login = session['login']
        user_data = None
        for user in user_list:
            if user['login'] == current_login:
                user_data = user
                break
        
        if not user_data:
            return redirect('/lab4/login')
        
        return render_template('lab4/edit_user.html', 
                             login=user_data['login'], 
                             name=user_data['name'])
    
    current_login = session['login']
    new_login = request.form.get('login', '')
    name = request.form.get('name', '')
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    
    if not new_login:
        return render_template('lab4/edit_user.html', error='Не введён логин', login=new_login, name=name)
    if not name:
        return render_template('lab4/edit_user.html', error='Не введено имя', login=new_login, name=name)
    if password and password != confirm_password:
        return render_template('lab4/edit_user.html', error='Пароли не совпадают', login=new_login, name=name)
    
    for user in user_list:
        if user['login'] == new_login and user['login'] != current_login:
            return render_template('lab4/edit_user.html', error='Логин уже существует', login=new_login, name=name)
    
    for user in user_list:
        if user['login'] == current_login:
            user['login'] = new_login
            user['name'] = name
            if password:
                user['password'] = password
            session['login'] = new_login
            break
    
    return redirect('/lab4/users')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        return render_template('lab4/fridge.html')
    
    temperature = request.form.get('temperature')
    
    if not temperature:
        return render_template('lab4/fridge.html', error='Ошибка: не задана температура')
    
    try:
        temp = int(temperature)
    except ValueError:
        return render_template('lab4/fridge.html', error='Ошибка: температура должна быть числом')
    
    if temp < -12:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком низкое значение')
    elif temp > -1:
        return render_template('lab4/fridge.html', error='Не удалось установить температуру — слишком высокое значение')
    elif -12 <= temp <= -9:
        snowflakes = 3
    elif -8 <= temp <= -5:
        snowflakes = 2
    elif -4 <= temp <= -1:
        snowflakes = 1
    else:
        snowflakes = 0
    
    return render_template('lab4/fridge.html', temperature=temp, snowflakes=snowflakes)


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    if request.method == 'GET':
        return render_template('lab4/grain.html')
    
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    if not weight:
        return render_template('lab4/grain.html', error='Не указан вес')
    
    try:
        weight_num = float(weight)
    except ValueError:
        return render_template('lab4/grain.html', error='Вес должен быть числом')
    
    if weight_num <= 0:
        return render_template('lab4/grain.html', error='Вес должен быть положительным числом')
    
    if weight_num > 100:
        return render_template('lab4/grain.html', error='Такого объёма сейчас нет в наличии')
    
    prices = {
        'barley': 12000,
        'oats': 8500,
        'wheat': 9000,
        'rye': 15000
    }
    
    grain_names = {
        'barley': 'ячмень',
        'oats': 'овёс',
        'wheat': 'пшеница',
        'rye': 'рожь'
    }
    
    price_per_ton = prices.get(grain_type)
    grain_name = grain_names.get(grain_type)
    
    total = weight_num * price_per_ton
    
    discount = 0
    if weight_num > 10:
        discount = total * 0.10
        total -= discount
    
    return render_template('lab4/grain.html', 
                         grain_name=grain_name,
                         weight=weight_num,
                         total=total,
                         discount=discount,
                         has_discount=weight_num > 10)