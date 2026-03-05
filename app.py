"""
Quantum Mirror Wonderland - Flask Application
Main Entry Point for Backend Server
"""

import os
import sys
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from quantum_mirror_backend import (
    QuantumMirrorBackend,
    UserAvatar,
    CompanionCore,
    AICore,
    GameGeneratorEngine
)

# Initialize Flask App
app = Flask(__name__, 
    static_folder='web',
    static_url_path='',
    template_folder='web')

# Enable CORS
CORS(app, origins=os.getenv('CORS_ORIGINS', '*').split(','))

# Initialize Backend
backend = QuantumMirrorBackend()

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Serve main HTML"""
    return send_from_directory('web', 'index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Quantum Mirror Wonderland",
        "version": "1.0.0"
    }), 200

# ============================================================================
# USER ROUTES
# ============================================================================

@app.route('/api/register', methods=['POST'])
def register():
    """Register new user"""
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        
        if not username or not email:
            return jsonify({"error": "Missing username or email"}), 400
        
        result = backend.register_user(username, email)
        return jsonify(result), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get user information"""
    try:
        if user_id not in backend.users:
            return jsonify({"error": "User not found"}), 404
        
        user = backend.users[user_id]
        return jsonify({
            "id": user_id,
            "username": user["username"],
            "email": user["email"],
            "level": user["avatar"].user_id if user.get("avatar") else 1
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# MIRROR ROUTES
# ============================================================================

@app.route('/api/mirrors', methods=['GET'])
def get_mirrors():
    """Get all mirrors for current user"""
    try:
        user_id = request.args.get('user_id', 1, type=int)
        user_mirrors = [m for m in backend.mirrors.values() if m.get('user_id') == user_id]
        return jsonify({"mirrors": user_mirrors}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/mirror/create', methods=['POST'])
def create_mirror():
    """Create new mirror"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 1)
        idea = data.get('idea', 'Mystery Game')
        
        result = backend.create_mirror(user_id, idea)
        return jsonify(result), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/mirror/<mirror_id>/break', methods=['POST'])
def break_mirror(mirror_id):
    """Break mirror and generate new design"""
    try:
        result = backend.break_mirror(mirror_id)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# CHAT ROUTES
# ============================================================================

@app.route('/api/chat/send', methods=['POST'])
def send_chat_message():
    """Send chat message and get companion response"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 1)
        room = data.get('room', 'Wunderland')
        message = data.get('message')
        
        if not message:
            return jsonify({"error": "No message provided"}), 400
        
        result = backend.send_chat_message(user_id, room, message)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/messages/<room>', methods=['GET'])
def get_chat_messages(room):
    """Get chat messages from room"""
    try:
        if room not in backend.chat_rooms:
            return jsonify({"messages": []}), 200
        
        messages = backend.chat_rooms[room]
        return jsonify({"messages": messages}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# GAME ROUTES
# ============================================================================

@app.route('/api/game/create', methods=['POST'])
def create_game():
    """Create new game"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 1)
        idea = data.get('idea', 'Mystery Game')
        
        game = backend.game_generator.create_game(user_id, idea)
        return jsonify(game), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/games/<int:user_id>', methods=['GET'])
def get_user_games(user_id):
    """Get games created by user"""
    try:
        user_games = [g for g in backend.games.values() if g.get('user_id') == user_id]
        return jsonify({"games": user_games}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# COMPANION ROUTES
# ============================================================================

@app.route('/api/companion/speak', methods=['POST'])
def companion_speak():
    """Get companion response"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        user_id = data.get('user_id', 1)
        
        # Get user avatar name
        user = backend.users.get(user_id, {})
        avatar_name = user.get("avatar").name if user.get("avatar") else "Wanderer"
        
        response = backend.companion.respond(message, avatar_name)
        return jsonify({"response": response}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# AVATAR ROUTES
# ============================================================================

@app.route('/api/avatar/<int:user_id>', methods=['GET'])
def get_avatar(user_id):
    """Get user avatar"""
    try:
        result = backend.get_user_avatar(user_id)
        if not result:
            return jsonify({"error": "Avatar not found"}), 404
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ============================================================================
# STATIC FILES
# ============================================================================

@app.route('/web/<path:path>')
def send_web(path):
    """Serve web files"""
    return send_from_directory('web', path)

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
    
    print(f"🌀 Quantum Mirror Wonderland v1.0")
    print(f"🚀 Starting on http://localhost:{port}")
    print(f"🐱 Master-Kater is ready!")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )

