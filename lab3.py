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


@lab3.route('/lab3/settings/clear')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    
    resp.set_cookie('color', '', expires=0)
    resp.set_cookie('bg_color', '', expires=0)
    resp.set_cookie('font_size', '', expires=0)
    resp.set_cookie('text_align', '', expires=0)
    
    return resp


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



PRODUCTS = [
    {'id': 1, 'name': 'iPhone 15', 'price': 89990, 'brand': 'Apple', 'color': 'черный', 'weight': 171},
    {'id': 2, 'name': 'Samsung Galaxy S24', 'price': 74990, 'brand': 'Samsung', 'color': 'белый', 'weight': 167},
    {'id': 3, 'name': 'Xiaomi Redmi Note 13', 'price': 24990, 'brand': 'Xiaomi', 'color': 'синий', 'weight': 188},
    {'id': 4, 'name': 'Google Pixel 8', 'price': 69990, 'brand': 'Google', 'color': 'серый', 'weight': 187},
    {'id': 5, 'name': 'OnePlus 11', 'price': 54990, 'brand': 'OnePlus', 'color': 'зеленый', 'weight': 205},
    {'id': 6, 'name': 'Realme 11 Pro+', 'price': 32990, 'brand': 'Realme', 'color': 'золотой', 'weight': 183},
    {'id': 7, 'name': 'iPhone 14', 'price': 69990, 'brand': 'Apple', 'color': 'красный', 'weight': 172},
    {'id': 8, 'name': 'Samsung Galaxy A54', 'price': 34990, 'brand': 'Samsung', 'color': 'фиолетовый', 'weight': 202},
    {'id': 9, 'name': 'Huawei P60 Pro', 'price': 79990, 'brand': 'Huawei', 'color': 'черный', 'weight': 200},
    {'id': 10, 'name': 'Honor 90', 'price': 29990, 'brand': 'Honor', 'color': 'синий', 'weight': 183},
    {'id': 11, 'name': 'Sony Xperia 5 V', 'price': 84990, 'brand': 'Sony', 'color': 'черный', 'weight': 182},
    {'id': 12, 'name': 'Motorola Edge 40', 'price': 39990, 'brand': 'Motorola', 'color': 'зеленый', 'weight': 167},
    {'id': 13, 'name': 'Nokia G42', 'price': 19990, 'brand': 'Nokia', 'color': 'фиолетовый', 'weight': 193},
    {'id': 14, 'name': 'iPhone 13', 'price': 59990, 'brand': 'Apple', 'color': 'розовый', 'weight': 174},
    {'id': 15, 'name': 'Samsung Galaxy Z Flip5', 'price': 99990, 'brand': 'Samsung', 'color': 'сиреневый', 'weight': 187},
    {'id': 16, 'name': 'Xiaomi 13T', 'price': 44990, 'brand': 'Xiaomi', 'color': 'черный', 'weight': 197},
    {'id': 17, 'name': 'Google Pixel 7a', 'price': 44990, 'brand': 'Google', 'color': 'белый', 'weight': 193},
    {'id': 18, 'name': 'Nothing Phone (2)', 'price': 49990, 'brand': 'Nothing', 'color': 'белый', 'weight': 201},
    {'id': 19, 'name': 'Asus Zenfone 10', 'price': 59990, 'brand': 'Asus', 'color': 'синий', 'weight': 172},
    {'id': 20, 'name': 'Oppo Find X6 Pro', 'price': 89990, 'brand': 'Oppo', 'color': 'черный', 'weight': 216}
]

@lab3.route('/lab3/products')
def products():
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    
    min_price_form = request.args.get('min_price')
    max_price_form = request.args.get('max_price')

    min_price = None
    max_price = None
    
    if min_price_form or max_price_form:
        min_price = int(min_price_form) if min_price_form else None
        max_price = int(max_price_form) if max_price_form else None
        
        if min_price and max_price and min_price > max_price:
            min_price, max_price = max_price, min_price
    elif min_price_cookie or max_price_cookie:
        min_price = int(min_price_cookie) if min_price_cookie else None
        max_price = int(max_price_cookie) if max_price_cookie else None
    
    filtered_products = []
    for product in PRODUCTS:
        price = product['price']
        if min_price and max_price:
            if min_price <= price <= max_price:
                filtered_products.append(product)
        elif min_price:
            if price >= min_price:
                filtered_products.append(product)
        elif max_price:
            if price <= max_price:
                filtered_products.append(product)
        else:
            filtered_products.append(product)
    
    all_prices = [p['price'] for p in PRODUCTS]
    global_min_price = min(all_prices)
    global_max_price = max(all_prices)
    
    resp = None
    if min_price_form or max_price_form:
        resp = make_response(render_template('lab3/products.html',
                           products=filtered_products,
                           min_price=min_price,
                           max_price=max_price,
                           global_min_price=global_min_price,
                           global_max_price=global_max_price,
                           products_count=len(filtered_products)))
        
        if min_price_form:
            resp.set_cookie('min_price', min_price_form)
        if max_price_form:
            resp.set_cookie('max_price', max_price_form)
    else:
        resp = make_response(render_template('lab3/products.html',
                           products=filtered_products,
                           min_price=min_price,
                           max_price=max_price,
                           global_min_price=global_min_price,
                           global_max_price=global_max_price,
                           products_count=len(filtered_products)))
    
    return resp

@lab3.route('/lab3/products/clear')
def clear_products_filter():
    resp = make_response(redirect('/lab3/products'))
    resp.set_cookie('min_price', '', expires=0)
    resp.set_cookie('max_price', '', expires=0)
    return resp