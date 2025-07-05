from flask import Blueprint, request, jsonify
from openai import OpenAI
import os
import random
import time
import json
from datetime import datetime

ai_chat_bp = Blueprint('ai_chat', __name__)

# Configuration for AI APIs
OPENAI_API_KEY = "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"
BACKUP_OPENAI_API_KEY = "sk-svcacct-N2GkER-wqvEuOsYBh4v07MmrpIt1ceIkNwZp1iP23RJkOC89M5PhVXKweElT3BlbkFJBzPvl8HlYQnnjNOBe-bYtX8IEk4sP1JrTNmW5InPQsMsgzn1Ph-nZcKHcAA"
HUGGINGFACE_API_KEY = "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"

# Fallback responses for when API is unavailable
FALLBACK_RESPONSES = [
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
    "Twinkle tip: thora break lo, phir try karo! 🌟"
]

def validate_chat_request(data):
    """Validate chat request data"""
    if not data:
        return False, "Request data is required"
    
    if not isinstance(data, dict):
        return False, "Request data must be a JSON object"
    
    message = data.get('message', '').strip()
    if not message:
        return False, "Message is required and cannot be empty"
    
    if len(message) > 1000:
        return False, "Message too long (max 1000 characters)"
    
    # Validate player_name
    player_name = data.get('player_name', 'Player').strip()
    if len(player_name) > 50:
        return False, "Player name too long (max 50 characters)"
    
    # Validate level
    level = data.get('level', 1)
    try:
        level = int(level)
        if level < 1 or level > 100:
            return False, "Level must be between 1 and 100"
    except (ValueError, TypeError):
        return False, "Level must be a valid number"
    
    # Validate context
    context = data.get('context', '').strip()
    if len(context) > 500:
        return False, "Context too long (max 500 characters)"
    
    return True, None

def get_openai_response(user_message, player_name="Player", level=1, context=""):
    """Get response from OpenAI API"""
    try:
        # Create OpenAI client
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        # Create the prompt for Twinkle
        prompt = f"""
Tum Twinkle ho — ek Roman Urdu bolne wali AI jo "MindFlow" game mein player ki dost aur guide hai.

Tumhara style friendly, funny, aur supportive hota hai. Har baat Roman Urdu mein kehni hai.

Player ka naam: {player_name}
Level: {level}
Context: {context}

Player ne kaha: "{user_message}"

Ab Twinkle ke taur pe reply do, sirf Roman Urdu mein. Response choti aur friendly honi chahiye.
"""
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.9
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        # Try backup API key
        try:
            client = OpenAI(api_key=BACKUP_OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.9
            )
            return response.choices[0].message.content.strip()
        except Exception as backup_error:
            print(f"Backup OpenAI API Error: {backup_error}")
            return None

@ai_chat_bp.route('/chat', methods=['POST'])
def chat_with_twinkle():
    """Chat endpoint for Twinkle AI companion"""
    try:
        # Check content type
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json',
                'message': 'Please send JSON data'
            }), 400
        
        # Get and validate request data
        try:
            data = request.get_json()
        except json.JSONDecodeError:
            return jsonify({
                'error': 'Invalid JSON format',
                'message': 'Please check your JSON syntax'
            }), 400
        
        # Validate input
        is_valid, error_message = validate_chat_request(data)
        if not is_valid:
            return jsonify({
                'error': 'Validation failed',
                'message': error_message
            }), 400
        
        # Extract validated data
        user_message = data.get('message', '').strip()
        player_name = data.get('player_name', 'Player').strip()
        level = int(data.get('level', 1))
        context = data.get('context', '').strip()
        
        # Add artificial delay to simulate thinking
        time.sleep(random.uniform(0.5, 2.0))
        
        # Try to get AI response
        ai_response = get_openai_response(user_message, player_name, level, context)
        
        # If AI fails, use fallback response
        if not ai_response:
            ai_response = random.choice(FALLBACK_RESPONSES)
        
        return jsonify({
            'response': ai_response,
            'timestamp': time.time(),
            'source': 'ai' if ai_response not in FALLBACK_RESPONSES else 'mock_ai',
            'player_name': player_name,
            'message_length': len(user_message)
        }), 200
        
    except Exception as e:
        print(f"Chat endpoint error: {e}")
        # Return fallback response on any error
        return jsonify({
            'response': random.choice(FALLBACK_RESPONSES),
            'timestamp': time.time(),
            'source': 'mock_ai',
            'error': 'An error occurred',
            'message': 'Please try again later'
        }), 200

@ai_chat_bp.route('/game-hint', methods=['POST'])
def get_game_hint():
    """Get game-specific hints from Twinkle"""
    try:
        # Check content type
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json',
                'message': 'Please send JSON data'
            }), 400
        
        # Get and validate request data
        try:
            data = request.get_json()
        except json.JSONDecodeError:
            return jsonify({
                'error': 'Invalid JSON format',
                'message': 'Please check your JSON syntax'
            }), 400
        
        if not data:
            return jsonify({
                'error': 'Request data is required'
            }), 400
        
        game_type = data.get('game_type', '').strip()
        if not game_type:
            return jsonify({
                'error': 'Game type is required'
            }), 400
        
        # Validate game type
        valid_game_types = ['memory-cards', 'word-puzzle', 'number-sequence', 'quick-math']
        if game_type not in valid_game_types:
            return jsonify({
                'error': 'Invalid game type',
                'message': f'Game type must be one of: {", ".join(valid_game_types)}'
            }), 400
        
        # Game-specific hint logic
        hints = {
            'memory-cards': [
                "Yaad rakhne ke liye patterns dekho! 🧠",
                "Corners se start karo, easier hota hai! 💡",
                "Ek baar mein sirf 2 cards flip karo! 🎯",
                "Visual memory use karo! 👁️",
                "Take your time, speed se kuch nahi hota! ⏰"
            ],
            'word-puzzle': [
                "Vowels (A, E, I, O, U) pehle try karo! 📝",
                "Common letters jaise R, S, T dekho! ✨",
                "Word ka meaning hint mein hai! 🤔",
                "Prefixes aur suffixes try karo! 🔤",
                "Context clues use karo! 🔍"
            ],
            'number-sequence': [
                "Numbers ko groups mein yaad karo! 🔢",
                "Rhythm banao, jaise music! 🎵",
                "Visualization use karo! 👁️",
                "Patterns dekho! 📊",
                "Mathematical relationships find karo! ➗"
            ],
            'quick-math': [
                "Simple calculations pehle karo! ➕",
                "Tables yaad rakho! ✖️",
                "Speed ke saath accuracy bhi important hai! ⚡",
                "Mental math practice karo! 🧮",
                "Break down complex problems! 🔢"
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
        print(f"Game hint endpoint error: {e}")
        return jsonify({
            'hint': "Main tumhare saath hoon! Try again! 🌟",
            'game_type': 'general',
            'timestamp': time.time(),
            'error': 'An error occurred',
            'message': 'Please try again later'
        }), 200

@ai_chat_bp.route('/encouragement', methods=['POST'])
def get_encouragement():
    """Get encouragement messages from Twinkle"""
    try:
        # Check content type
        if not request.is_json:
            return jsonify({
                'error': 'Content-Type must be application/json',
                'message': 'Please send JSON data'
            }), 400
        
        # Get and validate request data
        try:
            data = request.get_json()
        except json.JSONDecodeError:
            return jsonify({
                'error': 'Invalid JSON format',
                'message': 'Please check your JSON syntax'
            }), 400
        
        if not data:
            return jsonify({
                'error': 'Request data is required'
            }), 400
        
        # Validate score
        score = data.get('score', 0)
        try:
            score = int(score)
            if score < 0:
                return jsonify({
                    'error': 'Score cannot be negative'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'error': 'Score must be a valid number'
            }), 400
        
        game_type = data.get('game_type', '').strip()
        achievement = data.get('achievement', '').strip()
        
        encouragements = []
        
        if score > 50:
            encouragements.extend([
                "Wah! Tumhara score toh kamaal ka hai! 🏆",
                "Pro player ban rahe ho! Main proud hoon! 🌟",
                "Aise hi continue karo! Tum champion ho! 👑",
                "Incredible performance! Tum genius ho! 🧠"
            ])
        elif score > 20:
            encouragements.extend([
                "Bohat acha! Score improve ho raha hai! 📈",
                "Keep it up! Tum kar sakte ho! 💪",
                "Practice makes perfect! 🎯",
                "Getting better every time! 🚀"
            ])
        else:
            encouragements.extend([
                "Koi baat nahi! Start toh acha hai! 🌱",
                "Har expert bhi beginner tha! 🚀",
                "Try again! Main tumhare saath hoon! 💫",
                "Don't give up! Success is around the corner! 🌈"
            ])
        
        if achievement:
            encouragements.append(f"Congratulations on {achievement}! 🎉")
        
        if game_type:
            game_encouragements = {
                'memory-cards': "Memory games mein tumhara dimagh sharp ho raha hai! 🧠",
                'word-puzzle': "Vocabulary improve ho rahi hai! 📚",
                'number-sequence': "Mathematical thinking develop ho rahi hai! 🔢",
                'quick-math': "Mental math skills boost ho rahe hain! ⚡"
            }
            if game_type in game_encouragements:
                encouragements.append(game_encouragements[game_type])
        
        encouragement = random.choice(encouragements)
        
        return jsonify({
            'encouragement': encouragement,
            'score': score,
            'game_type': game_type,
            'timestamp': time.time()
        }), 200
        
    except Exception as e:
        print(f"Encouragement endpoint error: {e}")
        return jsonify({
            'encouragement': "Main tumhare saath hoon! Keep going! 💪",
            'timestamp': time.time(),
            'error': 'An error occurred',
            'message': 'Please try again later'
        }), 200

