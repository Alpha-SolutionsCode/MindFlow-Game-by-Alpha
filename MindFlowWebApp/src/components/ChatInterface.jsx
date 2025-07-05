import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Input } from '@/components/ui/input.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Send, Sparkles, MessageCircle, Bot, User } from 'lucide-react'
import ApiService from '../services/api.js'

const ChatInterface = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'twinkle',
      text: "Salam! Main Twinkle hoon, tumhari AI dost! Kya haal hai? Koi puzzle solve karna hai ya phir gossip karna hai? 😊",
      timestamp: new Date()
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  // Real AI responses using API
  const getAIResponse = async (userMessage) => {
    setIsTyping(true)
    
    try {
      const response = await ApiService.sendChatMessage(userMessage, 'Player', 1, '')
      setIsTyping(false)
      return response.response
    } catch (error) {
      console.error('AI response error:', error)
      setIsTyping(false)
      return "Sorry, main thora busy hoon! Try again! 😊"
    }
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return

    const userMessage = {
      id: messages.length + 1,
      sender: 'user',
      text: inputMessage,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')

    // Get AI response
    const aiResponse = await getAIResponse(inputMessage)
    
    const twinkleMessage = {
      id: messages.length + 2,
      sender: 'twinkle',
      text: aiResponse,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, twinkleMessage])
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-2 sm:p-4 overflow-hidden">
      <Card className="w-full max-w-2xl h-[90vh] sm:h-[600px] lg:h-[700px] bg-white/95 backdrop-blur-lg border-purple-200 shadow-2xl overflow-hidden">
        <CardHeader className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-t-lg p-4 sm:p-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 sm:w-10 sm:h-10 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full flex items-center justify-center flex-shrink-0">
                <Sparkles className="w-4 h-4 sm:w-5 sm:h-5 text-purple-900" />
              </div>
              <div>
                <CardTitle className="text-lg sm:text-xl font-bold">Twinkle</CardTitle>
                <p className="text-purple-100 text-xs sm:text-sm">Your AI Companion</p>
              </div>
            </div>
            <div className="flex items-center space-x-2 sm:space-x-3">
              <Badge variant="secondary" className="bg-green-500 text-white text-xs sm:text-sm px-2 py-1">
                <div className="w-2 h-2 bg-white rounded-full mr-1 animate-pulse"></div>
                <span>Online</span>
              </Badge>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={onClose}
                className="text-white hover:bg-white/20 p-2 rounded-lg transition-colors"
              >
                <span className="text-lg">✕</span>
              </Button>
            </div>
          </div>
        </CardHeader>

        <CardContent className="p-0 h-[calc(90vh-140px)] sm:h-[calc(600px-140px)] lg:h-[calc(700px-140px)] flex flex-col overflow-hidden">
          <ScrollArea className="flex-1 p-3 sm:p-4 overflow-hidden">
            <div className="space-y-3 sm:space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`flex items-start space-x-2 max-w-[85%] sm:max-w-[80%] ${
                    message.sender === 'user' ? 'flex-row-reverse space-x-reverse' : ''
                  }`}>
                    <div className={`w-7 h-7 sm:w-8 sm:h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.sender === 'user' 
                        ? 'bg-gradient-to-r from-purple-600 to-indigo-600' 
                        : 'bg-gradient-to-r from-yellow-400 to-orange-400'
                    }`}>
                      {message.sender === 'user' ? (
                        <User className="w-3 h-3 sm:w-4 sm:h-4 text-white" />
                      ) : (
                        <Bot className="w-3 h-3 sm:w-4 sm:h-4 text-purple-900" />
                      )}
                    </div>
                    <div className={`rounded-2xl px-3 py-2 sm:px-4 max-w-full ${
                      message.sender === 'user'
                        ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white'
                        : 'bg-gray-100 text-gray-800'
                    }`}>
                      <p className="text-xs sm:text-sm break-words leading-relaxed">{message.text}</p>
                      <p className={`text-xs mt-1 ${
                        message.sender === 'user' ? 'text-purple-200' : 'text-gray-500'
                      }`}>
                        {message.timestamp.toLocaleTimeString([], { 
                          hour: '2-digit', 
                          minute: '2-digit' 
                        })}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
              
              {isTyping && (
                <div className="flex justify-start">
                  <div className="flex items-start space-x-2">
                    <div className="w-7 h-7 sm:w-8 sm:h-8 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full flex items-center justify-center flex-shrink-0">
                      <Bot className="w-3 h-3 sm:w-4 sm:h-4 text-purple-900" />
                    </div>
                    <div className="bg-gray-100 rounded-2xl px-3 py-2 sm:px-4">
                      <div className="flex space-x-1">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          </ScrollArea>

          <div className="border-t border-gray-200 p-3 sm:p-4">
            <div className="flex space-x-2 sm:space-x-3">
              <Input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Twinkle se baat karo... (Type your message)"
                className="flex-1 border-purple-200 focus:border-purple-400 text-sm sm:text-base rounded-lg"
                disabled={isTyping}
              />
              <Button 
                onClick={handleSendMessage}
                disabled={!inputMessage.trim() || isTyping}
                className="bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white flex-shrink-0 px-3 sm:px-4 rounded-lg transition-all duration-200 hover:scale-105"
              >
                <Send className="w-4 h-4" />
              </Button>
            </div>
            <p className="text-xs text-gray-500 mt-2 text-center break-words">
              Press Enter to send • Twinkle responds in Roman Urdu
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default ChatInterface

