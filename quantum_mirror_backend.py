"""Dunkle Spiegel backend: legacy Wonderland APIs bridged to the Game Engine."""
from datetime import datetime
from typing import Dict, Optional

from quantum_game_engine.generation_v2 import GenerationOrchestrator
from game_engine import QuantumGameEngine


class QuantumMirrorBackend:
    """Compatibility backend for mirrors, chat, avatars and generated projects."""
    def __init__(self):
        self.users, self.mirrors, self.chat_rooms, self.games = {}, {}, {}, {}
        self.training_data = []
        self.companion = CompanionCore()
        self.ai_core = AICore()
        self.game_generator = GameGeneratorEngine(self)
        self.engine = QuantumGameEngine()
        self.orchestrator = GenerationOrchestrator()

    def register_user(self, username: str, email: str) -> Dict:
        user_id = max(self.users.keys(), default=0) + 1
        avatar = UserAvatar(user_id, username)
        self.users[user_id] = {'username': username, 'email': email, 'avatar': avatar,
                               'created_at': datetime.now().isoformat(), 'mirrors': [], 'games_created': 0}
        return {'user_id': user_id, 'username': username, 'avatar': avatar.name, 'status': 'created'}

    def create_mirror(self, user_id: int, mirror_idea: str) -> Dict:
        if user_id not in self.users:
            raise ValueError('User not found')
        game = self.game_generator.create_game(user_id, mirror_idea)
        mirror_id = f'mirror_{user_id}_{len(self.mirrors)+1}'
        mirror = {'mirror_id': mirror_id, 'user_id': user_id, 'idea': mirror_idea,
                  'game_id': game['game_id'], 'status': 'active', 'created_at': datetime.now().isoformat(),
                  'design': self._generate_paradiesical_design()}
        self.mirrors[mirror_id] = mirror
        self.users[user_id]['mirrors'].append(mirror_id)
        return mirror

    def create_generated_project(self, user_id: int, prompt: str, target='web', kind='game') -> Dict:
        if user_id not in self.users:
            raise ValueError('User not found')
        result = self.engine.generate(prompt, target, kind)
        result['blueprint'] = self.orchestrator.build_blueprint(prompt, target, kind)
        self.users[user_id]['games_created'] += 1
        self.games[result['id']] = {'user_id': user_id, **result}
        return result

    def send_chat_message(self, user_id: int, room_name: str, message: str) -> Dict:
        if user_id not in self.users:
            raise ValueError('User not found')
        room = self.chat_rooms.setdefault(room_name, [])
        room.append({'user_id': user_id, 'message': message, 'timestamp': datetime.now().isoformat()})
        response = self.companion.respond(message, self.users[user_id]['avatar'].name)
        room.append({'user_id': 'master_cat', 'message': response, 'timestamp': datetime.now().isoformat()})
        self.training_data.append({'user_id': user_id, 'input': message, 'response': response, 'timestamp': datetime.now().isoformat()})
        return {'room': room_name, 'user_message': message, 'companion_response': response}

    def get_user_avatar(self, user_id: int) -> Optional[Dict]:
        if user_id not in self.users: return None
        avatar = self.users[user_id]['avatar']
        interactions = sum(1 for x in self.training_data if x['user_id'] == user_id)
        return {'user_id': user_id, 'avatar_name': avatar.name, 'avatar_personality': avatar.personality,
                'avatar_memory': avatar.memory, 'interaction_count': interactions,
                'level': min(10, max(1, interactions // 50 + 1))}

    def break_mirror(self, mirror_id: str) -> Dict:
        if mirror_id not in self.mirrors: return {'error': 'Mirror not found'}
        mirror = self.mirrors[mirror_id]
        mirror['design'] = self._generate_paradiesical_design()
        mirror['last_broken'] = datetime.now().isoformat()
        return {'mirror_id': mirror_id, 'new_design': mirror['design'], 'status': 'regenerated'}

    @staticmethod
    def _generate_paradiesical_design() -> Dict:
        import random
        return {'primary_color': random.choice(['#FF1493','#00CED1','#FFD700','#9370DB']),
                'geometry': random.choice(['spiral','mandala','fractal','quantum_tunnel']),
                'light_effect': random.choice(['supernova','quantum_glow','dreamlight','paradox']),
                'sound_theme': random.choice(['ethereal','chaotic','mystical','psychedelic']),
                'particle_count': random.randint(100,500), 'animation_speed': round(random.uniform(.5,2),2)}


class UserAvatar:
    def __init__(self, user_id: int, name: str):
        self.user_id, self.name = user_id, name
        self.personality, self.memory, self.learning_style = 'curious', {}, 'adaptive'

    def process_input(self, user_input: str) -> str:
        self.memory[f'interaction_{len(self.memory)}'] = user_input
        return f"{self.name} verarbeitet: '{user_input}'"


class CompanionCore:
    def respond(self, message: str, user_avatar_name: str) -> str:
        return f'Master-Kater: {message} — wir können daraus ein neues Spiegelwelt-System bauen, {user_avatar_name}.'


class AICore:
    def process(self, prompt: str, user_id: int) -> str:
        return f"AI_Core verarbeitet für User {user_id}: '{prompt}'"


class GameGeneratorEngine:
    """Legacy facade. New generation requests use QuantumGameEngine."""
    def __init__(self, backend): self.backend = backend; self.games = {}

    def create_game(self, user_id: int, idea: str) -> Dict:
        game_id = f'game_{user_id}_{len(self.games)+1}'
        result = {'game_id': game_id, 'user_id': user_id, 'idea': idea,
                  'type': self._determine_game_type(idea), 'status': 'created'}
        self.games[game_id] = result
        return result

    @staticmethod
    def _determine_game_type(idea: str) -> str:
        text = idea.lower()
        if any(x in text for x in ('jump','platform')): return 'platformer'
        if 'puzzle' in text: return 'puzzle'
        if any(x in text for x in ('adventure','rpg')): return 'adventure'
        return 'interactive_experience'


backend = QuantumMirrorBackend()
