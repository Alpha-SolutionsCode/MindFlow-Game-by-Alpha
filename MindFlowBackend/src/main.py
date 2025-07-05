import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_compress import Compress
from src.models.user import db
from src.models.game import GameScore, Leaderboard
from src.routes.user import user_bp
from src.routes.game import game_bp
from src.config import get_config
from src.middleware import apply_middleware
# from src.routes.ai_chat import ai_chat_bp  # Temporarily commented out due to pydantic issue
import random
import time
import re
from functools import wraps
from datetime import datetime, timedelta
import threading

# Load configuration
config = get_config()

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Apply configuration
app.config.from_object(config)

# Initialize extensions
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[config.RATELIMIT_DEFAULT]
)

cache = Cache(app)
compress = Compress(app)

# Enable CORS for all routes with better mobile support
CORS(app, origins=config.CORS_ORIGINS, supports_credentials=config.CORS_SUPPORTS_CREDENTIALS, methods=config.CORS_METHODS)

# Apply middleware
apply_middleware(app)

# Rate limiting storage
request_counts = {}
rate_limit_lock = threading.Lock()

def rate_limit(max_requests=100, window=60):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            with rate_limit_lock:
                if client_ip not in request_counts:
                    request_counts[client_ip] = {'count': 0, 'reset_time': current_time + window}
                
                if current_time > request_counts[client_ip]['reset_time']:
                    request_counts[client_ip] = {'count': 0, 'reset_time': current_time + window}
                
                if request_counts[client_ip]['count'] >= max_requests:
                    return jsonify({
                        'error': 'Rate limit exceeded. Please try again later.',
                        'retry_after': int(request_counts[client_ip]['reset_time'] - current_time)
                    }), 429
                
                request_counts[client_ip]['count'] += 1
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_request_data(required_fields=None, optional_fields=None):
    """Request validation decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == 'POST' or request.method == 'PUT':
                if not request.is_json:
                    return jsonify({'error': 'Content-Type must be application/json'}), 400
                
                data = request.get_json()
                if data is None:
                    return jsonify({'error': 'Invalid JSON data'}), 400
                
                # Check required fields
                if required_fields:
                    missing_fields = [field for field in required_fields if field not in data]
                    if missing_fields:
                        return jsonify({
                            'error': f'Missing required fields: {", ".join(missing_fields)}'
                        }), 400
                
                # Validate field types and content
                if 'player_name' in data:
                    if not isinstance(data['player_name'], str) or len(data['player_name'].strip()) == 0:
                        return jsonify({'error': 'Player name must be a non-empty string'}), 400
                    # Sanitize player name
                    data['player_name'] = re.sub(r'[<>"\']', '', data['player_name'].strip())[:50]
                
                if 'message' in data:
                    if not isinstance(data['message'], str) or len(data['message'].strip()) == 0:
                        return jsonify({'error': 'Message must be a non-empty string'}), 400
                    # Sanitize message
                    data['message'] = re.sub(r'[<>"\']', '', data['message'].strip())[:500]
                
                if 'score' in data:
                    try:
                        data['score'] = int(data['score'])
                        if data['score'] < 0:
                            return jsonify({'error': 'Score must be a positive number'}), 400
                    except (ValueError, TypeError):
                        return jsonify({'error': 'Score must be a valid number'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

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
@rate_limit(max_requests=30, window=60)  # 30 requests per minute for AI chat
@validate_request_data(required_fields=['message'], optional_fields=['player_name'])
def mock_ai_chat():
    """Mock AI chat endpoint for Twinkle with improved responsiveness"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        player_name = data.get('player_name', 'Player')
        
        # Add artificial delay to simulate thinking (reduced for better responsiveness)
        time.sleep(random.uniform(0.2, 0.8))
        
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
            'source': 'mock_ai',
            'player_name': player_name,
            'message_length': len(user_message)
        }), 200
        
    except Exception as e:
        app.logger.error(f"AI chat error: {str(e)}")
        return jsonify({
            'response': "Sorry, main thora busy hoon! Try again! 🌟",
            'timestamp': time.time(),
            'source': 'fallback',
            'error': 'Internal server error'
        }), 200

@app.route('/api/ai/game-hint', methods=['POST'])
@rate_limit(max_requests=20, window=60)  # 20 requests per minute for hints
@validate_request_data(required_fields=['game_type'])
def mock_game_hint():
    """Mock game hint endpoint with improved responsiveness"""
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
            'timestamp': time.time(),
            'hint_count': len(game_hints)
        }), 200
        
    except Exception as e:
        app.logger.error(f"Game hint error: {str(e)}")
        return jsonify({
            'hint': "Main tumhare saath hoon! Try again! 🌟",
            'error': 'Internal server error'
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
    """Serve static files with improved mobile support"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return jsonify({'error': 'Static folder not configured'}), 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return jsonify({'error': 'index.html not found'}), 404

@app.route('/health')
@rate_limit(max_requests=1000, window=60)  # High limit for health checks
def health_check():
    """Enhanced health check endpoint with system info"""
    try:
        # Get basic system info
        import psutil
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        
        return jsonify({
            'status': 'healthy',
            'service': 'MindFlow Backend',
            'timestamp': datetime.utcnow().isoformat(),
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available': memory.available // (1024 * 1024)  # MB
            },
            'version': '1.0.0',
            'environment': os.environ.get('FLASK_ENV', 'development')
        }), 200
    except ImportError:
        # psutil not available, return basic health check
        return jsonify({
            'status': 'healthy',
            'service': 'MindFlow Backend',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }), 200
    except Exception as e:
        app.logger.error(f"Health check error: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/status')
@rate_limit(max_requests=100, window=60)
def api_status():
    """API status endpoint for mobile apps"""
    return jsonify({
        'api_version': '1.0.0',
        'status': 'operational',
        'features': {
            'ai_chat': True,
            'game_scores': True,
            'leaderboard': True,
            'user_management': True
        },
        'mobile_support': True,
        'rate_limits': {
            'ai_chat': '30 requests/minute',
            'game_hints': '20 requests/minute',
            'general': '100 requests/minute'
        }
    }), 200

@app.route('/api-docs')
def api_docs():
    """Serve API documentation page"""
    if app.static_folder is None:
        return "Static folder not configured", 404
    return send_from_directory(app.static_folder, 'api-docs.html')

@app.route('/admin')
def admin_dashboard():
    """Serve admin dashboard page"""
    if app.static_folder is None:
        return "Static folder not configured", 404
    return send_from_directory(app.static_folder, 'admin.html')

# Error handlers for better mobile experience
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Endpoint not found',
        'message': 'The requested resource does not exist',
        'status_code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal server error: {str(error)}")
    return jsonify({
        'error': 'Internal server error',
        'message': 'Something went wrong on our end. Please try again later.',
        'status_code': 500
    }), 500

@app.errorhandler(413)
def too_large(error):
    return jsonify({
        'error': 'Request too large',
        'message': 'The request payload is too large',
        'status_code': 413
    }), 413

if __name__ == '__main__':
    # Configure for better mobile performance
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=True,
        threaded=True,  # Enable threading for better concurrency
        use_reloader=True
    )
