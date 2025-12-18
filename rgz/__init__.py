from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import re
import sqlite3
import os
from pathlib import Path

rgz_bp = Blueprint('rgz', __name__)

STUDENT_INFO = {
    'full_name': 'Атаманкина Екатерина Романовна',
    'group': 'ФБИ-33'
}

ADMIN_CREDENTIALS = {
    'login': 'admin',
    'password': 'Admin123!'
}

def get_db_config():
    return current_app.config.get('DB_TYPE', 'sqlite')

def db_connect():
    db_type = get_db_config()
    
    if db_type == 'postgres':
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            
            conn = psycopg2.connect(
                host='localhost',
                database='atamankina_knowledge_base',
                user='tmnknkt',
                password='111'
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
            return conn, cur, 'postgres'
        except Exception as e:
            print(f"Ошибка подключения к PostgreSQL: {e}")
            raise
    else:
        dir_path = Path(__file__).parent.parent
        db_path = dir_path / "database.db"
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  
        cur = conn.cursor()
        return conn, cur, 'sqlite'

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

# ========== ВАЛИДАЦИЯ ==========

def validate_login(login):

    if not login or len(login) < 3:
        return False, "Логин должен содержать минимум 3 символа"
    if not re.match(r'^[a-zA-Z0-9._-]+$', login):
        return False, "Логин может содержать только латинские буквы, цифры, точки, дефисы и подчеркивания"
    return True, ""

def validate_password(password):

    if not password or len(password) < 6:
        return False, "Пароль должен содержать минимум 6 символов"
    if not re.search(r'\d', password) or not re.search(r'[a-zA-Z]', password):
        return False, "Пароль должен содержать хотя бы одну букву и одну цифру"
    return True, ""

# ========== МАРШРУТЫ ==========

@rgz_bp.route('/')
def index():
    """Главная страница магазина"""
    conn, cur, db_type = db_connect()
    
    try:
        if db_type == 'postgres':
            cur.execute("SELECT * FROM furniture_products ORDER BY id LIMIT 8")
        else:
            cur.execute("SELECT * FROM furniture_products ORDER BY id LIMIT 8")
        featured_products = cur.fetchall()
        
        cur.execute("SELECT * FROM furniture_categories")
        categories = cur.fetchall()
        
        return render_template('rgz/index.html',
                             featured_products=featured_products,
                             categories=categories,
                             student_info=STUDENT_INFO,
                             login=session.get('login'))
    except Exception as e:
        flash(f'Ошибка загрузки данных: {str(e)}', 'error')
        return render_template('rgz/index.html',
                             featured_products=[],
                             categories=[],
                             student_info=STUDENT_INFO,
                             login=session.get('login'))
    finally:
        db_close(conn, cur)

@rgz_bp.route('/products')
def products():
    """Страница каталога товаров"""
    category_id = request.args.get('category', type=int)
    search = request.args.get('search', '')
    
    conn, cur, db_type = db_connect()
    
    try:
        if category_id:
            if db_type == 'postgres':
                cur.execute("""
                    SELECT p.*, c.name as category_name 
                    FROM furniture_products p 
                    JOIN furniture_categories c ON p.category_id = c.id 
                    WHERE p.category_id = %s 
                    ORDER BY p.name
                """, (category_id,))
            else:
                cur.execute("""
                    SELECT p.*, c.name as category_name 
                    FROM furniture_products p 
                    JOIN furniture_categories c ON p.category_id = c.id 
                    WHERE p.category_id = ? 
                    ORDER BY p.name
                """, (category_id,))
        elif search:
            search_term = f"%{search}%"
            if db_type == 'postgres':
                cur.execute("""
                    SELECT p.*, c.name as category_name 
                    FROM furniture_products p 
                    JOIN furniture_categories c ON p.category_id = c.id 
                    WHERE p.name ILIKE %s OR p.description ILIKE %s 
                    ORDER BY p.name
                """, (search_term, search_term))
            else:
                cur.execute("""
                    SELECT p.*, c.name as category_name 
                    FROM furniture_products p 
                    JOIN furniture_categories c ON p.category_id = c.id 
                    WHERE p.name LIKE ? OR p.description LIKE ? 
                    ORDER BY p.name
                """, (search_term, search_term))
        else:
            if db_type == 'postgres':
                cur.execute("""
                    SELECT p.*, c.name as category_name 
                    FROM furniture_products p 
                    JOIN furniture_categories c ON p.category_id = c.id 
                    ORDER BY p.category_id, p.name
                """)
            else:
                cur.execute("""
                    SELECT p.*, c.name as category_name 
                    FROM furniture_products p 
                    JOIN furniture_categories c ON p.category_id = c.id 
                    ORDER BY p.category_id, p.name
                """)
        
        products_list = cur.fetchall()
        
        cur.execute("SELECT * FROM furniture_categories ORDER BY name")
        categories = cur.fetchall()
        
        return render_template('rgz/products.html',
                             products=products_list,
                             categories=categories,
                             selected_category=category_id,
                             search_query=search,
                             student_info=STUDENT_INFO,
                             login=session.get('login'))
    except Exception as e:
        flash(f'Ошибка загрузки товаров: {str(e)}', 'error')
        return render_template('rgz/products.html',
                             products=[],
                             categories=[],
                             selected_category=None,
                             search_query=search,
                             student_info=STUDENT_INFO,
                             login=session.get('login'))
    finally:
        db_close(conn, cur)

@rgz_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """Страница товара"""
    conn, cur, db_type = db_connect()
    
    try:
        if db_type == 'postgres':
            cur.execute("""
                SELECT p.*, c.name as category_name 
                FROM furniture_products p 
                JOIN furniture_categories c ON p.category_id = c.id 
                WHERE p.id = %s
            """, (product_id,))
        else:
            cur.execute("""
                SELECT p.*, c.name as category_name 
                FROM furniture_products p 
                JOIN furniture_categories c ON p.category_id = c.id 
                WHERE p.id = ?
            """, (product_id,))
        
        product = cur.fetchone()
        
        if not product:
            flash('Товар не найден', 'error')
            return redirect('/rgz/products')
        
        return render_template('rgz/product_detail.html',
                             product=product,
                             student_info=STUDENT_INFO,
                             login=session.get('login'))
    except Exception as e:
        flash(f'Ошибка загрузки товара: {str(e)}', 'error')
        return redirect('/rgz/products')
    finally:
        db_close(conn, cur)

@rgz_bp.route('/cart')
def cart():
    """Корзина пользователя"""
    if 'login' not in session:
        flash('Для просмотра корзины необходимо авторизоваться', 'error')
        return redirect('/rgz/login')
    
    conn, cur, db_type = db_connect()
    
    try:
        if db_type == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s", (session['login'],))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?", (session['login'],))
        
        user = cur.fetchone()
        if not user:
            session.pop('login', None)
            flash('Пользователь не найден', 'error')
            return redirect('/rgz/login')
        
        user_id = user['id']
        
        if db_type == 'postgres':
            cur.execute("""
                SELECT c.*, p.name, p.price, p.image_url, p.stock 
                FROM furniture_cart c 
                JOIN furniture_products p ON c.product_id = p.id 
                WHERE c.user_id = %s 
                ORDER BY c.added_at DESC
            """, (user_id,))
        else:
            cur.execute("""
                SELECT c.*, p.name, p.price, p.image_url, p.stock 
                FROM furniture_cart c 
                JOIN furniture_products p ON c.product_id = p.id 
                WHERE c.user_id = ? 
                ORDER BY c.added_at DESC
            """, (user_id,))
        
        cart_items = cur.fetchall()
        
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        
        return render_template('rgz/cart.html',
                             cart_items=cart_items,
                             total=total,
                             student_info=STUDENT_INFO,
                             login=session.get('login'))
    except Exception as e:
        flash(f'Ошибка загрузки корзины: {str(e)}', 'error')
        return render_template('rgz/cart.html',
                             cart_items=[],
                             total=0,
                             student_info=STUDENT_INFO,
                             login=session.get('login'))
    finally:
        db_close(conn, cur)

@rgz_bp.route('/cart/add/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    """Добавление товара в корзину"""
    if 'login' not in session:
        flash('Для добавления товаров в корзину необходимо авторизоваться', 'error')
        return redirect('/rgz/login')
    
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity < 1:
        flash('Количество должно быть больше 0', 'error')
        return redirect(f'/rgz/product/{product_id}')
    
    conn, cur, db_type = db_connect()
    
    try:
        if db_type == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s", (session['login'],))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?", (session['login'],))
        
        user = cur.fetchone()
        if not user:
            session.pop('login', None)
            flash('Пользователь не найден', 'error')
            return redirect('/rgz/login')
        
        user_id = user['id']
        
        if db_type == 'postgres':
            cur.execute("SELECT stock FROM furniture_products WHERE id = %s", (product_id,))
        else:
            cur.execute("SELECT stock FROM furniture_products WHERE id = ?", (product_id,))
        
        product = cur.fetchone()
        if not product:
            flash('Товар не найден', 'error')
            return redirect('/rgz/products')
        
        if product['stock'] < quantity:
            flash('Недостаточно товара на складе', 'error')
            return redirect(f'/rgz/product/{product_id}')
        
        if db_type == 'postgres':
            cur.execute("""
                INSERT INTO furniture_cart (user_id, product_id, quantity) 
                VALUES (%s, %s, %s) 
                ON CONFLICT (user_id, product_id) 
                DO UPDATE SET quantity = furniture_cart.quantity + %s
            """, (user_id, product_id, quantity, quantity))
        else:
            cur.execute("SELECT quantity FROM furniture_cart WHERE user_id = ? AND product_id = ?", 
                       (user_id, product_id))
            existing = cur.fetchone()
            if existing:
                new_quantity = existing['quantity'] + quantity
                cur.execute("UPDATE furniture_cart SET quantity = ? WHERE user_id = ? AND product_id = ?",
                           (new_quantity, user_id, product_id))
            else:
                cur.execute("INSERT INTO furniture_cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
                           (user_id, product_id, quantity))
        
        flash('Товар добавлен в корзину', 'success')
        return redirect('/rgz/cart')
    except Exception as e:
        flash(f'Ошибка при добавлении в корзину: {str(e)}', 'error')
        return redirect(f'/rgz/product/{product_id}')
    finally:
        db_close(conn, cur)

@rgz_bp.route('/cart/update/<int:item_id>', methods=['POST'])
def update_cart(item_id):
    """Обновление количества товара в корзине"""
    if 'login' not in session:
        flash('Необходимо авторизоваться', 'error')
        return redirect('/rgz/login')
    
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity < 1:
        flash('Количество должно быть больше 0', 'error')
        return redirect('/rgz/cart')
    
    conn, cur, db_type = db_connect()
    
    try:
        if db_type == 'postgres':
            cur.execute("""
                SELECT p.stock, c.product_id
                FROM furniture_cart c 
                JOIN furniture_products p ON c.product_id = p.id 
                WHERE c.id = %s
            """, (item_id,))
        else:
            cur.execute("""
                SELECT p.stock, c.product_id
                FROM furniture_cart c 
                JOIN furniture_products p ON c.product_id = p.id 
                WHERE c.id = ?
            """, (item_id,))
        
        result = cur.fetchone()
        if not result:
            flash('Товар в корзине не найден', 'error')
            return redirect('/rgz/cart')
        
        if result['stock'] < quantity:
            flash('Недостаточно товара на складе', 'error')
            return redirect('/rgz/cart')
        
        if db_type == 'postgres':
            cur.execute("UPDATE furniture_cart SET quantity = %s WHERE id = %s", (quantity, item_id))
        else:
            cur.execute("UPDATE furniture_cart SET quantity = ? WHERE id = ?", (quantity, item_id))
        
        flash('Корзина обновлена', 'success')
        return redirect('/rgz/cart')
    except Exception as e:
        flash(f'Ошибка обновления корзины: {str(e)}', 'error')
        return redirect('/rgz/cart')
    finally:
        db_close(conn, cur)

@rgz_bp.route('/cart/remove/<int:item_id>')
def remove_from_cart(item_id):
    """Удаление товара из корзины"""
    if 'login' not in session:
        flash('Необходимо авторизоваться', 'error')
        return redirect('/rgz/login')
    
    conn, cur, db_type = db_connect()
    
    try:
        if db_type == 'postgres':
            cur.execute("DELETE FROM furniture_cart WHERE id = %s", (item_id,))
        else:
            cur.execute("DELETE FROM furniture_cart WHERE id = ?", (item_id,))
        
        flash('Товар удален из корзины', 'success')
        return redirect('/rgz/cart')
    except Exception as e:
        flash(f'Ошибка удаления товара: {str(e)}', 'error')
        return redirect('/rgz/cart')
    finally:
        db_close(conn, cur)

@rgz_bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Оформление заказа"""
    if 'login' not in session:
        flash('Для оформления заказа необходимо авторизоваться', 'error')
        return redirect('/rgz/login')
    
    if request.method == 'GET':
        conn, cur, db_type = db_connect()
        
        try:
            if db_type == 'postgres':
                cur.execute("SELECT id FROM users WHERE login = %s", (session['login'],))
            else:
                cur.execute("SELECT id FROM users WHERE login = ?", (session['login'],))
            
            user = cur.fetchone()
            if not user:
                session.pop('login', None)
                flash('Пользователь не найден', 'error')
                return redirect('/rgz/login')
            
            user_id = user['id']
            
            # Получаем товары в корзине
            if db_type == 'postgres':
                cur.execute("""
                    SELECT c.*, p.name, p.price, p.stock 
                    FROM furniture_cart c 
                    JOIN furniture_products p ON c.product_id = p.id 
                    WHERE c.user_id = %s
                """, (user_id,))
            else:
                cur.execute("""
                    SELECT c.*, p.name, p.price, p.stock 
                    FROM furniture_cart c 
                    JOIN furniture_products p ON c.product_id = p.id 
                    WHERE c.user_id = ?
                """, (user_id,))
            
            cart_items = cur.fetchall()
            
            if not cart_items:
                flash('Корзина пуста', 'error')
                return redirect('/rgz/cart')
            
            # Проверяем наличие товаров
            for item in cart_items:
                if item['stock'] < item['quantity']:
                    flash(f'Недостаточно товара "{item["name"]}" на складе', 'error')
                    return redirect('/rgz/cart')
            
            # Считаем общую стоимость
            total = sum(item['price'] * item['quantity'] for item in cart_items)
            
            return render_template('rgz/checkout.html',
                                 cart_items=cart_items,
                                 total=total,
                                 student_info=STUDENT_INFO,
                                 login=session.get('login'))
        except Exception as e:
            flash(f'Ошибка загрузки корзины: {str(e)}', 'error')
            return redirect('/rgz/cart')
        finally:
            db_close(conn, cur)
    
    # POST запрос - оформление заказа
    conn, cur, db_type = db_connect()
    
    try:
        # Получаем ID пользователя
        if db_type == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s", (session['login'],))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?", (session['login'],))
        
        user = cur.fetchone()
        if not user:
            session.pop('login', None)
            flash('Пользователь не найден', 'error')
            return redirect('/rgz/login')
        
        user_id = user['id']
        
        # Получаем товары в корзине
        if db_type == 'postgres':
            cur.execute("""
                SELECT c.*, p.name, p.price, p.stock 
                FROM furniture_cart c 
                JOIN furniture_products p ON c.product_id = p.id 
                WHERE c.user_id = %s
            """, (user_id,))
        else:
            cur.execute("""
                SELECT c.*, p.name, p.price, p.stock 
                FROM furniture_cart c 
                JOIN furniture_products p ON c.product_id = p.id 
                WHERE c.user_id = ?
            """, (user_id,))
        
        cart_items = cur.fetchall()
        
        if not cart_items:
            flash('Корзина пуста', 'error')
            return redirect('/rgz/cart')
        
        # Проверяем наличие товаров
        for item in cart_items:
            if item['stock'] < item['quantity']:
                flash(f'Недостаточно товара "{item["name"]}" на складе', 'error')
                return redirect('/rgz/cart')
        
        # Считаем общую стоимость
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        
        # Создаем заказ
        if db_type == 'postgres':
            cur.execute("""
                INSERT INTO furniture_orders (user_id, total_amount) 
                VALUES (%s, %s) 
                RETURNING id
            """, (user_id, total))
        else:
            cur.execute("""
                INSERT INTO furniture_orders (user_id, total_amount) 
                VALUES (?, ?)
            """, (user_id, total))
            cur.execute("SELECT last_insert_rowid() as id")
        
        order_id = cur.fetchone()['id']
        
        # Добавляем товары в заказ и обновляем остатки
        for item in cart_items:
            if db_type == 'postgres':
                cur.execute("""
                    INSERT INTO furniture_order_items (order_id, product_id, quantity, price) 
                    VALUES (%s, %s, %s, %s)
                """, (order_id, item['product_id'], item['quantity'], item['price']))
                
                cur.execute("""
                    UPDATE furniture_products 
                    SET stock = stock - %s 
                    WHERE id = %s
                """, (item['quantity'], item['product_id']))
            else:
                cur.execute("""
                    INSERT INTO furniture_order_items (order_id, product_id, quantity, price) 
                    VALUES (?, ?, ?, ?)
                """, (order_id, item['product_id'], item['quantity'], item['price']))
                
                cur.execute("""
                    UPDATE furniture_products 
                    SET stock = stock - ? 
                    WHERE id = ?
                """, (item['quantity'], item['product_id']))
        
        # Очищаем корзину
        if db_type == 'postgres':
            cur.execute("DELETE FROM furniture_cart WHERE user_id = %s", (user_id,))
        else:
            cur.execute("DELETE FROM furniture_cart WHERE user_id = ?", (user_id,))
        
        flash('Заказ успешно оформлен!', 'success')
        return redirect('/rgz/orders')
    except Exception as e:
        flash(f'Ошибка оформления заказа: {str(e)}', 'error')
        return redirect('/rgz/checkout')
    finally:
        db_close(conn, cur)

@rgz_bp.route('/orders')
def orders():
    """История заказов"""
    if 'login' not in session:
        flash('Для просмотра заказов необходимо авторизоваться', 'error')
        return redirect('/rgz/login')
    
    conn, cur, db_type = db_connect()
    
    try:
        # Получаем ID пользователя
        if db_type == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s", (session['login'],))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?", (session['login'],))
        
        user_result = cur.fetchone()
        
        if not user_result:
            flash('Пользователь не найден', 'error')
            return redirect('/rgz/login')
        
        # Получаем user_id
        user_id = user_result['id'] if isinstance(user_result, dict) else user_result[0]
        
        # Получаем заказы пользователя
        if db_type == 'postgres':
            cur.execute("SELECT * FROM furniture_orders WHERE user_id = %s ORDER BY created_at DESC", (user_id,))
        else:
            cur.execute("SELECT * FROM furniture_orders WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
        
        orders_raw = cur.fetchall()
        
        orders_with_items = []
        for order_row in orders_raw:
            # Преобразуем в словарь
            if isinstance(order_row, dict):
                order_dict = order_row
            else:
                order_dict = {
                    'id': order_row[0],
                    'user_id': order_row[1],
                    'total_amount': float(order_row[2]),
                    'status': order_row[3],
                    'created_at': order_row[4]
                }
            
            order_id = order_dict['id']
            
            # Получаем товары заказа
            if db_type == 'postgres':
                cur.execute("""
                    SELECT oi.*, p.name, p.image_url 
                    FROM furniture_order_items oi 
                    JOIN furniture_products p ON oi.product_id = p.id 
                    WHERE oi.order_id = %s
                """, (order_id,))
            else:
                cur.execute("""
                    SELECT oi.*, p.name, p.image_url 
                    FROM furniture_order_items oi 
                    JOIN furniture_products p ON oi.product_id = p.id 
                    WHERE oi.order_id = ?
                """, (order_id,))
            
            items_raw = cur.fetchall()
            order_items = []  # Используем другое имя переменной
            
            for item_row in items_raw:
                if isinstance(item_row, dict):
                    item_dict = item_row
                else:
                    item_dict = {
                        'id': item_row[0],
                        'order_id': item_row[1],
                        'product_id': item_row[2],
                        'quantity': item_row[3],
                        'price': float(item_row[4]),
                        'name': item_row[5],
                        'image_url': item_row[6] if len(item_row) > 6 else ''
                    }
                order_items.append(item_dict)
            
            orders_with_items.append({
                'order': order_dict,
                'order_items': order_items 
            })
        
        return render_template('rgz/orders.html',
                             orders=orders_with_items,
                             student_info=STUDENT_INFO,
                             login=session.get('login'))
    except Exception as e:
        flash(f'Ошибка загрузки заказов: {str(e)}', 'error')
        return render_template('rgz/orders.html',
                             orders=[],
                             student_info=STUDENT_INFO,
                             login=session.get('login'))
    finally:
        db_close(conn, cur)

# ========== АВТОРИЗАЦИЯ И РЕГИСТРАЦИЯ ==========

@rgz_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Страница авторизации"""
    if request.method == 'GET':
        if 'login' in session:
            return redirect('/rgz')
        return render_template('rgz/login.html', student_info=STUDENT_INFO)
    
    # POST запрос
    login_input = request.form.get('login')
    password = request.form.get('password')
    
    # Валидация
    valid_login, error_msg = validate_login(login_input)
    if not valid_login:
        return render_template('rgz/login.html', 
                             error=error_msg,
                             student_info=STUDENT_INFO)
    
    valid_pass, error_msg = validate_password(password)
    if not valid_pass:
        return render_template('rgz/login.html', 
                             error=error_msg,
                             student_info=STUDENT_INFO)
    
    conn, cur, db_type = db_connect()
    
    try:
        # Проверяем пользователя
        if db_type == 'postgres':
            cur.execute("SELECT * FROM users WHERE login = %s", (login_input,))
        else:
            cur.execute("SELECT * FROM users WHERE login = ?", (login_input,))
        
        user = cur.fetchone()
        
        if not user:
            return render_template('rgz/login.html', 
                                 error='Пользователь не найден',
                                 student_info=STUDENT_INFO)
        
        if not check_password_hash(user['password'], password):
            return render_template('rgz/login.html', 
                                 error='Неверный пароль',
                                 student_info=STUDENT_INFO)
        
        # Авторизация успешна
        session['login'] = user['login']
        session['user_id'] = user['id']
        
        flash('Вы успешно авторизовались!', 'success')
        return redirect('/rgz')
    except Exception as e:
        return render_template('rgz/login.html', 
                             error=f'Ошибка авторизации: {str(e)}',
                             student_info=STUDENT_INFO)
    finally:
        db_close(conn, cur)

@rgz_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Страница регистрации"""
    if request.method == 'GET':
        if 'login' in session:
            return redirect('/rgz')
        return render_template('rgz/register.html', student_info=STUDENT_INFO)
    
    # POST запрос
    login_input = request.form.get('login')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    full_name = request.form.get('full_name')
    
    # Валидация
    valid_login, error_msg = validate_login(login_input)
    if not valid_login:
        return render_template('rgz/register.html', 
                             error=error_msg,
                             student_info=STUDENT_INFO)
    
    valid_pass, error_msg = validate_password(password)
    if not valid_pass:
        return render_template('rgz/register.html', 
                             error=error_msg,
                             student_info=STUDENT_INFO)
    
    if password != confirm_password:
        return render_template('rgz/register.html', 
                             error='Пароли не совпадают',
                             student_info=STUDENT_INFO)
    
    conn, cur, db_type = db_connect()
    
    try:
        # Проверяем, существует ли пользователь
        if db_type == 'postgres':
            cur.execute("SELECT login FROM users WHERE login = %s", (login_input,))
        else:
            cur.execute("SELECT login FROM users WHERE login = ?", (login_input,))
        
        if cur.fetchone():
            return render_template('rgz/register.html', 
                                 error='Пользователь с таким логином уже существует',
                                 student_info=STUDENT_INFO)
        
        # Создаем пользователя
        password_hash = generate_password_hash(password)
        
        if db_type == 'postgres':
            cur.execute("""
                INSERT INTO users (login, password, full_name) 
                VALUES (%s, %s, %s)
            """, (login_input, password_hash, full_name))
        else:
            cur.execute("""
                INSERT INTO users (login, password, full_name) 
                VALUES (?, ?, ?)
            """, (login_input, password_hash, full_name))
        
        flash('Регистрация успешна! Теперь вы можете авторизоваться.', 'success')
        return redirect('/rgz/login')
    except Exception as e:
        return render_template('rgz/register.html', 
                             error=f'Ошибка регистрации: {str(e)}',
                             student_info=STUDENT_INFO)
    finally:
        db_close(conn, cur)

@rgz_bp.route('/logout')
def logout():
    """Выход из системы"""
    session.pop('login', None)
    session.pop('user_id', None)
    flash('Вы успешно вышли из системы', 'success')
    return redirect('/rgz')

@rgz_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    """Профиль пользователя"""
    if 'login' not in session:
        flash('Для просмотра профиля необходимо авторизоваться', 'error')
        return redirect('/rgz/login')
    
    conn, cur, db_type = db_connect()
    
    try:
        if request.method == 'GET':
            # Получаем данные пользователя
            if db_type == 'postgres':
                cur.execute("SELECT login, full_name FROM users WHERE login = %s", (session['login'],))
            else:
                cur.execute("SELECT login, full_name FROM users WHERE login = ?", (session['login'],))
            
            user = cur.fetchone()
            
            return render_template('rgz/profile.html',
                                 user=user,
                                 student_info=STUDENT_INFO,
                                 login=session.get('login'))
        
        # POST запрос - обновление профиля
        full_name = request.form.get('full_name')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Обновление пароля
        if current_password and new_password:
            if new_password != confirm_password:
                return render_template('rgz/profile.html',
                                     error='Новые пароли не совпадают',
                                     user={'login': session['login'], 'full_name': full_name},
                                     student_info=STUDENT_INFO,
                                     login=session.get('login'))
            
            # Проверяем текущий пароль
            if db_type == 'postgres':
                cur.execute("SELECT password FROM users WHERE login = %s", (session['login'],))
            else:
                cur.execute("SELECT password FROM users WHERE login = ?", (session['login'],))
            
            user_db = cur.fetchone()
            if not check_password_hash(user_db['password'], current_password):
                return render_template('rgz/profile.html',
                                     error='Неверный текущий пароль',
                                     user={'login': session['login'], 'full_name': full_name},
                                     student_info=STUDENT_INFO,
                                     login=session.get('login'))
            
            # Обновляем пароль
            new_password_hash = generate_password_hash(new_password)
            if db_type == 'postgres':
                cur.execute("UPDATE users SET full_name = %s, password = %s WHERE login = %s",
                           (full_name, new_password_hash, session['login']))
            else:
                cur.execute("UPDATE users SET full_name = ?, password = ? WHERE login = ?",
                           (full_name, new_password_hash, session['login']))
        else:
            # Обновляем только имя
            if db_type == 'postgres':
                cur.execute("UPDATE users SET full_name = %s WHERE login = %s",
                           (full_name, session['login']))
            else:
                cur.execute("UPDATE users SET full_name = ? WHERE login = ?",
                           (full_name, session['login']))
        
        flash('Профиль успешно обновлен', 'success')
        return redirect('/rgz/profile')
    except Exception as e:
        flash(f'Ошибка обновления профиля: {str(e)}', 'error')
        return redirect('/rgz/profile')
    finally:
        db_close(conn, cur)

@rgz_bp.route('/profile/delete', methods=['POST'])
def delete_account():
    """Удаление аккаунта"""
    if 'login' not in session:
        flash('Необходимо авторизоваться', 'error')
        return redirect('/rgz/login')
    
    conn, cur, db_type = db_connect()
    
    try:
        # Получаем ID пользователя
        if db_type == 'postgres':
            cur.execute("SELECT id FROM users WHERE login = %s", (session['login'],))
        else:
            cur.execute("SELECT id FROM users WHERE login = ?", (session['login'],))
        
        user = cur.fetchone()
        if not user:
            session.pop('login', None)
            flash('Пользователь не найден', 'error')
            return redirect('/rgz/login')
        
        user_id = user['id']
        
        # Удаляем пользователя (каскадно удалятся его заказы и корзина)
        if db_type == 'postgres':
            cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        else:
            cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
        
        session.pop('login', None)
        session.pop('user_id', None)
        
        flash('Ваш аккаунт успешно удален', 'success')
        return redirect('/rgz')
    except Exception as e:
        flash(f'Ошибка удаления аккаунта: {str(e)}', 'error')
        return redirect('/rgz/profile')
    finally:
        db_close(conn, cur)