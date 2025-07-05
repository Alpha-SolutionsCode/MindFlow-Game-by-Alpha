// API service for MindFlow application
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://localhost:5000/api'

class ApiService {
  // Chat API methods
  static async sendChatMessage(message, playerName = 'Player', level = 1, context = '') {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          player_name: playerName,
          level,
          context
        })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Chat API error:', error)
      // Return fallback response
      return {
        response: "Sorry, main thora busy hoon! Try again! 😊",
        timestamp: Date.now() / 1000,
        source: 'fallback'
      }
    }
  }

  static async getGameHint(gameType, currentState = {}, playerName = 'Player') {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/game-hint`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          game_type: gameType,
          current_state: currentState,
          player_name: playerName
        })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Game hint API error:', error)
      return {
        hint: "Keep trying! Tum kar sakte ho! 💪",
        game_type: gameType,
        timestamp: Date.now() / 1000
      }
    }
  }

  static async getEncouragement(score = 0, gameType = '', achievement = '') {
    try {
      const response = await fetch(`${API_BASE_URL}/ai/encouragement`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          score,
          game_type: gameType,
          achievement
        })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Encouragement API error:', error)
      return {
        message: "Tum bohot acha kar rahe ho! 🌟",
        timestamp: Date.now() / 1000
      }
    }
  }

  // Game API methods
  static async saveScore(playerName, gameType, score, level = 1) {
    try {
      const response = await fetch(`${API_BASE_URL}/game/scores`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          player_name: playerName,
          game_type: gameType,
          score,
          level
        })
      })
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Save score API error:', error)
      return { error: 'Failed to save score' }
    }
  }

  static async getLeaderboard(gameType, limit = 10) {
    try {
      const response = await fetch(`${API_BASE_URL}/game/leaderboard/${gameType}?limit=${limit}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Leaderboard API error:', error)
      return { 
        game_type: gameType, 
        leaderboard: [],
        error: 'Failed to load leaderboard'
      }
    }
  }

  static async getPlayerStats(playerName) {
    try {
      const response = await fetch(`${API_BASE_URL}/game/player-stats/${encodeURIComponent(playerName)}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Player stats API error:', error)
      return { 
        error: 'Failed to load player stats',
        player_name: playerName,
        games: {},
        total_games_played: 0,
        total_score: 0
      }
    }
  }

  static async getRecentScores(limit = 20) {
    try {
      const response = await fetch(`${API_BASE_URL}/game/recent-scores?limit=${limit}`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Recent scores API error:', error)
      return { 
        recent_scores: [],
        error: 'Failed to load recent scores'
      }
    }
  }

  static async getGameTypes() {
    try {
      const response = await fetch(`${API_BASE_URL}/game/game-types`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Game types API error:', error)
      return { 
        game_types: ['memory-cards', 'word-puzzle', 'number-sequence', 'quick-math'],
        error: 'Failed to load game types'
      }
    }
  }

  // Health check
  static async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL.replace('/api', '')}/health`)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('Health check error:', error)
      return { 
        status: 'error',
        service: 'MindFlow Backend',
        error: error.message
      }
    }
  }
}

export default ApiService

