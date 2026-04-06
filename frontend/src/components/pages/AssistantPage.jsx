import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../../api/axiosClient';
import ReactMarkdown from 'react-markdown';
import { toast } from 'react-hot-toast';
import { 
  MessageCircle, 
  Send, 
  Plus, 
  Trash2, 
  Bot, 
  User,
  Zap,
  Lock,
  ChevronLeft,
  Loader2
} from 'lucide-react';

const AssistantPage = () => {
  const navigate = useNavigate();
  const [conversations, setConversations] = useState([]);
  const [selectedConversation, setSelectedConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingConversations, setIsLoadingConversations] = useState(true);
  const [usageStats, setUsageStats] = useState(null);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const questionsSuggerees = [
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
      setIsLoadingConversations(true);
      const response = await axiosClient.get('/api/ai/conversations/');
      setConversations(response.data);
      
      // Sélectionne la conversation la plus récente si aucune n'est sélectionnée
      if (response.data.length > 0 && !selectedConversation) {
        selectConversation(response.data[0].id);
      }
    } catch (error) {
      console.error('Erreur chargement conversations:', error);
      toast.error('Erreur lors du chargement des conversations');
    } finally {
      setIsLoadingConversations(false);
    }
  };

  const loadUsageStats = async () => {
    try {
      const response = await axiosClient.get('/api/ai/usage-stats/');
      setUsageStats(response.data);
    } catch (error) {
      console.error('Erreur chargement stats:', error);
    }
  };

  const createNewConversation = async () => {
    try {
      const response = await axiosClient.post('/api/ai/conversations/');
      const newConv = response.data;
      setConversations([newConv, ...conversations]);
      setSelectedConversation(newConv);
      setMessages([]);
      setNewMessage('');
      inputRef.current?.focus();
    } catch (error) {
      console.error('Erreur création conversation:', error);
      toast.error('Erreur lors de la création de la conversation');
    }
  };

  const selectConversation = async (convId) => {
    try {
      setSelectedConversation(convId);
      const response = await axiosClient.get(`/api/ai/conversations/${convId}/messages/`);
      setMessages(response.data);
    } catch (error) {
      console.error('Erreur chargement messages:', error);
      toast.error('Erreur lors du chargement des messages');
    }
  };

  const deleteConversation = async (convId, event) => {
    event.stopPropagation();
    
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette conversation ?')) {
      return;
    }

    try {
      await axiosClient.delete(`/api/ai/conversations/${convId}/supprimer/`);
      setConversations(conversations.filter(c => c.id !== convId));
      
      if (selectedConversation === convId) {
        setSelectedConversation(null);
        setMessages([]);
      }
      
      toast.success('Conversation supprimée');
    } catch (error) {
      console.error('Erreur suppression conversation:', error);
      toast.error('Erreur lors de la suppression');
    }
  };

  const sendMessage = async (messageText = null) => {
    const textToSend = messageText || newMessage.trim();
    if (!textToSend || !selectedConversation) return;

    // Ajoute le message utilisateur immédiatement
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: textToSend,
      created_at: new Date().toISOString()
    };
    setMessages(prev => [...prev, userMessage]);
    
    if (!messageText) {
      setNewMessage('');
    }

    setIsLoading(true);

    try {
      const response = await axiosClient.post(
        `/api/ai/conversations/${selectedConversation}/messages/`,
        { message: textToSend }
      );

      // Ajoute la réponse de l'assistant
      const assistantMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.data.content,
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, assistantMessage]);

      // Met à jour le titre de la conversation dans la liste
      if (response.data.limited) {
        toast.error(response.data.content);
      }

      // Recharge les conversations pour mettre à jour les titres
      loadConversations();
      loadUsageStats();
      
    } catch (error) {
      console.error('Erreur envoi message:', error);
      toast.error('Erreur lors de l\'envoi du message');
      
      // Retire le message utilisateur en cas d'erreur
      setMessages(prev => prev.slice(0, -1));
    } finally {
      setIsLoading(false);
      inputRef.current?.focus();
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const handleQuestionSuggeree = (question) => {
    if (!selectedConversation) {
      createNewConversation().then(() => {
        setTimeout(() => sendMessage(question), 100);
      });
    } else {
      sendMessage(question);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'À l\'instant';
    if (diffInHours < 24) return `Il y a ${diffInHours}h`;
    if (diffInHours < 48) return 'Hier';
    return date.toLocaleDateString('fr-FR', { day: 'numeric', month: 'short' });
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Sidebar */}
      <div className={`${sidebarOpen ? 'w-80' : 'w-0'} transition-all duration-300 bg-white border-r border-gray-200 flex flex-col`}>
        {/* Header sidebar */}
        <div className="p-4 border-b border-gray-200">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Bot className="w-6 h-6 text-violet-600" />
              <h2 className="text-lg font-semibold text-gray-900">AI Assistant</h2>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden p-2 hover:bg-gray-100 rounded-lg"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
          </div>
          
          <button
            onClick={createNewConversation}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 transition-colors"
          >
            <Plus className="w-4 h-4" />
            Nouvelle conversation
          </button>
        </div>

        {/* Usage stats */}
        {usageStats && (
          <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">
                {usageStats.messages_aujourdhui}/{usageStats.limite_journaliere} aujourd'hui
              </span>
              {usageStats.limite_journaliere === 5 && (
                <button
                  onClick={() => navigate('/pricing')}
                  className="text-violet-600 hover:text-violet-700 font-medium flex items-center gap-1"
                >
                  <Lock className="w-3 h-3" />
                  Pro
                </button>
              )}
            </div>
            <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
              <div 
                className="bg-violet-600 h-2 rounded-full transition-all"
                style={{ width: `${(usageStats.messages_aujourdhui / usageStats.limite_journaliere) * 100}%` }}
              />
            </div>
          </div>
        )}

        {/* Conversations list */}
        <div className="flex-1 overflow-y-auto">
          {isLoadingConversations ? (
            <div className="p-4 text-center text-gray-500">
              <Loader2 className="w-6 h-6 animate-spin mx-auto mb-2" />
              Chargement...
            </div>
          ) : conversations.length === 0 ? (
            <div className="p-4 text-center text-gray-500">
              Aucune conversation
            </div>
          ) : (
            <div className="divide-y divide-gray-100">
              {conversations.map(conv => (
                <div
                  key={conv.id}
                  onClick={() => selectConversation(conv.id)}
                  className={`p-4 hover:bg-gray-50 cursor-pointer transition-colors ${
                    selectedConversation === conv.id ? 'bg-violet-50 border-l-4 border-violet-600' : ''
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1 min-w-0">
                      <h3 className="font-medium text-gray-900 truncate">
                        {conv.titre}
                      </h3>
                      {conv.dernier_message && (
                        <p className="text-sm text-gray-500 truncate mt-1">
                          {conv.dernier_message}
                        </p>
                      )}
                      <p className="text-xs text-gray-400 mt-1">
                        {formatDate(conv.updated_at)}
                      </p>
                    </div>
                    <button
                      onClick={(e) => deleteConversation(conv.id, e)}
                      className="p-1 hover:bg-gray-200 rounded opacity-0 group-hover:opacity-100 transition-opacity"
                    >
                      <Trash2 className="w-4 h-4 text-gray-400" />
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Main chat area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {!sidebarOpen && (
                <button
                  onClick={() => setSidebarOpen(true)}
                  className="p-2 hover:bg-gray-100 rounded-lg"
                >
                  <ChevronLeft className="w-5 h-5" />
                </button>
              )}
              <div className="flex items-center gap-2">
                <MessageCircle className="w-5 h-5 text-violet-600" />
                <h1 className="text-xl font-semibold text-gray-900">
                  {selectedConversation 
                    ? conversations.find(c => c.id === selectedConversation)?.titre || 'Conversation'
                    : 'AI Assistant'
                  }
                </h1>
              </div>
            </div>
            
            {usageStats && usageStats.limite_journaliere === 5 && (
              <div className="flex items-center gap-2 text-sm text-amber-600 bg-amber-50 px-3 py-1 rounded-full">
                <Lock className="w-3 h-3" />
                {usageStats.messages_restants} messages restants
              </div>
            )}
          </div>
        </div>

        {/* Messages area */}
        <div className="flex-1 overflow-y-auto px-6 py-4">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-gray-500">
              <Bot className="w-12 h-12 mb-4 text-gray-300" />
              <h3 className="text-lg font-medium mb-2">Bienvenue sur AI Assistant</h3>
              <p className="text-center mb-6 max-w-md">
                Je suis votre expert automobile personnel. Posez-moi vos questions sur le marché, 
                les prix, ou demandez des conseils d'achat.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 w-full max-w-2xl">
                {questionsSuggerees.map((question, index) => (
                  <button
                    key={index}
                    onClick={() => handleQuestionSuggeree(question)}
                    className="text-left p-3 bg-white border border-gray-200 rounded-lg hover:border-violet-300 hover:bg-violet-50 transition-colors"
                  >
                    <span className="text-sm">{question}</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="space-y-4">
              {messages.map((message) => (
                <div
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div
                    className={`max-w-2xl ${
                      message.role === 'user'
                        ? 'bg-violet-600 text-white'
                        : 'bg-white border border-gray-200 text-gray-900'
                    } rounded-lg px-4 py-3 shadow-sm`}
                  >
                    <div className="flex items-start gap-3">
                      <div className={`w-6 h-6 rounded-full flex items-center justify-center flex-shrink-0 ${
                        message.role === 'user' ? 'bg-violet-700' : 'bg-gray-100'
                      }`}>
                        {message.role === 'user' ? (
                          <User className="w-4 h-4 text-white" />
                        ) : (
                          <Bot className="w-4 h-4 text-violet-600" />
                        )}
                      </div>
                      <div className="flex-1">
                        <div className="prose prose-sm max-w-none">
                          {message.role === 'assistant' ? (
                            <ReactMarkdown>{message.content}</ReactMarkdown>
                          ) : (
                            <p className="whitespace-pre-wrap">{message.content}</p>
                          )}
                        </div>
                        <p className={`text-xs mt-2 ${
                          message.role === 'user' ? 'text-violet-200' : 'text-gray-400'
                        }`}>
                          {formatDate(message.created_at)}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-white border border-gray-200 rounded-lg px-4 py-3 shadow-sm">
                    <div className="flex items-center gap-2">
                      <Loader2 className="w-4 h-4 animate-spin text-violet-600" />
                      <span className="text-gray-500">L'assistant réfléchit...</span>
                    </div>
                  </div>
                </div>
              )}
              
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input area */}
        <div className="bg-white border-t border-gray-200 px-6 py-4">
          <div className="flex items-center gap-3">
            <input
              ref={inputRef}
              type="text"
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder={
                usageStats && usageStats.messages_restants === 0 && usageStats.limite_journaliere === 5
                  ? "Limite atteinte. Passez au plan Pro pour continuer."
                  : "Posez votre question..."
              }
              disabled={isLoading || (usageStats && usageStats.messages_restants === 0 && usageStats.limite_journaliere === 5)}
              className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent disabled:bg-gray-100 disabled:text-gray-500"
            />
            <button
              onClick={() => sendMessage()}
              disabled={isLoading || !newMessage.trim() || !selectedConversation || (usageStats && usageStats.messages_restants === 0 && usageStats.limite_journaliere === 5)}
              className="px-4 py-2 bg-violet-600 text-white rounded-lg hover:bg-violet-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Send className="w-4 h-4" />
              )}
              Envoyer
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AssistantPage;
