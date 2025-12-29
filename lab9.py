from flask import Blueprint, render_template, session, jsonify, request
import random
from flask_login import login_required, current_user

lab9 = Blueprint('lab9', __name__)

# Новогодние поздравления
greetings = [
    "🎄 С Новым Годом! Пусть наступающий год принесет много радости, счастья и успехов во всех начинаниях!",
    "❄️ Желаю, чтобы новый год стал годом исполнения самых заветных желаний и смелых мечтаний!",
    "🌟 Пусть в новом году вас окружают только добрые и искренние люди, а каждый день будет наполнен теплом и уютом!",
    "✨ Желаю крепкого здоровья, неиссякаемой энергии и бодрости духа на весь год вперед!",
    "🎁 Пусть новый год принесет финансовое благополучие, стабильность и уверенность в завтрашнем дне!",
    "🦌 Желаю ярких впечатлений, незабываемых путешествий и новых интересных знакомств!",
    "🔔 Пусть в вашем доме всегда царят гармония, любовь и взаимопонимание!",
    "⭐ Желаю творческого вдохновения, смелых идей и успешной их реализации!",
    "☃️ Пусть работа приносит не только доход, но и удовольствие, а карьера стремительно идет вверх!",
    "🎅 Желаю, чтобы новый год стал самым счастливым и запоминающимся в вашей жизни!"
]

# Подарки (некоторые только для авторизованных)
gifts = [
    "gift1.png",  # 0 - для всех
    "gift2.png",  # 1 - для всех
    "gift3.png",  # 2 - для всех
    "gift4.png",  # 3 - для всех
    "gift5.png",  # 4 - для авторизованных
    "gift6.png",  # 5 - для авторизованных
    "gift7.png",  # 6 - для авторизованных
    "gift8.png",  # 7 - для авторизованных
    "gift9.png",  # 8 - для авторизованных
    "gift10.png"  # 9 - специальный подарок от Деда Мороза
]

# Коробки
boxes = [
    "box1.png", "box2.png", "box3.png", "box4.png", "box5.png",
    "box6.png", "box7.png", "box8.png", "box9.png", "box10.png"
]

# Какие коробки требуют авторизации (индексы 4-9)
REQUIRES_LOGIN = [4, 5, 6, 7, 8, 9]

def init_session():
    """Инициализация сессии"""
    if 'uid' not in session:
        session['uid'] = str(random.randint(10000, 99999))
    
    if 'open' not in session:
        session['open'] = []
    
    if 'states' not in session:
        session['states'] = [False] * 10
    
    if 'pos' not in session:
        generate_positions()
    
    # Инициализация специальных подарков Деда Мороза
    if 'santa_gifts' not in session:
        session['santa_gifts'] = 0

def generate_positions():
    """Генерация позиций для коробок"""
    pos = []
    used = []
    
    for i in range(10):
        attempts = 0
        placed = False
        
        while attempts < 100 and not placed:
            top = random.randint(5, 85)
            left = random.randint(5, 90)
            
            conflict = False
            for spot in used:
                if abs(top - spot['top']) < 15 and abs(left - spot['left']) < 15:
                    conflict = True
                    break
            
            if not conflict:
                used.append({'top': top, 'left': left})
                pos.append({
                    'id': i,
                    'top': f"{top}%",
                    'left': f"{left}%",
                    'requires_login': i in REQUIRES_LOGIN
                })
                placed = True
            attempts += 1
        
        if not placed:
            top = random.randint(5, 85)
            left = random.randint(5, 90)
            pos.append({
                'id': i,
                'top': f"{top}%",
                'left': f"{left}%",
                'requires_login': i in REQUIRES_LOGIN
            })
    
    session['pos'] = pos

@lab9.route('/lab9/')
def main():
    """Главная страница"""
    init_session()
    
    states = session.get('states', [False] * 10)
    open_count = len(session.get('open', []))
    left_count = 10 - sum(states)
    
    # Проверяем, авторизован ли пользователь
    is_authenticated = hasattr(current_user, 'is_authenticated') and current_user.is_authenticated
    
    return render_template('lab9/index.html',
                         pos=session['pos'],
                         states=states,
                         boxes=boxes,
                         open_count=open_count,
                         left_count=left_count,
                         is_authenticated=is_authenticated,
                         requires_login=REQUIRES_LOGIN,
                         santa_gifts=session.get('santa_gifts', 0))

@lab9.route('/lab9/open', methods=['POST'])
def open_box():
    """Открытие коробки"""
    init_session()
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'ok': False, 'msg': 'Нет данных'}), 400
            
        box_id = data.get('box_id')
        
        if box_id is None:
            return jsonify({'ok': False, 'msg': 'Нет ID подарка'}), 400
            
        box_id = int(box_id)
        
        if box_id < 0 or box_id >= 10:
            return jsonify({'ok': False, 'msg': 'Некорректный номер подарка'}), 400
        
        states = session.get('states', [False] * 10)
        open_list = session.get('open', [])
        
        # Проверка лимита
        if len(open_list) >= 3:
            return jsonify({'ok': False, 'msg': 'Можно открыть только 3 подарка!'}), 400
        
        # Проверка, не открыта ли уже
        if states[box_id]:
            return jsonify({'ok': False, 'msg': 'Этот подарок уже открыт!'}), 400
        
        # Проверка авторизации для специальных подарков
        if box_id in REQUIRES_LOGIN:
            is_authenticated = hasattr(current_user, 'is_authenticated') and current_user.is_authenticated
            if not is_authenticated:
                return jsonify({
                    'ok': False, 
                    'msg': 'Этот подарок доступен только авторизованным пользователям! Войдите в систему.'
                }), 403
        
        # Открываем коробку
        open_list.append(box_id)
        session['open'] = open_list
        states[box_id] = True
        session['states'] = states
        
        greeting = greetings[box_id]
        gift = gifts[box_id]
        left_count = 10 - sum(states)
        
        return jsonify({
            'ok': True,
            'greeting': greeting,
            'gift': gift,
            'open_count': len(open_list),
            'left_count': left_count,
            'requires_login': box_id in REQUIRES_LOGIN
        })
        
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Ошибка сервера: {str(e)}'}), 500

@lab9.route('/lab9/santa', methods=['POST'])  # Изменил на 'santa' вместо 'santa_gift'
@login_required
def santa():
    """Функция Деда Мороза - наполняет все коробки заново"""
    if not hasattr(current_user, 'is_authenticated') or not current_user.is_authenticated:
        return jsonify({'ok': False, 'msg': 'Требуется авторизация!'}), 401
    
    init_session()
    
    # Сбрасываем открытые коробки
    session['states'] = [False] * 10
    session['open'] = []
    
    # Генерируем новые позиции
    generate_positions()
    
    # Увеличиваем счетчик подарков Деда Мороза
    session['santa_gifts'] = session.get('santa_gifts', 0) + 1
    
    return jsonify({
        'ok': True,
        'msg': '🎅 Дед Мороз наполнил все коробки заново! 🎁',
        'santa_gifts': session['santa_gifts']
    })

@lab9.route('/lab9/status')
def status():
    """Получение статуса игры"""
    init_session()
    
    states = session.get('states', [False] * 10)
    open_count = len(session.get('open', []))
    left_count = 10 - sum(states)
    is_authenticated = hasattr(current_user, 'is_authenticated') and current_user.is_authenticated
    
    return jsonify({
        'open_count': open_count,
        'left_count': left_count,
        'is_authenticated': is_authenticated,
        'santa_gifts': session.get('santa_gifts', 0)
    })

@lab9.route('/lab9/reset', methods=['POST'])
def reset():
    """Сброс игры для всех пользователей"""
    session.pop('open', None)
    session.pop('states', None)
    session.pop('pos', None)
    session.pop('santa_gifts', None)
    
    return jsonify({
        'ok': True,
        'msg': 'Игра сброшена'
    })