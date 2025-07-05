from flask import Blueprint, request, jsonify
import openai
import os
import random
import time

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

def get_openai_response(user_message, player_name="Player", level=1, context=""):
    """Get response from OpenAI API"""
    try:
        # Set the API key
        openai.api_key = OPENAI_API_KEY
        
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
        
        response = openai.ChatCompletion.create(
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
            openai.api_key = BACKUP_OPENAI_API_KEY
            response = openai.ChatCompletion.create(
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
        data = request.get_json()
        
        user_message = data.get('message', '')
        player_name = data.get('player_name', 'Player')
        level = data.get('level', 1)
        context = data.get('context', '')
        
        if not user_message:
            return jsonify({'error': 'Message is required'}), 400
        
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
            'source': 'ai' if ai_response not in FALLBACK_RESPONSES else 'fallback'
        }), 200
        
    except Exception as e:
        # Return fallback response on any error
        return jsonify({
            'response': random.choice(FALLBACK_RESPONSES),
            'timestamp': time.time(),
            'source': 'fallback',
            'error': str(e)
        }), 200

@ai_chat_bp.route('/game-hint', methods=['POST'])
def get_game_hint():
    """Get game-specific hints from Twinkle"""
    try:
        data = request.get_json()
        
        game_type = data.get('game_type')
        current_state = data.get('current_state', {})
        player_name = data.get('player_name', 'Player')
        
        # Game-specific hint logic
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

@ai_chat_bp.route('/encouragement', methods=['POST'])
def get_encouragement():
    """Get encouragement messages from Twinkle"""
    try:
        data = request.get_json()
        
        score = data.get('score', 0)
        game_type = data.get('game_type', '')
        achievement = data.get('achievement', '')
        
        encouragements = []
        
        if score > 50:
            encouragements.extend([
                "Wah! Tumhara score toh kamaal ka hai! 🏆",
                "Pro player ban rahe ho! Main proud hoon! 🌟",
                "Aise hi continue karo! Tum champion ho! 👑"
            ])
        elif score > 20:
            encouragements.extend([
                "Bohat acha! Score improve ho raha hai! 📈",
                "Keep it up! Tum kar sakte ho! 💪",
                "Practice makes perfect! 🎯"
            ])
        else:
            encouragements.extend([
                "Koi baat nahi! Start toh acha hai! 🌱",
                "Har expert bhi beginner tha! 🚀",
                "Try again! Main tumhare saath hoon! 💫"
            ])
        
        if achievement:
            encouragements.append(f"Congratulations on {achievement}! 🎉")
        
        message = random.choice(encouragements)
        
        return jsonify({
            'message': message,
            'timestamp': time.time()
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': "Tum bohot acha kar rahe ho! 🌟",
            'error': str(e)
        }), 200

