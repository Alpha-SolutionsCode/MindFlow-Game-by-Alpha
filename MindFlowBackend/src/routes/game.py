from flask import Blueprint, request, jsonify
from src.models.game import db, GameScore, Leaderboard
import datetime
from functools import wraps
import time
import re

game_bp = Blueprint('game', __name__)

# Rate limiting storage for game routes
game_request_counts = {}

def game_rate_limit(max_requests=50, window=60):
    """Rate limiting decorator for game routes"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = request.remote_addr
            current_time = time.time()
            
            if client_ip not in game_request_counts:
                game_request_counts[client_ip] = {'count': 0, 'reset_time': current_time + window}
            
            if current_time > game_request_counts[client_ip]['reset_time']:
                game_request_counts[client_ip] = {'count': 0, 'reset_time': current_time + window}
            
            if game_request_counts[client_ip]['count'] >= max_requests:
                return jsonify({
                    'error': 'Game rate limit exceeded. Please try again later.',
                    'retry_after': int(game_request_counts[client_ip]['reset_time'] - current_time)
                }), 429
            
            game_request_counts[client_ip]['count'] += 1
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def validate_game_data(required_fields=None):
    """Game data validation decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == 'POST':
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
                
                # Validate and sanitize data
                if 'player_name' in data:
                    if not isinstance(data['player_name'], str) or len(data['player_name'].strip()) == 0:
                        return jsonify({'error': 'Player name must be a non-empty string'}), 400
                    # Sanitize player name
                    data['player_name'] = re.sub(r'[<>"\']', '', data['player_name'].strip())[:50]
                
                if 'game_type' in data:
                    if not isinstance(data['game_type'], str) or len(data['game_type'].strip()) == 0:
                        return jsonify({'error': 'Game type must be a non-empty string'}), 400
                    # Sanitize game type
                    data['game_type'] = re.sub(r'[<>"\']', '', data['game_type'].strip())[:30]
                
                if 'score' in data:
                    try:
                        data['score'] = int(data['score'])
                        if data['score'] < 0:
                            return jsonify({'error': 'Score must be a positive number'}), 400
                        if data['score'] > 999999:  # Reasonable upper limit
                            return jsonify({'error': 'Score is too high'}), 400
                    except (ValueError, TypeError):
                        return jsonify({'error': 'Score must be a valid number'}), 400
                
                if 'level' in data:
                    try:
                        data['level'] = int(data['level'])
                        if data['level'] < 1:
                            return jsonify({'error': 'Level must be at least 1'}), 400
                        if data['level'] > 100:  # Reasonable upper limit
                            return jsonify({'error': 'Level is too high'}), 400
                    except (ValueError, TypeError):
                        return jsonify({'error': 'Level must be a valid number'}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@game_bp.route('/scores', methods=['POST'])
@game_rate_limit(max_requests=30, window=60)  # 30 score submissions per minute
@validate_game_data(required_fields=['player_name', 'game_type', 'score'])
def save_score():
    """Save a game score with improved validation and responsiveness"""
    try:
        data = request.get_json()
        
        player_name = data.get('player_name', 'Anonymous')
        game_type = data.get('game_type')
        score = data.get('score')
        level = data.get('level', 1)
        
        # Additional validation
        if not game_type or score is None:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Save individual score
        game_score = GameScore(
            player_name=player_name,
            game_type=game_type,
            score=score,
            level=level,
            timestamp=datetime.datetime.utcnow()
        )
        
        db.session.add(game_score)
        
        # Update or create leaderboard entry
        leaderboard_entry = Leaderboard.query.filter_by(
            player_name=player_name, 
            game_type=game_type
        ).first()
        
        is_new_best = False
        if leaderboard_entry:
            if score > leaderboard_entry.best_score:
                leaderboard_entry.best_score = score
                leaderboard_entry.best_level = level
                leaderboard_entry.last_played = datetime.datetime.utcnow()
                is_new_best = True
            leaderboard_entry.total_games += 1
        else:
            leaderboard_entry = Leaderboard(
                player_name=player_name,
                game_type=game_type,
                best_score=score,
                best_level=level,
                total_games=1,
                last_played=datetime.datetime.utcnow()
            )
            db.session.add(leaderboard_entry)
            is_new_best = True
        
        db.session.commit()
        
        return jsonify({
            'message': 'Score saved successfully',
            'score_id': game_score.id,
            'is_new_best': is_new_best,
            'player_name': player_name,
            'game_type': game_type,
            'score': score,
            'level': level,
            'timestamp': game_score.timestamp.isoformat()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Failed to save score',
            'message': 'Please try again later'
        }), 500

@game_bp.route('/leaderboard/<game_type>', methods=['GET'])
@game_rate_limit(max_requests=100, window=60)  # 100 leaderboard requests per minute
def get_leaderboard(game_type):
    """Get leaderboard for a specific game type with pagination and mobile optimization"""
    try:
        # Validate game_type
        if not game_type or len(game_type.strip()) == 0:
            return jsonify({'error': 'Invalid game type'}), 400
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 50)  # Max 50 per page
        limit = request.args.get('limit', 10, type=int)
        
        # Ensure reasonable limits
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 50:
            per_page = 10
        if limit < 1 or limit > 100:
            limit = 10
        
        # Get leaderboard with pagination
        offset = (page - 1) * per_page
        leaderboard = Leaderboard.query.filter_by(game_type=game_type)\
            .order_by(Leaderboard.best_score.desc())\
            .offset(offset)\
            .limit(limit)\
            .all()
        
        # Get total count for pagination info
        total_count = Leaderboard.query.filter_by(game_type=game_type).count()
        
        result = []
        for i, entry in enumerate(leaderboard):
            result.append({
                'rank': offset + i + 1,
                'player_name': entry.player_name,
                'best_score': entry.best_score,
                'best_level': entry.best_level,
                'total_games': entry.total_games,
                'last_played': entry.last_played.isoformat() if entry.last_played else None
            })
        
        return jsonify({
            'game_type': game_type,
            'leaderboard': result,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': (total_count + per_page - 1) // per_page
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch leaderboard',
            'message': 'Please try again later'
        }), 500

@game_bp.route('/player-stats/<player_name>', methods=['GET'])
@game_rate_limit(max_requests=50, window=60)  # 50 player stats requests per minute
def get_player_stats(player_name):
    """Get statistics for a specific player with enhanced mobile support"""
    try:
        # Validate player name
        if not player_name or len(player_name.strip()) == 0:
            return jsonify({'error': 'Invalid player name'}), 400
        
        # Get all leaderboard entries for the player
        entries = Leaderboard.query.filter_by(player_name=player_name).all()
        
        if not entries:
            return jsonify({
                'error': 'Player not found',
                'message': 'No statistics found for this player'
            }), 404
        
        stats = {
            'player_name': player_name,
            'games': {},
            'total_games_played': 0,
            'total_score': 0,
            'average_score': 0,
            'games_played': len(entries)
        }
        
        for entry in entries:
            stats['games'][entry.game_type] = {
                'best_score': entry.best_score,
                'best_level': entry.best_level,
                'total_games': entry.total_games,
                'last_played': entry.last_played.isoformat() if entry.last_played else None
            }
            stats['total_games_played'] += entry.total_games
            stats['total_score'] += entry.best_score
        
        # Calculate average score
        if stats['total_games_played'] > 0:
            stats['average_score'] = round(stats['total_score'] / stats['total_games_played'], 2)
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch player statistics',
            'message': 'Please try again later'
        }), 500

@game_bp.route('/recent-scores', methods=['GET'])
@game_rate_limit(max_requests=100, window=60)  # 100 recent scores requests per minute
def get_recent_scores():
    """Get recent scores across all games with pagination and filtering"""
    try:
        # Get pagination and filter parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)  # Max 100 per page
        game_type = request.args.get('game_type')  # Optional filter
        player_name = request.args.get('player_name')  # Optional filter
        
        # Ensure reasonable limits
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        # Build query with filters
        query = GameScore.query
        
        if game_type:
            query = query.filter_by(game_type=game_type)
        
        if player_name:
            query = query.filter_by(player_name=player_name)
        
        # Get total count for pagination
        total_count = query.count()
        
        # Get paginated results
        offset = (page - 1) * per_page
        recent_scores = query\
            .order_by(GameScore.timestamp.desc())\
            .offset(offset)\
            .limit(per_page)\
            .all()
        
        result = []
        for i, score in enumerate(recent_scores):
            result.append({
                'id': score.id,
                'rank': offset + i + 1,
                'player_name': score.player_name,
                'game_type': score.game_type,
                'score': score.score,
                'level': score.level,
                'timestamp': score.timestamp.isoformat()
            })
        
        return jsonify({
            'recent_scores': result,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': (total_count + per_page - 1) // per_page
            },
            'filters': {
                'game_type': game_type,
                'player_name': player_name
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch recent scores',
            'message': 'Please try again later'
        }), 500

@game_bp.route('/game-types', methods=['GET'])
@game_rate_limit(max_requests=200, window=60)  # 200 game types requests per minute
def get_game_types():
    """Get all available game types with additional metadata"""
    try:
        game_types = db.session.query(Leaderboard.game_type).distinct().all()
        types = [game_type[0] for game_type in game_types]
        
        # Add metadata for each game type
        game_metadata = {}
        for game_type in types:
            # Get stats for this game type
            total_players = Leaderboard.query.filter_by(game_type=game_type).count()
            total_games = db.session.query(GameScore).filter_by(game_type=game_type).count()
            
            game_metadata[game_type] = {
                'total_players': total_players,
                'total_games': total_games,
                'last_updated': datetime.datetime.utcnow().isoformat()
            }
        
        return jsonify({
            'game_types': types,
            'metadata': game_metadata,
            'total_game_types': len(types)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch game types',
            'message': 'Please try again later'
        }), 500

@game_bp.route('/top-players', methods=['GET'])
@game_rate_limit(max_requests=50, window=60)  # 50 top players requests per minute
def get_top_players():
    """Get top players across all games"""
    try:
        limit = min(request.args.get('limit', 10, type=int), 50)  # Max 50 players
        
        # Get players with highest total scores across all games
        top_players = db.session.query(
            Leaderboard.player_name,
            db.func.sum(Leaderboard.best_score).label('total_score'),
            db.func.sum(Leaderboard.total_games).label('total_games'),
            db.func.count(Leaderboard.game_type).label('games_played')
        ).group_by(Leaderboard.player_name)\
         .order_by(db.func.sum(Leaderboard.best_score).desc())\
         .limit(limit)\
         .all()
        
        result = []
        for i, player in enumerate(top_players):
            result.append({
                'rank': i + 1,
                'player_name': player.player_name,
                'total_score': player.total_score,
                'total_games': player.total_games,
                'games_played': player.games_played,
                'average_score': round(player.total_score / player.total_games, 2) if player.total_games > 0 else 0
            })
        
        return jsonify({
            'top_players': result,
            'total_players': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to fetch top players',
            'message': 'Please try again later'
        }), 500

