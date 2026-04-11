import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import axiosClient from '../api/axios';
import ReactMarkdown from 'react-markdown';
import { useSelector } from 'react-redux';

const AdvancedAssistantPage = () => {
  const navigate = useNavigate();
  const messagesEndRef = useRef(null);
  const { user } = useSelector((s) => s.user);
  
  const [conversations, setConversations] = useState([]);
  const [currentConversation, setCurrentConversation] = useState(null);
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [usageStats, setUsageStats] = useState(null);
  const [showConversationList, setShowConversationList] = useState(true);
  const [userProfile, setUserProfile] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [marketInsights, setMarketInsights] = useState([]);
  const [showRecommendations, setShowRecommendations] = useState(false);
  const [showMarketInsights, setShowMarketInsights] = useState(false);
  const [lastAnalysis, setLastAnalysis] = useState(null);

  const suggestedMessages = [
    "Je cherche un SUV familial avec budget 25000EUR",
    "Quelle est la tendance des prix des voitures électriques ?",
    "Recommande-moi un véhicule pour un usage quotidien",
    "Estime le prix d'une BMW Série 3 de 2020",
    "Compare une Toyota Corolla et une Honda Civic",
    "Quel est le meilleur moment pour acheter une voiture ?"
  ];

  const quickActions = [
    { icon: ' recommendations', label: 'Recommandations', action: () => loadRecommendations() },
    { icon: ' trend', label: 'Marché', action: () => loadMarketInsights() },
    { icon: ' profile', label: 'Profil IA', action: () => loadUserProfile() },
    { icon: ' prediction', label: 'Prédictions', action: () => setShowRecommendations(true) }
  ];

  useEffect(() => {
    loadConversations();
    loadUsageStats();
    loadUserProfile();
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

  const loadUserProfile = async () => {
    try {
      const response = await axiosClient.get('/api/ai/profil-ia/');
      setUserProfile(response.data);
    } catch (error) {
      console.error('Erreur chargement profil IA:', error);
    }
  };

  const loadRecommendations = async () => {
    try {
      setIsLoading(true);
      const response = await axiosClient.get('/api/ai/recommandations-vehicules/?limit=5');
      setRecommendations(response.data.recommandations);
      setShowRecommendations(true);
    } catch (error) {
      console.error('Erreur chargement recommandations:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const loadMarketInsights = async () => {
    try {
      setIsLoading(true);
      const response = await axiosClient.get('/api/ai/market-insights/');
      setMarketInsights(response.data.insights);
      setShowMarketInsights(true);
    } catch (error) {
      console.error('Erreur chargement market insights:', error);
    } finally {
      setIsLoading(false);
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
      alert('Erreur création conversation');
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
      alert('Erreur chargement conversation');
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = async (messageText = null) => {
    const textToSend = messageText || newMessage.trim();
    if (!textToSend) return;

    let convId = currentConversation?.id;
    if (!convId) {
      await createNewConversation();
      setTimeout(() => {
        sendMessage(textToSend);
      }, 500);
      return;
    }

    try {
      setIsLoading(true);
      
      const userMessage = {
        role: 'user',
        content: textToSend,
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, userMessage]);
      
      if (!messageText) {
        setNewMessage('');
      }

      // Utiliser l'endpoint de conversation intelligente
      const response = await axiosClient.post('/api/ai/conversation-intelligente/', {
        conversation_id: convId,
        message: textToSend
      });

      // Ajouter la réponse de l'assistant
      const assistantMessage = {
        role: 'assistant',
        content: response.data.reponse.texte,
        created_at: new Date().toISOString()
      };
      setMessages(prev => [...prev, assistantMessage]);
      
      // Mettre à jour l'analyse et recommandations
      setLastAnalysis(response.data.analyse);
      if (response.data.recommandations && response.data.recommandations.length > 0) {
        setRecommendations(response.data.recommandations);
        setShowRecommendations(true);
      }
      
      loadUsageStats();
      loadConversations();
    } catch (error) {
      console.error('Erreur envoi message:', error);
      alert('Erreur envoi message');
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
    } catch (error) {
      alert('Erreur suppression');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const updateProfile = async (profileData) => {
    try {
      await axiosClient.put('/api/ai/profil-ia/', profileData);
      loadUserProfile();
      alert('Profil mis à jour avec succès');
    } catch (error) {
      alert('Erreur mise à jour profil');
    }
  };

  const getInsightIcon = (type) => {
    const icons = {
      'tendance_prix': ' trend',
      'opportunite': ' opportunity',
      'alerte_marche': ' alert',
      'conseil_achat': ' advice',
      'conseil_vente': ' advice',
      'prediction': ' prediction'
    };
    return icons[type] || ' info';
  };

  const getInsightColor = (impact) => {
    if (impact >= 70) return 'text-red-600 bg-red-50';
    if (impact >= 40) return 'text-yellow-600 bg-yellow-50';
    return 'text-green-600 bg-green-50';
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Colonne gauche - Navigation */}
      <div className={`${showConversationList ? 'w-80' : 'w-0'} transition-all duration-300 bg-white border-r border-gray-200 overflow-hidden flex flex-col`}>
        <div className="p-4 border-b border-gray-200">
          <button
            onClick={createNewConversation}
            className="w-full bg-violet-600 text-white px-4 py-2 rounded-lg hover:bg-violet-700 transition-colors flex items-center justify-center gap-2"
          >
            <span>+</span> Nouvelle conversation
          </button>
          
          {/* Actions rapides */}
          <div className="mt-3 grid grid-cols-2 gap-2">
            {quickActions.map((action, index) => (
              <button
                key={index}
                onClick={action.action}
                className="p-2 bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors text-xs flex flex-col items-center"
              >
                <span className="text-lg mb-1">{action.icon}</span>
                <span>{action.label}</span>
              </button>
            ))}
          </div>
          
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
                  onClick={() => navigate('/abonnement')}
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

      {/* Colonne principale - Interface de chat */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white border-b border-gray-200 p-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowConversationList(!showConversationList)}
              className="text-gray-500 hover:text-gray-700 transition-colors"
            >
              <span className="text-xl">{'{'}</span>
            </button>
            <div>
              <h1 className="text-xl font-semibold text-gray-900">
                AutoIntel AI Assistant
              </h1>
              <p className="text-sm text-gray-500">Conversation intelligente avec recommandations</p>
            </div>
          </div>
          
          {/* Profil IA rapide */}
          {userProfile && (
            <div className="flex items-center gap-4">
              <div className="text-right">
                <div className="text-sm font-medium text-gray-900">
                  Score: {userProfile.scores.budget + userProfile.scores.ecologique + userProfile.scores.praticite}/300
                </div>
                <div className="text-xs text-gray-500">
                  Budget: {userProfile.scores.budget} | Éco: {userProfile.scores.ecologique} | Pratique: {userProfile.scores.praticite}
                </div>
              </div>
              <button
                onClick={() => setShowRecommendations(true)}
                className="bg-violet-100 text-violet-700 px-3 py-1 rounded-lg text-sm hover:bg-violet-200 transition-colors"
              >
                Voir profil
              </button>
            </div>
          )}
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 && !isLoading && (
            <div className="text-center py-8">
              <div className="text-6xl mb-4"> intelligence</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                Assistant IA AutoIntel Avancé
              </h2>
              <p className="text-gray-600 mb-6 max-w-2xl mx-auto">
                Je suis votre assistant intelligent spécialisé dans l'automobile. 
                Je peux analyser vos besoins, recommander des véhicules, prédire les prix et vous donner des conseils d'experts.
              </p>
              
              {/* Messages suggérés */}
              <div className="max-w-3xl mx-auto">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Questions suggérées:</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                  {suggestedMessages.map((msg, index) => (
                    <button
                      key={index}
                      onClick={() => sendMessage(msg)}
                      className="text-left p-4 bg-gradient-to-r from-violet-50 to-purple-50 hover:from-violet-100 hover:to-purple-100 rounded-lg transition-all duration-200 text-gray-700 border border-violet-200"
                    >
                      <span className="text-violet-600 mr-2"> intelligence</span>
                      {msg}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-3xl px-4 py-3 rounded-lg ${
                  message.role === 'user'
                    ? 'bg-violet-600 text-white'
                    : 'bg-gray-800 text-white'
                }`}
              >
                {message.role === 'assistant' ? (
                  <div>
                    <ReactMarkdown className="prose prose-invert max-w-none">
                      {message.content}
                    </ReactMarkdown>
                    
                    {/* Suggestions de suivi */}
                    {index === messages.length - 1 && lastAnalysis?.suggestions && (
                      <div className="mt-3 pt-3 border-t border-gray-600">
                        <p className="text-sm text-gray-300 mb-2">Suggestions:</p>
                        <div className="space-y-1">
                          {lastAnalysis.suggestions.map((suggestion, idx) => (
                            <button
                              key={idx}
                              onClick={() => sendMessage(suggestion)}
                              className="block w-full text-left p-2 bg-gray-700 hover:bg-gray-600 rounded text-sm text-gray-200"
                            >
                              {suggestion}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
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
                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-violet-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-sm">Analyse en cours...</span>
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
              placeholder="Décrivez vos besoins, posez une question..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-violet-500"
              disabled={isLoading}
            />
            <button
              onClick={() => sendMessage()}
              disabled={isLoading || !newMessage.trim()}
              className="bg-violet-600 text-white px-6 py-3 rounded-lg hover:bg-violet-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {isLoading ? '...' : 'Envoyer'}
            </button>
          </div>
        </div>
      </div>

      {/* Panneau latéral - Recommandations et Insights */}
      {(showRecommendations || showMarketInsights) && (
        <div className="w-96 bg-white border-l border-gray-200 overflow-hidden flex flex-col">
          <div className="p-4 border-b border-gray-200 flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900">
              {showRecommendations ? 'Recommandations' : 'Insights Marché'}
            </h2>
            <button
              onClick={() => {
                setShowRecommendations(false);
                setShowMarketInsights(false);
              }}
              className="text-gray-500 hover:text-gray-700"
            >
              ×
            </button>
          </div>

          <div className="flex-1 overflow-y-auto p-4">
            {showRecommendations && (
              <div className="space-y-4">
                {recommendations.length === 0 ? (
                  <div className="text-center text-gray-500 py-8">
                    Aucune recommandation disponible
                  </div>
                ) : (
                  recommendations.map((reco, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-semibold text-gray-900">
                          {reco.vehicule.marque} {reco.vehicule.modele}
                        </h3>
                        <span className="bg-violet-100 text-violet-700 px-2 py-1 rounded text-sm font-medium">
                          {reco.scores.total}/100
                        </span>
                      </div>
                      
                      <p className="text-gray-600 text-sm mb-2">
                        Prix: {reco.vehicule.prix_moyen.toLocaleString()}EUR | 
                        {reco.vehicule.type_carburant} | 
                        {reco.vehicule.nombre_places} places
                      </p>
                      
                      {reco.raisons && reco.raisons.length > 0 && (
                        <div className="mb-2">
                          <p className="text-sm font-medium text-gray-700 mb-1">Pourquoi ce véhicule:</p>
                          <ul className="text-xs text-gray-600 space-y-1">
                            {reco.raisons.map((raison, idx) => (
                              <li key={idx} className="flex items-start">
                                <span className="text-green-500 mr-1">check</span>
                                {raison}
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                      
                      <div className="flex gap-2 mt-3">
                        <button className="flex-1 bg-violet-600 text-white px-3 py-1 rounded text-sm hover:bg-violet-700">
                          Voir détails
                        </button>
                        <button className="flex-1 border border-violet-600 text-violet-600 px-3 py-1 rounded text-sm hover:bg-violet-50">
                          Comparer
                        </button>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}

            {showMarketInsights && (
              <div className="space-y-4">
                {marketInsights.length === 0 ? (
                  <div className="text-center text-gray-500 py-8">
                    Aucun insight disponible
                  </div>
                ) : (
                  marketInsights.map((insight, index) => (
                    <div key={index} className={`border rounded-lg p-4 ${getInsightColor(insight.niveau_impact)}`}>
                      <div className="flex items-start gap-3">
                        <span className="text-2xl">{getInsightIcon(insight.type)}</span>
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900 mb-1">
                            {insight.titre}
                          </h3>
                          <p className="text-sm text-gray-700 mb-2">
                            {insight.description}
                          </p>
                          <div className="flex items-center justify-between text-xs">
                            <span>Impact: {insight.niveau_impact}%</span>
                            <span>Confiance: {insight.confiance}%</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdvancedAssistantPage;
