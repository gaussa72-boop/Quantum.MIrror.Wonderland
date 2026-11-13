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

# SECURITY HARDENING
_SEC_RATE_LIMIT={}
from time import monotonic
@app.before_request
def _sec_before():
    if request.content_length and request.content_length>1048576:return jsonify(error="Request too large."),413
    if request.path.startswith("/.git/") or request.path.startswith("/.env"):return jsonify(error="Not Found."),404
    ip=request.remote_addr or "unknown";now=monotonic();b=_SEC_RATE_LIMIT.setdefault(ip,[]);b[:]=[t for t in b if now-t<60];limit=30 if request.method in {"POST","PUT","PATCH","DELETE"} else 120
    if len(b)>=limit:return jsonify(error="Too many requests. Please try again later."),429
    b.append(now)
@app.after_request
def _sec_headers(response):
    response.headers.setdefault("X-Content-Type-Options","nosniff");response.headers.setdefault("X-Frame-Options","DENY");response.headers.setdefault("Referrer-Policy","strict-origin-when-cross-origin");response.headers.setdefault("Permissions-Policy","camera=(), microphone=(), geolocation=()");response.headers.setdefault("Cross-Origin-Opener-Policy","same-origin");response.headers.setdefault("Strict-Transport-Security","max-age=31536000; includeSubDomains");response.headers.pop("Server",None);return response


# --- Security hardening ---
from collections import defaultdict, deque
from time import monotonic
from html import escape as html_escape

_SECURITY_RATE = defaultdict(deque)
_SECURITY_WINDOW = 60
_SECURITY_MAX = 120
_SECURITY_POST_MAX = 30
_SECURITY_MAX_BODY = 1024 * 1024

@app.before_request
def _security_before_request():
    if request.content_length and request.content_length > _SECURITY_MAX_BODY:
        return jsonify(error="Request too large."), 413
    path = request.path or "/"
    blocked = {"/.env","/.git/config","/server.py","/app.py","/main.py","/package.json","/requirements.txt","/render.yaml","/Procfile"}
    if path in blocked or path.startswith("/.git/") or path.startswith("/.env"):
        return jsonify(error="Not Found."), 404
    ip = request.remote_addr or "unknown"
    now = monotonic()
    q = _SECURITY_RATE[ip]
    while q and now - q[0] > _SECURITY_WINDOW:
        q.popleft()
    limit = _SECURITY_POST_MAX if request.method in {"POST","PUT","PATCH","DELETE"} else _SECURITY_MAX
    if len(q) >= limit:
        return jsonify(error="Too many requests. Please try again later."), 429
    q.append(now)

@app.after_request
def _security_headers(response):
    response.headers.setdefault("X-Content-Type-Options","nosniff")
    response.headers.setdefault("X-Frame-Options","DENY")
    response.headers.setdefault("Referrer-Policy","strict-origin-when-cross-origin")
    response.headers.setdefault("Permissions-Policy","camera=(), microphone=(), geolocation=()")
    response.headers.setdefault("Cross-Origin-Opener-Policy","same-origin")
    response.headers.setdefault("Strict-Transport-Security","max-age=31536000; includeSubDomains")
    response.headers.setdefault("Cache-Control","no-store" if request.path.startswith("/api/") else "public, max-age=300")
    response.headers.pop("Server", None)
    return response
# --- End security hardening ---
CORS(app, origins=[x.strip() for x in os.getenv("CORS_ORIGINS", "").split(",") if x.strip()] or [])
backend = QuantumMirrorBackend()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health():
    return jsonify({'status':'healthy','service':'Quantum Mirror Wonderland','version':'2.0.0','game_studio':True,'ai_enabled':os.getenv('AI_ENABLED','true').lower()=='true','ai_configured':bool(os.getenv('OPENAI_API_KEY','').strip() or os.getenv('OPENROUTER_API_KEY','').strip()),'provider':os.getenv('AI_PROVIDER','openai'),'model':os.getenv('OPENAI_MODEL','gpt-4o-mini')}), 200

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

@app.route('/chat')
def chat_page():
    return send_from_directory('.', 'chat.html')

@app.route('/engine')
def engine_alias():
    return redirect('/studio')

@app.route('/api/chat/ai', methods=['POST'])
def ai_chat():
    data=request.get_json(silent=True) or {}
    message=str(data.get('message') or '').strip()
    if not message:return jsonify({'error':'message is required'}),400
    if len(message)>12000:return jsonify({'error':'Nachricht ist zu lang (max. 12.000 Zeichen).'}),413
    if os.getenv('AI_ENABLED','true').strip().lower()!='true':
        return jsonify({'error':'KI ist mit AI_ENABLED=false deaktiviert.'}),503
    openai_key=os.getenv('OPENAI_API_KEY','').strip()
    router_key=os.getenv('OPENROUTER_API_KEY','').strip()
    provider=os.getenv('AI_PROVIDER','openai').strip().lower()
    if not (openai_key or router_key) or OpenAI is None:
        return jsonify({'error':'OPENAI_API_KEY oder OPENROUTER_API_KEY fehlt in Render.'}),503
    use_router=(provider=='openrouter' and bool(router_key)) or (not openai_key and bool(router_key))
    model=(os.getenv('OPENROUTER_MODEL','openai/gpt-4o-mini').strip() if use_router else os.getenv('OPENAI_MODEL','gpt-4o-mini').strip())
    try:
        system='Du bist Quantum Mirror Wonderland. Arbeite wie ein moderner KI-Architekt für Game Design, Worldbuilding, Code und Recherche. Liefere konkrete, sichere und überprüfbare Ergebnisse.'
        if use_router:
            active=OpenAI(api_key=router_key,base_url='https://openrouter.ai/api/v1')
            response=active.chat.completions.create(model=model,messages=[{'role':'system','content':system},{'role':'user','content':message}])
            answer=response.choices[0].message.content or 'Keine Antwort.'
        else:
            active=OpenAI(api_key=openai_key)
            options={'model':model,'instructions':system,'input':message,'store':False}
            if os.getenv('ENABLE_WEB_SEARCH','true').lower()=='true':
                options['tools']=[{'type':'web_search','search_context_size':'medium'}]
                options['tool_choice']='auto'
            response=active.responses.create(**options)
            answer=response.output_text or 'Keine Antwort.'
        return jsonify({'response':answer,'model':model,'provider':'openrouter' if use_router else 'openai'}),200
    except Exception:
        app.logger.exception('Quantum Mirror AI request failed (%s / %s)',provider,model)
        return jsonify({'error':'KI-Schnittstelle fehlgeschlagen. Prüfe API-Key, Modellfreigabe und Guthaben.'}),502

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
from ki_game_mod_api import register_ki_game_mod_routes
register_ki_game_mod_routes(app)


@app.route('/dark-mirror-game')
def dark_mirror_game_index_redirect():
    return redirect('/dark-mirror-game/')

@app.route('/dark-mirror-game/')
def dark_mirror_game_index():
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'dark_mirror_game'), 'index.html')

@app.route('/dark-mirror-game/<path:filename>')
def dark_mirror_game_assets(filename):
    return send_from_directory(os.path.join(os.path.dirname(__file__), 'dark_mirror_game'), filename)

@app.errorhandler(404)
def not_found(error): return jsonify({'error':'Not found'}),404
@app.errorhandler(500)
def server_error(error): return jsonify({'error':'Internal server error'}),500

if __name__=='__main__':
    port=int(os.getenv('PORT',5000)); debug=os.getenv('FLASK_DEBUG','False')=='True'
    print(f'🌀 Quantum Mirror Wonderland v2.0 — Game Studio on http://localhost:{port}/studio')
    app.run(host='0.0.0.0',port=port,debug=debug)
