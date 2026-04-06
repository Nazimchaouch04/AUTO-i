import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axios';
import ReactMarkdown from 'react-markdown';
import { useAuth } from '../contexts/AuthContext';
import { showToast } from '../components/Toast';

const AssistantPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);
  
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [usageStats, setUsageStats] = useState(null);
  const [showConversationList, setShowConversationList] = useState(true);

  const suggestedMessages = [
    "Est-ce qu'une Clio 2019 à 12 000€ est une bonne affaire ?",
    "Quelle voiture me conseilles-tu pour moins de 800 000 DA ?",
    "Comment évolue le prix des SUV en Algérie ?",
    "Explique-moi comment fonctionne l'estimation ML"
  ];

  useEffect(() => {
    loadConversations();
    loadUsageStats();
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const loadConversations = async () => {
    try {
      const response = await axiosClient.get('/api/ai/conversations/');
      setConversations(response.data);
    } catch (error) {
      console.error('Erreur chargement conversations:', error);
    }
  };

  const loadUsageStats = async () => {
    try {
      const response = await axiosClient.get('/api/ai/usage-stats/');
      setUsageStats(response.data);
    } catch (error) {
      console.error('Erreur chargement stats usage:', error);
    }
  };

  const createNewConversation = async () => {
    try {
      const response = await axiosClient.post('/api/ai/conversations/');
      const newConv = response.data;
      setConversations([newConv, ...conversations]);
      setCurrentConversation(newConv);
      setMessages([]);
      setShowConversationList(false);
    } catch (error) {
      showToast({ message: 'Erreur création conversation', type: 'error' });
    }
  };

  const loadConversation = async (convId) => {
    try {
      setIsLoading(true);
      const response = await axiosClient.get(`/api/ai/conversations/${convId}/messages/`);
      setMessages(response.data);
      setCurrentConversation(conversations.find(c => c.id === convId));
      setShowConversationList(false);
    } catch (error) {
      showToast({ message: 'Erreur chargement conversation', type: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async (messageText = null) => {
    const textToSend = messageText || newMessage.trim();
    if (!textToSend) return;

    // Si pas de conversation, en créer une
    let convId = currentConversation?.id;
    if (!convId) {
      await createNewConversation();
      // Attendre un peu pour que la conversation soit créée
      setTimeout(() => {
        sendMessage(textToSend);
      }, 500);
      return;
    }

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

      const response = await axiosClient.post(`/api/ai/conversations/${convId}/messages/`, {
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
        
        // Mettre à jour les stats d'usage
        loadUsageStats();
        
        // Mettre à jour la liste des conversations
        loadConversations();
      }
    } catch (error) {
      showToast({ message: 'Erreur envoi message', type: 'error' });
    } finally {
      setIsLoading(false);
    }
  };

  const deleteConversation = async (convId) => {
    if (!confirm('Supprimer cette conversation ?')) return;
    
    try {
      await axiosClient.delete(`/api/ai/conversations/${convId}/supprimer/`);
      setConversations(conversations.filter(c => c.id !== convId));
      if (currentConversation?.id === convId) {
        setCurrentConversation(null);
        setMessages([]);
        setShowConversationList(true);
      }
      showToast({ message: 'Conversation supprimée', type: 'success' });
    } catch (error) {
      showToast({ message: 'Erreur suppression', type: 'error' });
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Colonne gauche - Liste des conversations */}
      <div className={`${showConversationList ? 'w-80' : 'w-0'} transition-all duration-300 bg-white border-r border-gray-200 overflow-hidden flex flex-col`}>
        <div className="p-4 border-b border-gray-200">
          <button
            onClick={createNewConversation}
            className="w-full bg-violet-600 text-white px-4 py-2 rounded-lg hover:bg-violet-700 transition-colors flex items-center justify-center gap-2"
          >
            <span>+</span> Nouvelle conversation
          </button>
          
          {/* Stats d'utilisation */}
          {usageStats && (
            <div className="mt-3 p-3 bg-gray-50 rounded-lg text-sm">
              <div className="flex justify-between items-center">
                <span className="text-gray-600">Messages aujourd'hui:</span>
                <span className="font-medium">
                  {usageStats.messages_aujourdhui}/{usageStats.limite_journaliere}
                </span>
              </div>
              {usageStats.messages_restants <= 1 && usageStats.limite_journaliere <= 5 && (
                <button
                  onClick={() => navigate('/subscriptions')}
                  className="mt-2 text-xs text-violet-600 hover:text-violet-700 underline"
                >
                  Passer au Pro pour messages illimités
                </button>
              )}
            </div>
          )}
        </div>
        
        <div className="flex-1 overflow-y-auto">
          {conversations.length === 0 ? (
            <div className="p-4 text-center text-gray-500 text-sm">
              Aucune conversation
            </div>
          ) : (
            conversations.map(conv => (
              <div
                key={conv.id}
                className={`p-4 border-b border-gray-100 cursor-pointer hover:bg-gray-50 transition-colors ${currentConversation?.id === conv.id ? 'bg-violet-50' : ''}`}
                onClick={() => loadConversation(conv.id)}
              >
                <div className="flex justify-between items-start">
                  <div className="flex-1 min-w-0">
                    <h3 className="font-medium text-gray-900 truncate">{conv.titre}</h3>
                    <p className="text-sm text-gray-500 truncate mt-1">{conv.dernier_message}</p>
                    <p className="text-xs text-gray-400 mt-1">
                      {new Date(conv.updated_at).toLocaleDateString('fr-FR', { 
                        hour: '2-digit', 
                        minute: '2-digit' 
                      })}
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      deleteConversation(conv.id);
                    }}
                    className="ml-2 text-gray-400 hover:text-red-500 transition-colors"
                  >
                    ×
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Colonne droite - Interface de chat */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowConversationList(!showConversationList)}
              className="text-gray-500 hover:text-gray-700 transition-colors"
            >
              ☰
            </button>
            <h1 className="text-xl font-semibold text-gray-900">
              AutoIntel AI Assistant
            </h1>
          </div>
          {currentConversation && (
            <span className="text-sm text-gray-500">{currentConversation.titre}</span>
          )}
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && !isLoading && (
            <div className="text-center py-8">
              <div className="text-4xl mb-4">🤖</div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                Bonjour ! Je suis votre assistant AutoIntel
              </h2>
              <p className="text-gray-600 mb-6">
                Posez-moi vos questions sur le marché automobile, les prix, les tendances...
              </p>
              
              {/* Messages suggérés */}
              <div className="max-w-2xl mx-auto space-y-2">
                {suggestedMessages.map((msg, index) => (
                  <button
                    key={index}
                    onClick={() => sendMessage(msg)}
                    className="w-full text-left p-3 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors text-gray-700"
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
                className={`max-w-2xl px-4 py-3 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-violet-600 text-white'
                    : 'bg-gray-800 text-white'
                }`}
              >
                {message.role === 'assistant' ? (
                  <ReactMarkdown className="prose prose-invert max-w-none">
                    {message.content}
                  </ReactMarkdown>
                ) : (
                  <p>{message.content}</p>
                )}
                <p className="text-xs opacity-70 mt-2">
                  {new Date(message.created_at).toLocaleTimeString('fr-FR', {
                    hour: '2-digit',
                    minute: '2-digit'
                  })}
                </p>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-800 text-white px-4 py-3 rounded-lg">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        {/* Input */}
        <div className="bg-white border-t border-gray-200 p-4">
          <div className="flex gap-3">
            <input
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Tapez votre message..."
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500"
              disabled={isLoading}
            />
            <button
              onClick={() => sendMessage()}
              disabled={isLoading || !newMessage.trim()}
              className="bg-violet-600 text-white px-6 py-2 rounded-lg hover:bg-violet-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? '...' : 'Envoyer'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AssistantPage;
