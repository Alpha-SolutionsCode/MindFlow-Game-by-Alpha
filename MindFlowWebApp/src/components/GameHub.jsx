import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { 
  Brain, 
  Gamepad2, 
  Trophy, 
  Star, 
  ArrowLeft, 
  Shuffle, 
  Target,
  Zap,
  Clock,
  CheckCircle
} from 'lucide-react'

const GameHub = ({ onBack }) => {
  const [currentGame, setCurrentGame] = useState(null)
  const [gameScore, setGameScore] = useState(0)
  const [gameLevel, setGameLevel] = useState(1)

  const games = [
    {
      id: 'memory-cards',
      title: 'Memory Cards',
      description: 'Match pairs of cards to test your memory',
      icon: <Brain className="w-6 h-6 sm:w-8 sm:h-8" />,
      difficulty: 'Easy',
      color: 'bg-gradient-to-r from-blue-500 to-blue-600'
    },
    {
      id: 'word-puzzle',
      title: 'Word Puzzle',
      description: 'Unscramble words with Twinkle\'s hints',
      icon: <Shuffle className="w-6 h-6 sm:w-8 sm:h-8" />,
      difficulty: 'Medium',
      color: 'bg-gradient-to-r from-green-500 to-green-600'
    },
    {
      id: 'number-sequence',
      title: 'Number Sequence',
      description: 'Remember and repeat number sequences',
      icon: <Target className="w-6 h-6 sm:w-8 sm:h-8" />,
      difficulty: 'Hard',
      color: 'bg-gradient-to-r from-red-500 to-red-600'
    },
    {
      id: 'quick-math',
      title: 'Quick Math',
      description: 'Solve math problems against the clock',
      icon: <Zap className="w-6 h-6 sm:w-8 sm:h-8" />,
      difficulty: 'Medium',
      color: 'bg-gradient-to-r from-purple-500 to-purple-600'
    }
  ]

  const renderGameSelection = () => (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900 p-3 sm:p-4 overflow-x-hidden">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="flex flex-col items-center justify-between mb-6 sm:mb-8 gap-4 w-full">
          <Button
            onClick={onBack}
            variant="outline"
            className="border-2 border-white text-white hover:bg-white hover:text-purple-900 w-full max-w-[200px] self-start text-sm sm:text-base font-medium rounded-lg transition-all duration-200"
          >
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Home
          </Button>
          <div className="text-center w-full px-2">
            <h1 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-2 break-words">Alpha Games</h1>
            <p className="text-purple-200 text-sm sm:text-base md:text-lg break-words leading-relaxed">Choose your challenge and play with Twinkle!</p>
          </div>
          <div className="flex flex-row items-center justify-center space-x-2 sm:space-x-4 w-full px-2">
            <Badge className="bg-gradient-to-r from-yellow-400 to-orange-400 text-purple-900 text-sm sm:text-base px-3 py-2 font-medium">
              <Trophy className="w-4 h-4 mr-1" />
              Score: {gameScore}
            </Badge>
            <Badge className="bg-gradient-to-r from-green-500 to-green-600 text-white text-sm sm:text-base px-3 py-2 font-medium">
              Level: {gameLevel}
            </Badge>
          </div>
        </div>

        {/* Games Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6 mb-8 sm:mb-12">
          {games.map((game) => (
            <Card 
              key={game.id}
              className="bg-white/10 backdrop-blur-lg border-white/20 text-white hover:scale-105 transition-all duration-300 cursor-pointer hover:shadow-xl hover:bg-white/15"
              onClick={() => setCurrentGame(game.id)}
            >
              <CardHeader className="text-center p-4 sm:p-6">
                <div className={`w-12 h-12 sm:w-16 sm:h-16 md:w-20 md:h-20 ${game.color} rounded-full flex items-center justify-center mx-auto mb-3 sm:mb-4 text-white shadow-lg`}>
                  {game.icon}
                </div>
                <CardTitle className="text-base sm:text-lg md:text-xl font-bold">{game.title}</CardTitle>
                <Badge variant="secondary" className="mx-auto text-xs sm:text-sm bg-white/20 text-white border-white/30">
                  {game.difficulty}
                </Badge>
              </CardHeader>
              <CardContent className="p-4 sm:p-6 pt-0">
                <CardDescription className="text-purple-200 text-center text-sm sm:text-base leading-relaxed">
                  {game.description}
                </CardDescription>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Twinkle's Tips */}
        <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-4 sm:p-6 md:p-8 border border-white/20">
          <div className="flex flex-col sm:flex-row items-center space-y-3 sm:space-y-0 sm:space-x-4 mb-4 sm:mb-6">
            <div className="w-10 h-10 sm:w-12 sm:h-12 md:w-14 md:h-14 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full flex items-center justify-center">
              <Star className="w-5 h-5 sm:w-6 sm:h-6 text-purple-900" />
            </div>
            <div className="text-center sm:text-left">
              <h3 className="text-lg sm:text-xl md:text-2xl font-bold text-white">Twinkle's Gaming Tips</h3>
              <p className="text-purple-200 text-sm sm:text-base">Your AI companion is here to help!</p>
            </div>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 text-purple-200 text-sm sm:text-base">
            <div className="flex items-start space-x-3">
              <CheckCircle className="w-5 h-5 sm:w-6 sm:h-6 text-green-400 mt-0.5 flex-shrink-0" />
              <span>Start with easier games to build confidence</span>
            </div>
            <div className="flex items-start space-x-3">
              <CheckCircle className="w-5 h-5 sm:w-6 sm:h-6 text-green-400 mt-0.5 flex-shrink-0" />
              <span>Take breaks between challenging levels</span>
            </div>
            <div className="flex items-start space-x-3">
              <CheckCircle className="w-5 h-5 sm:w-6 sm:h-6 text-green-400 mt-0.5 flex-shrink-0" />
              <span>Ask me for hints if you get stuck!</span>
            </div>
            <div className="flex items-start space-x-3">
              <CheckCircle className="w-5 h-5 sm:w-6 sm:h-6 text-green-400 mt-0.5 flex-shrink-0" />
              <span>Practice daily to improve your scores</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )

  const renderGame = () => {
    const game = games.find(g => g.id === currentGame)
    
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900 p-3 sm:p-4 overflow-x-hidden">
        <div className="max-w-4xl mx-auto">
          {/* Game Header */}
          <div className="flex flex-col items-center justify-between mb-6 sm:mb-8 gap-4 w-full">
            <Button
              onClick={() => setCurrentGame(null)}
              variant="outline"
              className="border-2 border-white text-white hover:bg-white hover:text-purple-900 w-full max-w-[200px] self-start text-sm sm:text-base font-medium rounded-lg transition-all duration-200"
            >
              <ArrowLeft className="w-4 h-4 mr-2" />
              Back to Games
            </Button>
            <div className="text-center w-full px-2">
              <h1 className="text-xl sm:text-2xl md:text-3xl lg:text-4xl font-bold text-white break-words">{game?.title}</h1>
              <p className="text-purple-200 text-sm sm:text-base md:text-lg break-words leading-relaxed">{game?.description}</p>
            </div>
            <div className="flex items-center justify-center space-x-3 w-full px-2">
              <Badge className="bg-gradient-to-r from-yellow-400 to-orange-400 text-purple-900 text-sm sm:text-base px-3 py-2 font-medium">
                <Trophy className="w-4 h-4 mr-1" />
                {gameScore}
              </Badge>
            </div>
          </div>

          {/* Game Content */}
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-4 sm:p-6 md:p-8 border border-white/20">
            {currentGame === 'memory-cards' && <MemoryCardGame onScore={setGameScore} />}
            {currentGame === 'word-puzzle' && <WordPuzzleGame onScore={setGameScore} />}
            {currentGame === 'number-sequence' && <NumberSequenceGame onScore={setGameScore} />}
            {currentGame === 'quick-math' && <QuickMathGame onScore={setGameScore} />}
          </div>
        </div>
      </div>
    )
  }

  return currentGame ? renderGame() : renderGameSelection()
}

// Memory Card Game Component
const MemoryCardGame = ({ onScore }) => {
  const [cards, setCards] = useState([])
  const [flippedCards, setFlippedCards] = useState([])
  const [matchedCards, setMatchedCards] = useState([])
  const [moves, setMoves] = useState(0)
  const [gameStarted, setGameStarted] = useState(false)

  const symbols = ['🌟', '🎯', '🎮', '🏆', '⚡', '🧠', '💎', '🎪']

  const initializeGame = () => {
    const gameCards = [...symbols, ...symbols]
      .sort(() => Math.random() - 0.5)
      .map((symbol, index) => ({
        id: index,
        symbol,
        isFlipped: false,
        isMatched: false
      }))
    
    setCards(gameCards)
    setFlippedCards([])
    setMatchedCards([])
    setMoves(0)
    setGameStarted(true)
  }

  const handleCardClick = (cardId) => {
    if (flippedCards.length === 2) return
    if (flippedCards.includes(cardId)) return
    if (matchedCards.includes(cardId)) return

    const newFlippedCards = [...flippedCards, cardId]
    setFlippedCards(newFlippedCards)

    if (newFlippedCards.length === 2) {
      setMoves(moves + 1)
      const [firstCard, secondCard] = newFlippedCards
      const firstSymbol = cards.find(c => c.id === firstCard)?.symbol
      const secondSymbol = cards.find(c => c.id === secondCard)?.symbol

      if (firstSymbol === secondSymbol) {
        setMatchedCards([...matchedCards, firstCard, secondCard])
        setFlippedCards([])
        onScore(prev => prev + 10)
      } else {
        setTimeout(() => {
          setFlippedCards([])
        }, 1000)
      }
    }
  }

  return (
    <div className="text-center w-full max-w-full">
      <div className="flex flex-col sm:flex-row justify-between items-center mb-6 gap-2 w-full max-w-full">
        <div className="text-white">
          <span className="text-base sm:text-lg">Moves: {moves}</span>
        </div>
        <div className="text-white">
          <span className="text-base sm:text-lg">Matched: {matchedCards.length / 2}/{symbols.length}</span>
        </div>
      </div>

      {!gameStarted ? (
        <div className="text-center">
          <h3 className="text-xl sm:text-2xl font-bold text-white mb-4">Memory Card Challenge</h3>
          <p className="text-purple-200 mb-6 text-sm sm:text-base">Match all pairs of cards to win!</p>
          <Button onClick={initializeGame} className="bg-yellow-400 hover:bg-yellow-500 text-purple-900">
            Start Game
          </Button>
        </div>
      ) : (
        <div className="grid grid-cols-4 gap-2 sm:gap-4 max-w-xs sm:max-w-md mx-auto w-full">
          {cards.map((card) => (
            <div
              key={card.id}
              onClick={() => handleCardClick(card.id)}
              className={`w-12 h-12 sm:w-16 sm:h-16 rounded-lg flex items-center justify-center text-lg sm:text-2xl cursor-pointer transition-all duration-300 ${
                flippedCards.includes(card.id) || matchedCards.includes(card.id)
                  ? 'bg-white text-purple-900'
                  : 'bg-purple-600 hover:bg-purple-500'
              }`}
            >
              {flippedCards.includes(card.id) || matchedCards.includes(card.id) 
                ? card.symbol 
                : '?'
              }
            </div>
          ))}
        </div>
      )}

      {matchedCards.length === cards.length && (
        <div className="mt-6 text-center">
          <h3 className="text-xl sm:text-2xl font-bold text-yellow-400 mb-2">Congratulations! 🎉</h3>
          <p className="text-white text-sm sm:text-base">You completed the game in {moves} moves!</p>
          <Button onClick={initializeGame} className="mt-4 bg-yellow-400 hover:bg-yellow-500 text-purple-900">
            Play Again
          </Button>
        </div>
      )}
    </div>
  )
}

// Word Puzzle Game Component
const WordPuzzleGame = ({ onScore }) => {
  const [currentWord, setCurrentWord] = useState('')
  const [scrambledWord, setScrambledWord] = useState('')
  const [userGuess, setUserGuess] = useState('')
  const [score, setScore] = useState(0)
  const [hint, setHint] = useState('')
  const [gameStarted, setGameStarted] = useState(false)

  const words = [
    { word: 'BRAIN', hint: 'Organ used for thinking' },
    { word: 'PUZZLE', hint: 'A game that challenges your mind' },
    { word: 'MEMORY', hint: 'Ability to remember things' },
    { word: 'CHALLENGE', hint: 'A difficult task' },
    { word: 'TWINKLE', hint: 'Your AI companion\'s name' },
    { word: 'ALPHA', hint: 'First letter of Greek alphabet' }
  ]

  const startNewRound = () => {
    const randomWord = words[Math.floor(Math.random() * words.length)]
    setCurrentWord(randomWord.word)
    setHint(randomWord.hint)
    setScrambledWord(randomWord.word.split('').sort(() => Math.random() - 0.5).join(''))
    setUserGuess('')
    setGameStarted(true)
  }

  const checkAnswer = () => {
    if (userGuess.toUpperCase() === currentWord) {
      setScore(score + 15)
      onScore(prev => prev + 15)
      alert('Correct! Well done! 🎉')
      startNewRound()
    } else {
      alert('Try again! Hint: ' + hint)
    }
  }

  return (
    <div className="text-center w-full max-w-full">
      {!gameStarted ? (
        <div>
          <h3 className="text-xl sm:text-2xl font-bold text-white mb-4">Word Puzzle Challenge</h3>
          <p className="text-purple-200 mb-6 text-sm sm:text-base">Unscramble the letters to form a word!</p>
          <Button onClick={startNewRound} className="bg-yellow-400 hover:bg-yellow-500 text-purple-900">
            Start Game
          </Button>
        </div>
      ) : (
        <div>
          <div className="mb-6">
            <h3 className="text-lg sm:text-xl text-white mb-2">Unscramble this word:</h3>
            <div className="text-2xl sm:text-4xl font-bold text-yellow-400 mb-4 tracking-wider break-all">
              {scrambledWord}
            </div>
            <p className="text-purple-200 text-sm sm:text-base">Hint: {hint}</p>
          </div>

          <div className="mb-6">
            <input
              type="text"
              value={userGuess}
              onChange={(e) => setUserGuess(e.target.value)}
              className="px-4 py-2 rounded-lg text-center text-base sm:text-lg font-bold uppercase bg-white text-purple-900 border-2 border-purple-300 w-full max-w-xs"
              placeholder="Your answer"
            />
          </div>

          <div className="flex flex-col sm:flex-row gap-2 sm:space-x-4 justify-center items-center">
            <Button onClick={checkAnswer} className="bg-green-500 hover:bg-green-600 text-white">
              Submit Answer
            </Button>
            <Button onClick={startNewRound} variant="outline" className="border-white text-white hover:bg-white hover:text-purple-900">
              New Word
            </Button>
          </div>

          <div className="mt-4 text-white text-sm sm:text-base">
            Score: {score}
          </div>
        </div>
      )}
    </div>
  )
}

// Number Sequence Game Component
const NumberSequenceGame = ({ onScore }) => {
  const [sequence, setSequence] = useState([])
  const [userSequence, setUserSequence] = useState([])
  const [showSequence, setShowSequence] = useState(false)
  const [gameStarted, setGameStarted] = useState(false)
  const [level, setLevel] = useState(1)

  const startGame = () => {
    const newSequence = Array.from({ length: 3 + level }, () => Math.floor(Math.random() * 9) + 1)
    setSequence(newSequence)
    setUserSequence([])
    setShowSequence(true)
    setGameStarted(true)

    setTimeout(() => {
      setShowSequence(false)
    }, 2000 + level * 500)
  }

  const addNumber = (number) => {
    if (showSequence) return
    
    const newUserSequence = [...userSequence, number]
    setUserSequence(newUserSequence)

    if (newUserSequence.length === sequence.length) {
      if (JSON.stringify(newUserSequence) === JSON.stringify(sequence)) {
        onScore(prev => prev + level * 5)
        setLevel(level + 1)
        alert(`Correct! Level ${level + 1}! 🎉`)
        setTimeout(startGame, 1000)
      } else {
        alert('Wrong sequence! Try again.')
        setUserSequence([])
      }
    }
  }

  return (
    <div className="text-center w-full max-w-full">
      {!gameStarted ? (
        <div>
          <h3 className="text-xl sm:text-2xl font-bold text-white mb-4">Number Sequence Challenge</h3>
          <p className="text-purple-200 mb-6 text-sm sm:text-base">Remember and repeat the number sequence!</p>
          <Button onClick={startGame} className="bg-yellow-400 hover:bg-yellow-500 text-purple-900">
            Start Game
          </Button>
        </div>
      ) : (
        <div>
          <div className="mb-6">
            <h3 className="text-lg sm:text-xl text-white mb-2">Level: {level}</h3>
            <div className="text-base sm:text-lg text-purple-200 mb-4">
              {showSequence ? 'Memorize this sequence:' : 'Repeat the sequence:'}
            </div>
            
            {showSequence && (
              <div className="text-2xl sm:text-4xl font-bold text-yellow-400 mb-4 break-all">
                {sequence.join(' - ')}
              </div>
            )}
          </div>

          {!showSequence && (
            <div>
              <div className="mb-6">
                <div className="text-lg sm:text-2xl text-white mb-4 break-all">
                  Your sequence: {userSequence.join(' - ')}
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2 sm:gap-4 max-w-xs mx-auto w-full">
                {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((number) => (
                  <Button
                    key={number}
                    onClick={() => addNumber(number)}
                    className="w-12 h-12 sm:w-16 sm:h-16 text-lg sm:text-xl bg-purple-600 hover:bg-purple-500 text-white"
                  >
                    {number}
                  </Button>
                ))}
              </div>

              <Button 
                onClick={() => setUserSequence([])} 
                variant="outline" 
                className="mt-4 border-white text-white hover:bg-white hover:text-purple-900"
              >
                Clear
              </Button>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

// Quick Math Game Component
const QuickMathGame = ({ onScore }) => {
  const [problem, setProblem] = useState('')
  const [answer, setAnswer] = useState(0)
  const [userAnswer, setUserAnswer] = useState('')
  const [timeLeft, setTimeLeft] = useState(30)
  const [gameActive, setGameActive] = useState(false)
  const [score, setScore] = useState(0)

  const generateProblem = () => {
    const num1 = Math.floor(Math.random() * 20) + 1
    const num2 = Math.floor(Math.random() * 20) + 1
    const operations = ['+', '-', '*']
    const operation = operations[Math.floor(Math.random() * operations.length)]
    
    let result
    switch (operation) {
      case '+':
        result = num1 + num2
        break
      case '-':
        result = Math.abs(num1 - num2)
        setProblem(`${Math.max(num1, num2)} - ${Math.min(num1, num2)}`)
        setAnswer(result)
        return
      case '*':
        result = num1 * num2
        break
      default:
        result = num1 + num2
    }
    
    setProblem(`${num1} ${operation} ${num2}`)
    setAnswer(result)
  }

  const startGame = () => {
    setGameActive(true)
    setScore(0)
    setTimeLeft(30)
    generateProblem()
    
    const timer = setInterval(() => {
      setTimeLeft(prev => {
        if (prev <= 1) {
          clearInterval(timer)
          setGameActive(false)
          return 0
        }
        return prev - 1
      })
    }, 1000)
  }

  const checkAnswer = () => {
    if (parseInt(userAnswer) === answer) {
      setScore(score + 5)
      onScore(prev => prev + 5)
      generateProblem()
      setUserAnswer('')
    } else {
      alert('Try again!')
    }
  }

  return (
    <div className="text-center w-full max-w-full">
      {!gameActive && timeLeft === 30 ? (
        <div>
          <h3 className="text-xl sm:text-2xl font-bold text-white mb-4">Quick Math Challenge</h3>
          <p className="text-purple-200 mb-6 text-sm sm:text-base">Solve as many problems as you can in 30 seconds!</p>
          <Button onClick={startGame} className="bg-yellow-400 hover:bg-yellow-500 text-purple-900">
            Start Game
          </Button>
        </div>
      ) : (
        <div>
          <div className="mb-6">
            <div className="flex flex-col sm:flex-row justify-between items-center mb-4 gap-2">
              <div className="text-white text-sm sm:text-base">Score: {score}</div>
              <div className="text-yellow-400 font-bold">
                <Clock className="w-5 h-5 inline mr-1" />
                <span className="text-sm sm:text-base">{timeLeft}s</span>
              </div>
            </div>
            
            {gameActive ? (
              <div>
                <div className="text-2xl sm:text-4xl font-bold text-white mb-4 break-all">
                  {problem} = ?
                </div>
                
                <div className="mb-4">
                  <input
                    type="number"
                    value={userAnswer}
                    onChange={(e) => setUserAnswer(e.target.value)}
                    className="px-4 py-2 rounded-lg text-center text-base sm:text-lg font-bold bg-white text-purple-900 border-2 border-purple-300 w-full max-w-xs"
                    placeholder="Answer"
                    onKeyPress={(e) => e.key === 'Enter' && checkAnswer()}
                  />
                </div>
                
                <Button onClick={checkAnswer} className="bg-green-500 hover:bg-green-600 text-white">
                  Submit
                </Button>
              </div>
            ) : (
              <div>
                <h3 className="text-xl sm:text-2xl font-bold text-yellow-400 mb-2">Time's Up! 🎉</h3>
                <p className="text-white mb-4 text-sm sm:text-base">Final Score: {score}</p>
                <Button onClick={startGame} className="bg-yellow-400 hover:bg-yellow-500 text-purple-900">
                  Play Again
                </Button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default GameHub

