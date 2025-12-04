from flask import Blueprint, render_template, request, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path
from datetime import datetime

lab6 = Blueprint('lab6', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='localhost',
            database='atamankina_knowledge_base',
            user='tmnknkt',
            password='111'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def init_offices_table():
    """Инициализация таблицы offices начальными данными"""
    conn, cur = db_connect()
    
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT COUNT(*) as count FROM offices;")
        else:
            cur.execute("SELECT COUNT(*) as count FROM offices;")
        
        result = cur.fetchone()
        count = result['count'] if 'count' in result else result[0]
        
        if count == 0:
            offices_data = []
            for i in range(1, 11):
                offices_data.append({
                    "number": i,
                    "price": 900 + i % 3 * 100
                })
            
            for office in offices_data:
                if current_app.config['DB_TYPE'] == 'postgres':
                    cur.execute(
                        "INSERT INTO offices (number, price) VALUES (%s, %s) ON CONFLICT (number) DO NOTHING;",
                        (office['number'], office['price'])
                    )
                else:
                    cur.execute(
                        "INSERT OR IGNORE INTO offices (number, price) VALUES (?, ?);",
                        (office['number'], office['price'])
                    )
            
            print("Таблица offices инициализирована начальными данными")
    except Exception as e:
        print(f"Ошибка при инициализации таблицы offices: {e}")
    finally:
        db_close(conn, cur)

@lab6.route('/lab6/')
def main():
    init_offices_table()
    
    login = session.get('login')
    return render_template('lab6/lab6.html', login=login)

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    if data['method'] == 'info':
        conn, cur = db_connect()
        
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
            else:
                cur.execute("SELECT number, tenant, price FROM offices ORDER BY number;")
            
            offices = cur.fetchall()
            
            office_list = []
            for office in offices:
                if isinstance(office, dict):
                    office_list.append({
                        "number": office['number'],
                        "tenant": office['tenant'] if office['tenant'] else "",
                        "price": office['price']
                    })
                else: 
                    office_list.append({
                        "number": office[0],
                        "tenant": office[1] if office[1] else "",
                        "price": office[2]
                    })
            
            return {
                'jsonrpc': '2.0',
                'result': office_list,
                'id': id
            }
        except Exception as e:
            print(f"Ошибка при получении списка офисов: {e}")
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 500,
                    'message': 'Internal server error'
                },
                'id': id
            }
        finally:
            db_close(conn, cur)
    
    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        
        if isinstance(office_number, str):
            try:
                office_number = int(office_number)
            except ValueError:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 3,
                        'message': 'Invalid office number'
                    },
                    'id': id
                }
        
        conn, cur = db_connect()
        
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT tenant FROM offices WHERE number = %s;", (office_number,))
            else:
                cur.execute("SELECT tenant FROM offices WHERE number = ?;", (office_number,))
            
            office = cur.fetchone()
            
            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 6,
                        'message': 'Office not found'
                    },
                    'id': id
                }
            
            tenant = office['tenant'] if isinstance(office, dict) else office[0]
            if tenant:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 2,
                        'message': 'Already booked'
                    },
                    'id': id
                }
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute(
                    "UPDATE offices SET tenant = %s WHERE number = %s;",
                    (login, office_number)
                )
            else:
                cur.execute(
                    "UPDATE offices SET tenant = ? WHERE number = ?;",
                    (login, office_number)
                )
            
            return {
                'jsonrpc': '2.0',
                'result': "success",  
                'id': id
            }
        except Exception as e:
            print(f"Ошибка при бронировании офиса: {e}")
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 500,
                    'message': 'Internal server error'
                },
                'id': id
            }
        finally:
            db_close(conn, cur)
    
    if data['method'] == 'cancellation':
        office_number = data['params']
        
        if isinstance(office_number, str):
            try:
                office_number = int(office_number)
            except ValueError:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 3,
                        'message': 'Invalid office number'
                    },
                    'id': id
                }
        
        conn, cur = db_connect()
        
        try:
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT tenant FROM offices WHERE number = %s;", (office_number,))
            else:
                cur.execute("SELECT tenant FROM offices WHERE number = ?;", (office_number,))
            
            office = cur.fetchone()
            
            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 6,
                        'message': 'Office not found'
                    },
                    'id': id
                }
            
            tenant = office['tenant'] if isinstance(office, dict) else office[0]
            
            if not tenant:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 4,
                        'message': 'Office is not booked'
                    },
                    'id': id
                }
            
            if tenant != login:
                return {
                    'jsonrpc': '2.0',
                    'error': {
                        'code': 5,
                        'message': 'Cannot cancel someone else\'s booking'
                    },
                    'id': id
                }
            
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute(
                    "UPDATE offices SET tenant = NULL WHERE number = %s;",
                    (office_number,)
                )
            else:
                cur.execute(
                    "UPDATE offices SET tenant = NULL WHERE number = ?;",
                    (office_number,)
                )
            
            return {
                'jsonrpc': '2.0',
                'result': "cancellation_success",  
                'id': id
            }
        except Exception as e:
            print(f"Ошибка при отмене бронирования: {e}")
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 500,
                    'message': 'Internal server error'
                },
                'id': id
            }
        finally:
            db_close(conn, cur)

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }