import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from src.models.user import db
from src.models.game import GameScore, Leaderboard
from src.routes.user import user_bp
from src.routes.game import game_bp
# from src.routes.ai_chat import ai_chat_bp  # Temporarily commented out due to pydantic issue
import random
import time

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'sk-svcacct-N2GkER-wqvEuOsYBh4v07MmrpIt1ceIkNwZp1iP23RJkOC89M5PhVXKweElT3BlbkFJBzPvl8HlYQnnjNOBe-bYtX8IEk4sP1JrTNmW5InPQsMsgzn1Ph-nZcKHcAA'

# Enable CORS for all routes
CORS(app, origins="*")

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(game_bp, url_prefix='/api/game')
# app.register_blueprint(ai_chat_bp, url_prefix='/api/ai')  # Temporarily commented out

# Mock AI responses for Twinkle
TWINKLE_RESPONSES = [
    "Salam! Main Twinkle hoon, tumhari AI dost! Kya haal hai? 😊",
    "Wah! Bohat interesting sawal hai! Main soch rahi hoon... 🤔",
    "Oyee! Tumhara dimagh toh kamaal ka hai! Iska jawab toh main bhi dhund rahi hoon 😄",
    "Hmm, yeh puzzle thora tricky hai. Kya tumne left side try kiya? 🧩",
    "Arre yaar, tum toh genius ho! Main impressed hoon 🌟",
    "Chalo ek hint deti hoon: yeh answer 'A' se start hota hai... 💡",
    "Gossip time! Suna hai aaj weather bohat acha hai, perfect for brain games! ☀️",
    "Tumhara score improve ho raha hai! Keep it up! 🏆",
    "Ek minute... main check kar rahi hoon database mein... Found it! ✨",
    "Kya baat hai! Tum toh pro player ban rahe ho! 🎮",
    "Main tumhare saath games khelna pasand karti hoon! 💫",
    "Twinkle tip: thora break lo, phir try karo! 🌟",
    "Acha! Main tumhare saath hoon! Kya help chahiye? 🤗",
    "Bohat acha question hai! Main soch rahi hoon... 🧠",
    "Tumhara confidence dekh ke main khush hoon! 🌈",
    "Chalo ek aur game khelte hain! Ready ho? 🎯"
]

@app.route('/api/ai/chat', methods=['POST'])
def mock_ai_chat():
    """Mock AI chat endpoint for Twinkle"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        player_name = data.get('player_name', 'Player')
        
        # Add artificial delay to simulate thinking
        time.sleep(random.uniform(0.5, 1.5))
        
        # Generate contextual response based on user message
        if any(word in user_message.lower() for word in ['hello', 'hi', 'salam', 'kaise ho']):
            response = f"Salam {player_name}! Main Twinkle hoon! Kya haal hai? 😊"
        elif any(word in user_message.lower() for word in ['help', 'madad', 'problem']):
            response = "Main tumhari help karungi! Kya problem hai? 🤗"
        elif any(word in user_message.lower() for word in ['game', 'khel', 'score']):
            response = "Games mein expert banne ke liye practice karo! Main tumhare saath hoon! 🎮"
        elif any(word in user_message.lower() for word in ['tired', 'thak', 'break']):
            response = "Thora break lo! Fresh mind se better khelte hain! ☕"
        else:
            response = random.choice(TWINKLE_RESPONSES)
        
        return jsonify({
            'response': response,
            'timestamp': time.time(),
            'source': 'mock_ai'
        }), 200
        
    except Exception as e:
        return jsonify({
            'response': "Sorry, main thora busy hoon! Try again! 🌟",
            'timestamp': time.time(),
            'source': 'fallback',
            'error': str(e)
        }), 200

@app.route('/api/ai/game-hint', methods=['POST'])
def mock_game_hint():
    """Mock game hint endpoint"""
    try:
        data = request.get_json()
        game_type = data.get('game_type', 'general')
        
        hints = {
            'memory-cards': [
                "Yaad rakhne ke liye patterns dekho! 🧠",
                "Corners se start karo, easier hota hai! 💡",
                "Ek baar mein sirf 2 cards flip karo! 🎯"
            ],
            'word-puzzle': [
                "Vowels (A, E, I, O, U) pehle try karo! 📝",
                "Common letters jaise R, S, T dekho! ✨",
                "Word ka meaning hint mein hai! 🤔"
            ],
            'number-sequence': [
                "Numbers ko groups mein yaad karo! 🔢",
                "Rhythm banao, jaise music! 🎵",
                "Visualization use karo! 👁️"
            ],
            'quick-math': [
                "Simple calculations pehle karo! ➕",
                "Tables yaad rakho! ✖️",
                "Speed ke saath accuracy bhi important hai! ⚡"
            ]
        }
        
        game_hints = hints.get(game_type, ["Keep trying! Tum kar sakte ho! 💪"])
        hint = random.choice(game_hints)
        
        return jsonify({
            'hint': hint,
            'game_type': game_type,
            'timestamp': time.time()
        }), 200
        
    except Exception as e:
        return jsonify({
            'hint': "Main tumhare saath hoon! Try again! 🌟",
            'error': str(e)
        }), 200

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {'status': 'healthy', 'service': 'MindFlow Backend'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
