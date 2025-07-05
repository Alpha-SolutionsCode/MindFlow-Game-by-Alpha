from flask import Blueprint, request, jsonify
from src.models.game import db, GameScore, Leaderboard
import datetime

game_bp = Blueprint('game', __name__)

@game_bp.route('/scores', methods=['POST'])
def save_score():
    """Save a game score"""
    try:
        data = request.get_json()
        
        player_name = data.get('player_name', 'Anonymous')
        game_type = data.get('game_type')
        score = data.get('score')
        level = data.get('level', 1)
        
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
        
        if leaderboard_entry:
            if score > leaderboard_entry.best_score:
                leaderboard_entry.best_score = score
                leaderboard_entry.best_level = level
                leaderboard_entry.last_played = datetime.datetime.utcnow()
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
        
        db.session.commit()
        
        return jsonify({
            'message': 'Score saved successfully',
            'score_id': game_score.id,
            'is_new_best': leaderboard_entry.best_score == score
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@game_bp.route('/leaderboard/<game_type>', methods=['GET'])
def get_leaderboard(game_type):
    """Get leaderboard for a specific game type"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        leaderboard = Leaderboard.query.filter_by(game_type=game_type)\
            .order_by(Leaderboard.best_score.desc())\
            .limit(limit)\
            .all()
        
        result = []
        for entry in leaderboard:
            result.append({
                'player_name': entry.player_name,
                'best_score': entry.best_score,
                'best_level': entry.best_level,
                'total_games': entry.total_games,
                'last_played': entry.last_played.isoformat() if entry.last_played else None
            })
        
        return jsonify({
            'game_type': game_type,
            'leaderboard': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@game_bp.route('/player-stats/<player_name>', methods=['GET'])
def get_player_stats(player_name):
    """Get statistics for a specific player"""
    try:
        # Get all leaderboard entries for the player
        entries = Leaderboard.query.filter_by(player_name=player_name).all()
        
        if not entries:
            return jsonify({'error': 'Player not found'}), 404
        
        stats = {
            'player_name': player_name,
            'games': {},
            'total_games_played': 0,
            'total_score': 0
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
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@game_bp.route('/recent-scores', methods=['GET'])
def get_recent_scores():
    """Get recent scores across all games"""
    try:
        limit = request.args.get('limit', 20, type=int)
        
        recent_scores = GameScore.query\
            .order_by(GameScore.timestamp.desc())\
            .limit(limit)\
            .all()
        
        result = []
        for score in recent_scores:
            result.append({
                'id': score.id,
                'player_name': score.player_name,
                'game_type': score.game_type,
                'score': score.score,
                'level': score.level,
                'timestamp': score.timestamp.isoformat()
            })
        
        return jsonify({
            'recent_scores': result
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@game_bp.route('/game-types', methods=['GET'])
def get_game_types():
    """Get all available game types"""
    try:
        game_types = db.session.query(Leaderboard.game_type).distinct().all()
        types = [game_type[0] for game_type in game_types]
        
        return jsonify({
            'game_types': types
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

