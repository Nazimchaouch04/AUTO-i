import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../../api/axiosClient';
import ReactMarkdown from 'react-markdown';
import { useToast } from '../ui/Toast';

const AIFloatingButton = () => {
  const { showToast } = useToast();
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState(null);
  const [currentPage, setCurrentPage] = useState('');

  useEffect(() => {
    setCurrentPage(window.location.pathname);
  }, []);

  const getSuggestedMessages = () => {
    switch (currentPage) {
      case '/annonces':
        return [
          "Analyse cette annonce pour moi",
          "Est-ce un bon prix ?",
          "Quelles sont les alternatives ?"
        ];
      case '/estimation':
        return [
          "Explique ce résultat",
          "Comment améliorer cette estimation ?",
          "Quels facteurs influencent le prix ?"
        ];
      case '/dashboard':
        return [
          "Résume le marché du moment",
          "Quelles sont les tendances actuelles ?",
          "Y a-t-il des bonnes affaires ?"
        ];
      default:
        return [
          "Quelle voiture me conseilles-tu ?",
          "Comment évolue le marché ?",
          "Est-ce le bon moment pour acheter ?"
        ];
    }
  };

  const sendMessage = async (messageText = null) => {
    const textToSend = messageText || newMessage.trim();
    if (!textToSend) return;

    try {
      setIsLoading(true);
      
      // Ajouter le message utilisateur immédiatement
      const userMessage = {
        role: 'user',
        content: textToSend,
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, userMessage]);
      
      if (!messageText) {
        setNewMessage('');
      }

      // Utiliser l'endpoint message-rapide pour créer une conversation automatiquement
      const response = await axiosClient.post('/api/ai/message-rapide/', {
        message: textToSend
      });

      if (response.data.limited) {
        showToast({ message: response.data.content, type: 'warning' });
      } else {
        // Ajouter la réponse de l'assistant
        const assistantMessage = {
          role: 'assistant',
          content: response.data.content,
          created_at: new Date().toISOString()
        };
        setMessages(prev => [...prev, assistantMessage]);
        
        // Sauvegarder l'ID de conversation pour les futurs messages
        if (response.data.conversation_id) {
          setConversationId(response.data.conversation_id);
        }
      }
    } catch (error) {
      showToast({ message: 'Erreur envoi message', type: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const openFullAssistant = () => {
    setIsOpen(false);
    navigate('/assistant');
  };

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="fixed bottom-6 right-6 bg-violet-600 hover:bg-violet-700 text-white rounded-full p-4 shadow-lg transition-all duration-200 hover:scale-110 z-50 flex items-center gap-2"
      >
        <span className="text-xl">🤖</span>
        <span className="font-medium">Ask AI</span>
      </button>
    );
  }

  return (
    <div className="fixed bottom-6 right-6 w-96 max-h-[600px] bg-white rounded-lg shadow-2xl z-50 flex flex-col border border-gray-200">
      {/* Header */}
      <div className="bg-violet-600 text-white p-4 rounded-t-lg flex justify-between items-center">
        <div className="flex items-center gap-2">
          <span className="text-xl">🤖</span>
          <span className="font-medium">AutoIntel AI</span>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={openFullAssistant}
            className="text-white hover:text-violet-200 transition-colors text-sm"
            title="Ouvrir l'assistant complet"
          >
            ⛶
          </button>
          <button
            onClick={() => setIsOpen(false)}
            className="text-white hover:text-violet-200 transition-colors"
          >
            ×
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 max-h-96">
        {messages.length === 0 && !isLoading && (
          <div className="text-center py-4">
            <div className="text-2xl mb-2">🤖</div>
            <p className="text-gray-600 text-sm mb-3">
              Posez-moi vos questions sur l'automobile !
            </p>
            
            {/* Messages suggérés */}
            <div className="space-y-1">
              {getSuggestedMessages().map((msg, index) => (
                <button
                  key={index}
                  onClick={() => sendMessage(msg)}
                  className="w-full text-left p-2 bg-gray-100 hover:bg-gray-200 rounded text-sm transition-colors text-gray-700"
                >
                  💭 {msg}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] px-3 py-2 rounded-lg text-sm ${
                message.role === 'user'
                  ? 'bg-violet-600 text-white'
                  : 'bg-gray-100 text-gray-800'
              }`}
            >
              {message.role === 'assistant' ? (
                <ReactMarkdown className="prose prose-sm max-w-none">
                  {message.content}
                </ReactMarkdown>
              ) : (
                <p>{message.content}</p>
              )}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 text-gray-800 px-3 py-2 rounded-lg">
              <div className="flex space-x-1">
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-1.5 h-1.5 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input */}
      <div className="p-3 border-t border-gray-200">
        <div className="flex gap-2">
          <input
            type="text"
            value={newMessage}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Tapez votre message..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"
            disabled={isLoading}
          />
          <button
            onClick={() => sendMessage()}
            disabled={isLoading || !newMessage.trim()}
            className="bg-violet-600 text-white px-4 py-2 rounded-lg hover:bg-violet-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors text-sm"
          >
            {isLoading ? '...' : '→'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default AIFloatingButton;
