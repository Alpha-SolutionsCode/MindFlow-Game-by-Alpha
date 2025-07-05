import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Star, Brain, Sparkles, MessageCircle, Trophy, Users, Zap, Gamepad2 } from 'lucide-react'
import mindflowLogo from './assets/mindflow.png'
import ChatInterface from './components/ChatInterface.jsx'
import GameHub from './components/GameHub.jsx'
import './App.css'

function App() {
  const [activeFeature, setActiveFeature] = useState(0)
  const [isVisible, setIsVisible] = useState(false)
  const [isChatOpen, setIsChatOpen] = useState(false)
  const [currentView, setCurrentView] = useState('home') // 'home', 'games'

  const features = [
    {
      icon: <Brain className="w-6 h-6 sm:w-8 sm:h-8" />,
      title: "AI-Powered Learning",
      description: "Experience personalized learning with Twinkle, your AI companion"
    },
    {
      icon: <MessageCircle className="w-6 h-6 sm:w-8 sm:h-8" />,
      title: "Interactive Chat",
      description: "Chat with Twinkle for a culturally relatable experience"
    },
    {
      icon: <Gamepad2 className="w-6 h-6 sm:w-8 sm:h-8" />,
      title: "Alpha Games",
      description: "Play engaging mini-games with Twinkle as your guide"
    },
    {
      icon: <Trophy className="w-6 h-6 sm:w-8 sm:h-8" />,
      title: "Memory Challenges",
      description: "Test your memory with engaging puzzles and brain teasers"
    }
  ]

  useEffect(() => {
    setIsVisible(true)
    const interval = setInterval(() => {
      setActiveFeature((prev) => (prev + 1) % features.length)
    }, 3000)
    return () => clearInterval(interval)
  }, [])

  // Render Games View
  if (currentView === 'games') {
    return <GameHub onBack={() => setCurrentView('home')} />
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 via-purple-800 to-indigo-900 overflow-x-hidden">
      {/* Header */}
      <header className="w-full px-4 py-4 sm:py-6">
        <nav className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-2 sm:space-x-3">
            <img 
              src={mindflowLogo} 
              alt="MindFlow Logo" 
              className="w-10 h-10 sm:w-12 sm:h-12 rounded-lg shadow-lg flex-shrink-0"
            />
            <h1 className="text-xl sm:text-2xl font-bold text-white">MindFlow</h1>
          </div>
          {/* Desktop Nav */}
          <div className="hidden md:flex space-x-4 lg:space-x-6">
            <button 
              onClick={() => setCurrentView('home')}
              className={`px-3 py-2 rounded-lg transition-all duration-200 font-medium ${
                currentView === 'home' 
                  ? 'bg-yellow-400 text-purple-900 shadow-lg' 
                  : 'text-white hover:bg-white/10 hover:text-yellow-300'
              }`}
            >
              Home
            </button>
            <button 
              onClick={() => setCurrentView('games')}
              className={`px-3 py-2 rounded-lg transition-all duration-200 font-medium ${
                currentView === 'games' 
                  ? 'bg-yellow-400 text-purple-900 shadow-lg' 
                  : 'text-white hover:bg-white/10 hover:text-yellow-300'
              }`}
            >
              Games
            </button>
            <button 
              onClick={() => setIsChatOpen(true)}
              className="px-4 py-2 bg-gradient-to-r from-yellow-400 to-orange-400 text-purple-900 font-medium rounded-lg hover:from-yellow-500 hover:to-orange-500 transition-all duration-200 flex items-center space-x-2 shadow-lg hover:shadow-xl"
            >
              <MessageCircle className="w-4 h-4" />
              <span>Chat with Twinkle</span>
            </button>
          </div>
          {/* Mobile Nav */}
          <div className="md:hidden flex items-center space-x-2">
            <button 
              onClick={() => setCurrentView('games')}
              className="px-3 py-2 bg-yellow-400 text-purple-900 font-medium rounded-lg text-sm"
            >
              Games
            </button>
            <button 
              onClick={() => setIsChatOpen(true)} 
              className="p-2 bg-yellow-400 text-purple-900 rounded-lg hover:bg-yellow-500 transition-colors"
            >
              <MessageCircle className="w-5 h-5" />
            </button>
          </div>
        </nav>
      </header>

      {/* Hero Section */}
      <section className="w-full px-4 py-8 sm:py-12 lg:py-16 text-center">
        <div className={`max-w-6xl mx-auto transition-all duration-1000 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-10'}`}>
          <div className="flex justify-center mb-6 sm:mb-8">
            <div className="relative">
              <img 
                src={mindflowLogo} 
                alt="MindFlow" 
                className="w-24 h-24 sm:w-32 sm:h-32 lg:w-40 lg:h-40 mx-auto rounded-2xl shadow-2xl animate-pulse"
              />
              <div className="absolute -top-1 -right-1 sm:-top-2 sm:-right-2">
                <Star className="w-6 h-6 sm:w-8 sm:h-8 text-yellow-400 animate-bounce" />
              </div>
            </div>
          </div>
          
          <h2 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold text-white mb-4 sm:mb-6 leading-tight">
            Welcome to <span className="text-yellow-400">MindFlow</span>
          </h2>
          
          <p className="text-base sm:text-lg md:text-xl lg:text-2xl text-purple-200 mb-6 sm:mb-8 max-w-4xl mx-auto px-4 leading-relaxed">
            Meet Twinkle, your Roman Urdu AI companion! Experience fun, witty, and brainy conversations 
            while challenging your mind with engaging puzzles and memory games.
          </p>
          
          <div className="flex flex-col sm:flex-row gap-3 sm:gap-4 justify-center items-center px-4">
            <Button 
              size="lg" 
              onClick={() => setCurrentView('games')}
              className="w-full sm:w-auto bg-gradient-to-r from-yellow-400 to-orange-400 hover:from-yellow-500 hover:to-orange-500 text-purple-900 font-bold px-6 sm:px-8 py-3 sm:py-4 text-base sm:text-lg rounded-xl shadow-lg transform hover:scale-105 transition-all duration-200"
            >
              <Sparkles className="w-5 h-5 mr-2" />
              Start Playing
            </Button>
            <Button 
              variant="outline" 
              size="lg" 
              onClick={() => setIsChatOpen(true)}
              className="w-full sm:w-auto border-2 border-white text-white bg-white/10 hover:bg-white hover:text-purple-900 px-6 sm:px-8 py-3 sm:py-4 text-base sm:text-lg rounded-xl backdrop-blur-sm transition-all duration-200"
            >
              <MessageCircle className="w-5 h-5 mr-2" />
              Chat with Twinkle
            </Button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="w-full px-4 py-8 sm:py-12 lg:py-16">
        <div className="max-w-7xl mx-auto">
          <h3 className="text-2xl sm:text-3xl md:text-4xl font-bold text-center text-white mb-8 sm:mb-12">
            Amazing Features
          </h3>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
            {features.map((feature, index) => (
              <Card 
                key={index}
                className={`bg-white/10 backdrop-blur-lg border-white/20 text-white transition-all duration-500 hover:scale-105 cursor-pointer ${
                  activeFeature === index ? 'ring-2 ring-yellow-400 bg-white/20 shadow-xl' : 'hover:shadow-lg'
                }`}
                onClick={() => setActiveFeature(index)}
              >
                <CardHeader className="text-center p-4 sm:p-6">
                  <div className="flex justify-center mb-3 sm:mb-4 text-yellow-400">
                    {feature.icon}
                  </div>
                  <CardTitle className="text-lg sm:text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent className="p-4 sm:p-6 pt-0">
                  <CardDescription className="text-purple-200 text-center text-sm sm:text-base">
                    {feature.description}
                  </CardDescription>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Twinkle Section */}
      <section className="w-full px-4 py-8 sm:py-12 lg:py-16">
        <div className="max-w-6xl mx-auto">
          <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-6 sm:p-8 lg:p-12 border border-white/20">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 sm:gap-8 items-center">
              <div>
                <Badge className="bg-gradient-to-r from-yellow-400 to-orange-400 text-purple-900 mb-4 font-medium">
                  <Sparkles className="w-4 h-4 mr-1" />
                  Meet Twinkle
                </Badge>
                <h3 className="text-2xl sm:text-3xl md:text-4xl font-bold text-white mb-4 sm:mb-6">
                  Alpha Game
                </h3>
                <p className="text-purple-200 text-base sm:text-lg mb-6 leading-relaxed">
                  Twinkle speaks Roman Urdu and brings a local, culturally relatable experience. 
                  She's witty, supportive, and ready to help you with puzzles, gossip, and brain challenges!
                </p>
                <div className="space-y-3 sm:space-y-4">
                  <div className="flex items-center space-x-3">
                    <Zap className="w-5 h-5 text-yellow-400 flex-shrink-0" />
                    <span className="text-white text-sm sm:text-base">Friendly Roman Urdu conversations</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <Brain className="w-5 h-5 text-yellow-400 flex-shrink-0" />
                    <span className="text-white text-sm sm:text-base">Smart puzzle assistance</span>
                  </div>
                  <div className="flex items-center space-x-3">
                    <MessageCircle className="w-5 h-5 text-yellow-400 flex-shrink-0" />
                    <span className="text-white text-sm sm:text-base">Cultural gossip and fun facts</span>
                  </div>
                </div>
              </div>
              <div className="text-center">
                <div className="bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full w-32 h-32 sm:w-48 sm:h-48 lg:w-64 lg:h-64 mx-auto flex items-center justify-center shadow-2xl">
                  <div className="text-4xl sm:text-6xl">🌟</div>
                </div>
                <p className="text-yellow-400 text-lg sm:text-xl font-bold mt-4">Twinkle</p>
                <p className="text-purple-200 text-sm sm:text-base">Your AI Companion</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="w-full px-4 py-8 sm:py-12 lg:py-16">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-6 lg:gap-8 text-center">
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 sm:p-8 border border-white/20">
              <div className="text-2xl sm:text-3xl md:text-4xl font-bold text-yellow-400 mb-2">10K+</div>
              <div className="text-white text-sm sm:text-base">Active Users</div>
            </div>
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 sm:p-8 border border-white/20">
              <div className="text-2xl sm:text-3xl md:text-4xl font-bold text-yellow-400 mb-2">50K+</div>
              <div className="text-white text-sm sm:text-base">Puzzles Solved</div>
            </div>
            <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-6 sm:p-8 border border-white/20 sm:col-span-2 md:col-span-1">
              <div className="text-2xl sm:text-3xl md:text-4xl font-bold text-yellow-400 mb-2">95%</div>
              <div className="text-white text-sm sm:text-base">User Satisfaction</div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="w-full px-4 py-6 sm:py-8 border-t border-white/20">
        <div className="max-w-6xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="flex items-center space-x-2 sm:space-x-3">
              <img 
                src={mindflowLogo} 
                alt="MindFlow Logo" 
                className="w-8 h-8 rounded flex-shrink-0"
              />
              <span className="text-white font-bold text-sm sm:text-base">MindFlow</span>
            </div>
            <div className="text-purple-200 text-center md:text-right">
              <p className="mb-2 text-xs sm:text-sm">© 2025 MindFlow. All rights reserved.</p>
              <p className="text-xs break-words">
                Designed By <span className="text-yellow-400 font-semibold">Muhammad Mikran Sandhu</span> at{' '}
                <span className="text-yellow-400 font-semibold">Alpha Solutions</span>
              </p>
            </div>
          </div>
        </div>
      </footer>

      {/* Floating Chat Button */}
      {!isChatOpen && (
        <Button
          onClick={() => setIsChatOpen(true)}
          className="fixed bottom-4 right-4 sm:bottom-6 sm:right-6 w-14 h-14 sm:w-16 sm:h-16 rounded-full bg-gradient-to-r from-yellow-400 to-orange-400 hover:from-yellow-500 hover:to-orange-500 text-purple-900 shadow-2xl z-40 flex items-center justify-center transition-all duration-200 hover:scale-110"
        >
          <MessageCircle className="w-6 h-6 sm:w-7 sm:h-7" />
        </Button>
      )}

      {/* Chat Interface */}
      <ChatInterface 
        isOpen={isChatOpen} 
        onClose={() => setIsChatOpen(false)} 
      />
    </div>
  )
}

export default App

