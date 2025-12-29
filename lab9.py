from flask import Blueprint, render_template, session, jsonify, request
import random

lab9 = Blueprint('lab9', __name__)

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

gifts = [
    "gift1.png", "gift2.png", "gift3.png", "gift4.png", "gift5.png",
    "gift6.png", "gift7.png", "gift8.png", "gift9.png", "gift10.png"
]

boxes = [
    "box1.png", "box2.png", "box3.png", "box4.png", "box5.png",
    "box6.png", "box7.png", "box8.png", "box9.png", "box10.png"
]

def init_session():
    if 'uid' not in session:
        session['uid'] = str(random.randint(10000, 99999))
    
    if 'open' not in session:
        session['open'] = []
    
    if 'states' not in session:
        session['states'] = [False] * 10
    
    if 'pos' not in session:
        generate_positions()

def generate_positions():
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
                    'left': f"{left}%"
                })
                placed = True
            attempts += 1
        
        if not placed:
            top = random.randint(5, 85)
            left = random.randint(5, 90)
            pos.append({
                'id': i,
                'top': f"{top}%",
                'left': f"{left}%"
            })
    
    session['pos'] = pos

@lab9.route('/lab9/')
def main():
    init_session()
    
    states = session.get('states', [False] * 10)
    open_count = len(session.get('open', []))
    left_count = 10 - sum(states)
    
    return render_template('lab9/index.html',
                         pos=session['pos'],
                         states=states,
                         boxes=boxes,
                         open_count=open_count,
                         left_count=left_count)

@lab9.route('/lab9/open', methods=['POST'])
def open_box():
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
        
        if len(open_list) >= 3:
            return jsonify({'ok': False, 'msg': 'Можно открыть только 3 подарка!'}), 400
        
        if states[box_id]:
            return jsonify({'ok': False, 'msg': 'Этот подарок уже открыт!'}), 400
        
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
            'left_count': left_count
        })
        
    except Exception as e:
        return jsonify({'ok': False, 'msg': f'Ошибка сервера: {str(e)}'}), 500

@lab9.route('/lab9/status')
def status():
    init_session()
    
    states = session.get('states', [False] * 10)
    open_count = len(session.get('open', []))
    left_count = 10 - sum(states)
    
    return jsonify({
        'open_count': open_count,
        'left_count': left_count
    })

@lab9.route('/lab9/reset', methods=['POST'])
def reset():
    session.pop('open', None)
    session.pop('states', None)
    session.pop('pos', None)
    
    return jsonify({
        'ok': True,
        'msg': 'Игра сброшена'
    })