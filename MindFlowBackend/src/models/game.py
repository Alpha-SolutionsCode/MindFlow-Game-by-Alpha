from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class GameScore(db.Model):
    """Model for individual game scores"""
    __tablename__ = 'game_scores'
    
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    game_type = db.Column(db.String(50), nullable=False)  # 'memory-cards', 'word-puzzle', etc.
    score = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, default=1)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def __repr__(self):
        return f'<GameScore {self.player_name}: {self.score} in {self.game_type}>'

class Leaderboard(db.Model):
    """Model for leaderboard entries (best scores per player per game)"""
    __tablename__ = 'leaderboard'
    
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(100), nullable=False)
    game_type = db.Column(db.String(50), nullable=False)
    best_score = db.Column(db.Integer, nullable=False)
    best_level = db.Column(db.Integer, default=1)
    total_games = db.Column(db.Integer, default=1)
    last_played = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Ensure unique combination of player and game type
    __table_args__ = (db.UniqueConstraint('player_name', 'game_type'),)
    
    def __repr__(self):
        return f'<Leaderboard {self.player_name}: {self.best_score} in {self.game_type}>'

