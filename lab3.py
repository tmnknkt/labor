from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab3_3():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie/')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success') 
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    text_align = request.args.get('text_align')
    
    if any([color, bg_color, font_size, text_align]):    
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if text_align:
            resp.set_cookie('text_align', text_align)
        return resp
    
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    text_align = request.cookies.get('text_align')
    
    return render_template('lab3/settings.html', 
                         color=color,
                         bg_color=bg_color,
                         font_size=font_size,
                         text_align=text_align)


@lab3.route('/lab3/ticket', methods=['GET', 'POST'])
def ticket_form():
    errors = {}
    
    if request.method == 'POST':
        fio = request.form.get('fio')
        shelf = request.form.get('shelf')
        bedding = request.form.get('bedding')
        baggage = request.form.get('baggage')
        age = request.form.get('age')
        departure = request.form.get('departure')
        destination = request.form.get('destination')
        date = request.form.get('date')
        insurance = request.form.get('insurance')
        
        errors = {}
        
        if not fio:
            errors['fio'] = 'Заполните поле ФИО'
        if not shelf:
            errors['shelf'] = 'Выберите полку'
        if not bedding:
            errors['bedding'] = 'Укажите наличие белья'
        if not baggage:
            errors['baggage'] = 'Укажите наличие багажа'
        if not age:
            errors['age'] = 'Заполните возраст'
        elif not age.isdigit() or int(age) < 1 or int(age) > 120:
            errors['age'] = 'Возраст должен быть от 1 до 120 лет'
        if not departure:
            errors['departure'] = 'Заполните пункт выезда'
        if not destination:
            errors['destination'] = 'Заполните пункт назначения'
        if not date:
            errors['date'] = 'Выберите дату поездки'
        if not insurance:
            errors['insurance'] = 'Укажите наличие страховки'
        
        if errors:
            return render_template('lab3/ticket_form.html', errors=errors, 
                                 fio=fio, shelf=shelf, bedding=bedding, 
                                 baggage=baggage, age=age, departure=departure,
                                 destination=destination, date=date, insurance=insurance)
        
        age_int = int(age)
        if age_int < 18:
            base_price = 700  # детский 
            ticket_type = "Детский билет"
        else:
            base_price = 1000  # взрослый 
            ticket_type = "Взрослый билет"
        
        additional_cost = 0
        if shelf in ['lower', 'lower_side']:
            additional_cost += 100
        if bedding == 'yes':
            additional_cost += 75
        if baggage == 'yes':
            additional_cost += 250
        if insurance == 'yes':
            additional_cost += 150
        
        total_price = base_price + additional_cost
        
        return render_template('lab3/ticket_result.html', 
                             fio=fio, shelf=shelf, bedding=bedding,
                             baggage=baggage, age=age, departure=departure,
                             destination=destination, date=date, insurance=insurance,
                             ticket_type=ticket_type, total_price=total_price)
    
    return render_template('lab3/ticket_form.html', errors=errors)

@lab3.route('/lab3/ticket_result')
def ticket_result():
    return redirect(url_for('lab3.ticket_form'))