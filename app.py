"""Quantum Mirror Wonderland + Quantum Game Studio entry point."""
import os
import sys
from flask import Flask, jsonify, request, send_from_directory, redirect
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
from quantum_mirror_backend import QuantumMirrorBackend
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app, origins=os.getenv('CORS_ORIGINS', '*').split(','))
backend = QuantumMirrorBackend()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health():
    return jsonify({'status':'healthy','service':'Quantum Mirror Wonderland','version':'2.0.0','game_studio':True}), 200

@app.route('/api/register', methods=['POST'])
def register():
    data=request.get_json(silent=True) or {}; username=data.get('username'); email=data.get('email')
    if not username or not email: return jsonify({'error':'Missing username or email'}),400
    try: return jsonify(backend.register_user(username,email)),201
    except Exception as exc: return jsonify({'error':str(exc)}),500

@app.route('/api/user/<int:user_id>')
def get_user(user_id):
    user=backend.users.get(user_id)
    if not user: return jsonify({'error':'User not found'}),404
    return jsonify({'id':user_id,'username':user['username'],'email':user['email']}),200

@app.route('/api/mirrors')
def get_mirrors():
    user_id=request.args.get('user_id',1,type=int)
    return jsonify({'mirrors':[m for m in backend.mirrors.values() if m.get('user_id')==user_id]}),200

@app.route('/api/mirror/create',methods=['POST'])
def create_mirror():
    data=request.get_json(silent=True) or {}; return jsonify(backend.create_mirror(data.get('user_id',1),data.get('idea','Mystery Game'))),201

@app.route('/api/mirror/<mirror_id>/break',methods=['POST'])
def break_mirror(mirror_id):
    return jsonify(backend.break_mirror(mirror_id)),200

@app.route('/engine')
def engine_alias():
    return redirect('/studio')

@app.route('/api/chat/ai', methods=['POST'])
def ai_chat():
    data=request.get_json(silent=True) or {}
    message=str(data.get('message') or '').strip()
    if not message: return jsonify({'error':'message is required'}),400
    key=os.getenv('OPENAI_API_KEY')
    if not key or OpenAI is None:
        return jsonify({'error':'OPENAI_API_KEY is not configured'}),503
    try:
        tools=[{'type':'web_search','search_context_size':'medium'}] if os.getenv('ENABLE_WEB_SEARCH','true').lower()=='true' else []
        response=OpenAI(api_key=key).responses.create(
            model=os.getenv('OPENAI_MODEL','gpt-6-astra'),
            reasoning={'effort':'high'},
            tools=tools,
            tool_choice='auto',
            store=False,
            input=[
                {'role':'system','content':'Du bist Quantum Mirror Wonderland. Arbeite wie ein moderner KI-Architekt für Game Design, Worldbuilding, Code und Recherche. Liefere konkrete, sichere und überprüfbare Ergebnisse.'},
                {'role':'user','content':message}
            ]
        )
        return jsonify({'response':response.output_text or 'Keine Antwort.','model':os.getenv('OPENAI_MODEL','gpt-6-astra')})
    except Exception:
        app.logger.exception('Astra chat failure')
        return jsonify({'error':'KI-Schnittstelle momentan nicht erreichbar.'}),502

@app.route('/api/chat/send',methods=['POST'])
def send_chat_message():
    data=request.get_json(silent=True) or {}; message=data.get('message')
    if not message: return jsonify({'error':'No message provided'}),400
    return jsonify(backend.send_chat_message(data.get('user_id',1),data.get('room','Wunderland'),message)),200

@app.route('/api/chat/messages/<room>')
def get_chat_messages(room):
    return jsonify({'messages':backend.chat_rooms.get(room,[])}),200

@app.route('/api/game/create',methods=['POST'])
def create_game():
    data=request.get_json(silent=True) or {}; return jsonify(backend.game_generator.create_game(data.get('user_id',1),data.get('idea','Mystery Game'))),201

@app.route('/api/games/<int:user_id>')
def get_user_games(user_id):
    return jsonify({'games':[g for g in backend.games.values() if g.get('user_id')==user_id]}),200

@app.route('/api/companion/speak',methods=['POST'])
def companion_speak():
    data=request.get_json(silent=True) or {}; user=backend.users.get(data.get('user_id',1),{}); avatar=user.get('avatar'); name=avatar.name if avatar else 'Wanderer'
    return jsonify({'response':backend.companion.respond(data.get('message',''),name)}),200

@app.route('/api/avatar/<int:user_id>')
def get_avatar(user_id):
    result=backend.get_user_avatar(user_id)
    return (jsonify(result),200) if result else (jsonify({'error':'Avatar not found'}),404)

@app.route('/web/<path:path>')
def send_web(path): return send_from_directory('.', path)

from studio_api import register_studio_routes
register_studio_routes(app)

@app.errorhandler(404)
def not_found(error): return jsonify({'error':'Not found'}),404
@app.errorhandler(500)
def server_error(error): return jsonify({'error':'Internal server error'}),500

if __name__=='__main__':
    port=int(os.getenv('PORT',5000)); debug=os.getenv('FLASK_DEBUG','False')=='True'
    print(f'🌀 Quantum Mirror Wonderland v2.0 — Game Studio on http://localhost:{port}/studio')
    app.run(host='0.0.0.0',port=port,debug=debug)
