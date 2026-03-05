"""
Quantum Mirror Wonderland - Backend Integration
Integriert alle vorherigen Codes + neue Chat & User Avatar Module
"""

import json
from datetime import datetime
from typing import Dict, List, Optional

class QuantumMirrorBackend:
    """
    Master-Backend für Quantum Mirror Wonderland
    Integriert: AI Core, Companion Core, Game Generator, Chat, Training, User Avatars
    """
    
    def __init__(self):
        self.users = {}
        self.mirrors = {}
        self.chat_rooms = {}
        self.games = {}
        self.training_data = []
        self.companion = CompanionCore()
        self.ai_core = AICore()
        self.game_generator = GameGeneratorEngine()
    
    def register_user(self, username: str, email: str) -> Dict:
        """Registriere neuen User mit eigenem Avatar"""
        user_id = len(self.users) + 1
        user_avatar = UserAvatar(user_id, username)
        
        self.users[user_id] = {
            "username": username,
            "email": email,
            "avatar": user_avatar,
            "created_at": datetime.now().isoformat(),
            "mirrors": [],
            "games_created": 0
        }
        
        return {
            "user_id": user_id,
            "username": username,
            "avatar": user_avatar.name,
            "status": "created"
        }
    
    def create_mirror(self, user_id: int, mirror_idea: str) -> Dict:
        """Erstelle neuen Spiegel (Unterprogramm) für User"""
        mirror_id = f"mirror_{user_id}_{len(self.mirrors)+1}"
        
        # Generiere Game basierend auf Idee
        game_data = self.game_generator.create_game(user_id, mirror_idea)
        
        mirror_data = {
            "mirror_id": mirror_id,
            "user_id": user_id,
            "idea": mirror_idea,
            "game_id": game_data["game_id"],
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "design": self._generate_paradiesical_design()
        }
        
        self.mirrors[mirror_id] = mirror_data
        self.users[user_id]["mirrors"].append(mirror_id)
        
        return mirror_data
    
    def send_chat_message(self, user_id: int, room_name: str, message: str) -> Dict:
        """Sende Chat-Nachricht, Kater antwortet"""
        if room_name not in self.chat_rooms:
            self.chat_rooms[room_name] = []
        
        # User Nachricht
        self.chat_rooms[room_name].append({
            "user_id": user_id,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Kater antwortet
        companion_response = self.companion.respond(message, self.users[user_id]["avatar"].name)
        
        self.chat_rooms[room_name].append({
            "user_id": "master_cat",
            "message": companion_response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Trainiere KI mit Austausch
        self._store_training_data(user_id, message, companion_response)
        
        return {
            "room": room_name,
            "user_message": message,
            "companion_response": companion_response
        }
    
    def get_user_avatar(self, user_id: int) -> Optional[Dict]:
        """Hole User Avatar Informationen"""
        if user_id not in self.users:
            return None
        
        user = self.users[user_id]
        avatar = user["avatar"]
        
        return {
            "user_id": user_id,
            "avatar_name": avatar.name,
            "avatar_personality": avatar.personality,
            "avatar_memory": avatar.memory,
            "interaction_count": len(self.training_data),
            "level": self._calculate_evolution_level(user_id)
        }
    
    def break_mirror(self, mirror_id: str) -> Dict:
        """Zerbreche Spiegel → neue paradiesische Design wird erzeugt"""
        if mirror_id not in self.mirrors:
            return {"error": "Mirror not found"}
        
        mirror = self.mirrors[mirror_id]
        new_design = self._generate_paradiesical_design()
        
        mirror["design"] = new_design
        mirror["last_broken"] = datetime.now().isoformat()
        
        return {
            "mirror_id": mirror_id,
            "new_design": new_design,
            "status": "regenerated"
        }
    
    def _generate_paradiesical_design(self) -> Dict:
        """Generiere verrücktes, magisches Wonderland-Design wie Alice im Wunderland"""
        import random
        
        colors = ["#FF1493", "#00CED1", "#FFD700", "#FF6347", "#9370DB"]
        geometries = ["spiral", "mandala", "fractal", "quantum_tunnel", "shifting_shapes"]
        
        return {
            "primary_color": random.choice(colors),
            "geometry": random.choice(geometries),
            "light_effect": random.choice(["supernova", "quantum_glow", "dreamlight", "paradox"]),
            "sound_theme": random.choice(["ethereal", "chaotic", "mystical", "psychedelic"]),
            "particle_count": random.randint(100, 500),
            "animation_speed": random.uniform(0.5, 2.0)
        }
    
    def _store_training_data(self, user_id: int, input_text: str, response: str):
        """Speichere Trainingsdaten für Evolution"""
        self.training_data.append({
            "user_id": user_id,
            "input": input_text,
            "response": response,
            "timestamp": datetime.now().isoformat()
        })
    
    def _calculate_evolution_level(self, user_id: int) -> int:
        """Berechne Evolution Level basierend auf Interaktionen"""
        user_interactions = sum(1 for t in self.training_data if t["user_id"] == user_id)
        return min(10, max(1, user_interactions // 50))


class UserAvatar:
    """Persönlicher KI-Avatar pro User"""
    
    def __init__(self, user_id: int, name: str):
        self.user_id = user_id
        self.name = name
        self.personality = "curious"
        self.memory = {}
        self.learning_style = "adaptive"
    
    def process_input(self, user_input: str) -> str:
        """Verarbeite Benutzer-Eingabe"""
        self.memory[f"interaction_{len(self.memory)}"] = user_input
        return f"{self.name} verarbeitet: '{user_input}' und übermittelt an System"


class CompanionCore:
    """Master-Kater als Universal KI-Begleiter"""
    
    PERSONALITY_TONES = {
        "mystical": ["Im Nebel der Spiegel erkenne ich...", "Die Quantenwelt flüstert...", "Zwischen den Spiegeln..."],
        "chaotic": ["Chaos bricht aus! Hahahaha!", "Die Spiegel zerbrechen! Neue Welten entstehen!", "Verrücktheit ist Methode!"],
        "wise": ["Weise Wort: ", "Die Lehre besagt: ", "In meinem Alter weiß ich: "]
    }
    
    def respond(self, message: str, user_avatar_name: str) -> str:
        """Master-Kater antwortet auf Nachrichten"""
        import random
        
        tone = random.choice(list(self.PERSONALITY_TONES.keys()))
        response_template = random.choice(self.PERSONALITY_TONES[tone])
        
        return f"{response_template} {message} (über {user_avatar_name})"


class AICore:
    """Zentrale KI-Engine"""
    
    def process(self, prompt: str, user_id: int) -> str:
        """Verarbeite KI-Input"""
        return f"AI_Core verarbeitet für User {user_id}: '{prompt}'"


class GameGeneratorEngine:
    """Generiert Mini-Games & Unterprogramme"""
    
    def __init__(self):
        self.games = {}
    
    def create_game(self, user_id: int, idea: str) -> Dict:
        """Generiere neues Game aus Idee"""
        game_id = f"game_{user_id}_{len(self.games)+1}"
        
        self.games[game_id] = {
            "game_id": game_id,
            "user_id": user_id,
            "idea": idea,
            "type": self._determine_game_type(idea),
            "status": "created"
        }
        
        return self.games[game_id]
    
    def _determine_game_type(self, idea: str) -> str:
        """Bestimme Game-Typ basierend auf Idee"""
        if "jump" in idea.lower() or "platform" in idea.lower():
            return "platformer"
        elif "puzzle" in idea.lower():
            return "puzzle"
        elif "adventure" in idea.lower():
            return "adventure"
        else:
            return "interactive_experience"


# Globale Backend-Instanz
backend = QuantumMirrorBackend()

