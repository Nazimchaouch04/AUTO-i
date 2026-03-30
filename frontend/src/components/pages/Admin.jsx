import React, { useState, useEffect } from 'react'
import { Settings, Database, Users, Car, BarChart3, AlertTriangle, CheckCircle, Activity, RefreshCw, Download, Upload } from 'lucide-react'

export default function Admin() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('overview')
  const [systemStatus, setSystemStatus] = useState('healthy')

  useEffect(() => {
    fetchAdminStats()
    checkSystemHealth()
  }, [])

  const fetchAdminStats = async () => {
    setLoading(true)
    try {
      // Simuler API call
      setTimeout(() => {
        setStats({
          overview: {
            total_users: 1234,
            total_annonces: 12453,
            total_estimations: 3456,
            total_alertes: 789,
            daily_active_users: 234,
            monthly_active_users: 892,
            conversion_rate: 3.2,
            avg_session_duration: 450
          },
          database: {
            total_records: 15678,
            database_size: '2.3 GB',
            last_backup: '2024-01-18 02:00',
            backup_status: 'success',
            tables_count: 12,
            indexes_count: 34,
            query_avg_time: 0.05
          },
          performance: {
            avg_response_time: 145,
            uptime_percentage: 99.8,
            error_rate: 0.2,
            api_calls_today: 45678,
            cache_hit_rate: 78.5,
            memory_usage: 68.2,
            cpu_usage: 42.1
          },
          recent_activity: [
            {
              type: 'new_user',
              user: 'jean_dupont',
              timestamp: '2024-01-18 14:23',
              details: 'Inscription nouvelle utilisateur'
            },
            {
              type: 'new_annonce',
              user: 'admin',
              timestamp: '2024-01-18 14:15',
              details: 'Nouvelle annonce ajoutée: Peugeot 208'
            },
            {
              type: 'estimation',
              user: 'marie_dubois',
              timestamp: '2024-01-18 14:10',
              details: 'Estimation réalisée: Renault Clio'
            },
            {
              type: 'alert_triggered',
              user: 'system',
              timestamp: '2024-01-18 14:05',
              details: 'Alerte déclenchée pour 5 utilisateurs'
            }
          ],
          system_logs: [
            {
              level: 'info',
              timestamp: '2024-01-18 14:30',
              message: 'Database backup completed successfully',
              source: 'backup_system'
            },
            {
              level: 'warning',
              timestamp: '2024-01-18 14:25',
              message: 'High memory usage detected on server-01',
              source: 'monitoring'
            },
            {
              level: 'error',
              timestamp: '2024-01-18 14:20',
              message: 'API rate limit exceeded for user: bot_detector',
              source: 'api_gateway'
            },
            {
              level: 'info',
              timestamp: '2024-01-18 14:15',
              message: 'Cache cleared successfully',
              source: 'cache_manager'
            }
          ]
        })
        setLoading(false)
      }, 1000)
    } catch (error) {
      console.error('Error fetching admin stats:', error)
      setLoading(false)
    }
  }

  const checkSystemHealth = () => {
    // Simuler vérification système
    const healthChecks = [
      { service: 'Database', status: 'healthy', response_time: 0.05 },
      { service: 'API Gateway', status: 'healthy', response_time: 0.12 },
      { service: 'Cache', status: 'healthy', response_time: 0.02 },
      { service: 'Email Service', status: 'degraded', response_time: 1.2 },
      { service: 'File Storage', status: 'healthy', response_time: 0.08 }
    ]
    
    const hasIssues = healthChecks.some(check => check.status !== 'healthy')
    setSystemStatus(hasIssues ? 'degraded' : 'healthy')
  }

  const handleSystemAction = (action) => {
    switch (action) {
      case 'backup':
        alert('Backup démarré...')
        break
      case 'cache_clear':
        alert('Cache vidé avec succès')
        break
      case 'restart_api':
        alert('API redémarré')
        break
      case 'export_data':
        alert('Export des données en cours...')
        break
      default:
        break
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-primary-bg pt-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse-slow">
            <div className="h-8 bg-primary-card rounded w-1/3 mb-8"></div>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              {[...Array(4)].map((_, index) => (
                <div key={index} className="h-32 bg-primary-card rounded-xl"></div>
              ))}
            </div>
            <div className="h-96 bg-primary-card rounded-xl"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-primary-bg pt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-primary-text-primary mb-2">Administration</h1>
            <p className="text-primary-text-secondary">Panneau de contrôle système</p>
          </div>
          <div className="flex items-center space-x-2">
            <div className={`flex items-center space-x-2 px-3 py-1 rounded-full text-sm font-medium ${
              systemStatus === 'healthy' 
                ? 'bg-success/10 text-success' 
                : 'bg-warning/10 text-warning'
            }`}>
              <div className={`w-2 h-2 rounded-full ${
                systemStatus === 'healthy' ? 'bg-success' : 'bg-warning'
              }`}></div>
              <span>{systemStatus === 'healthy' ? 'Système sain' : 'Système dégradé'}</span>
            </div>
            <button
              onClick={checkSystemHealth}
              className="p-2 border border-primary-border/DEFAULT rounded-lg hover:bg-primary-elevated transition-colors duration-200"
            >
              <RefreshCw className="w-4 h-4 text-primary-text-secondary" />
            </button>
          </div>
        </div>

        {/* Navigation des onglets */}
        <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl mb-8">
          <div className="flex border-b border-primary-border/DEFAULT">
            {[
              { id: 'overview', label: 'Vue d\'ensemble', icon: BarChart3 },
              { id: 'database', label: 'Base de données', icon: Database },
              { id: 'performance', label: 'Performance', icon: Activity },
              { id: 'logs', label: 'Logs système', icon: AlertTriangle }
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 flex-1 py-4 px-6 text-center font-medium transition-colors duration-200 ${
                  activeTab === tab.id 
                    ? 'text-accent border-b-2 border-accent' 
                    : 'text-primary-text-secondary hover:text-primary-text-primary'
                }`}
              >
                <tab.icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            ))}
          </div>

          {/* Contenu des onglets */}
          <div className="p-6">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                {/* KPI Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="bg-primary-elevated rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <Users className="w-8 h-8 text-accent" />
                      <span className="text-sm text-success">+12%</span>
                    </div>
                    <p className="text-2xl font-bold text-primary-text-primary">{stats.overview.total_users}</p>
                    <p className="text-sm text-primary-text-secondary">Utilisateurs totaux</p>
                  </div>
                  <div className="bg-primary-elevated rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <Car className="w-8 h-8 text-accent-secondary" />
                      <span className="text-sm text-success">+8%</span>
                    </div>
                    <p className="text-2xl font-bold text-primary-text-primary">{stats.overview.total_annonces}</p>
                    <p className="text-sm text-primary-text-secondary">Annonces totales</p>
                  </div>
                  <div className="bg-primary-elevated rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <BarChart3 className="w-8 h-8 text-success" />
                      <span className="text-sm text-success">+15%</span>
                    </div>
                    <p className="text-2xl font-bold text-primary-text-primary">{stats.overview.total_estimations}</p>
                    <p className="text-sm text-primary-text-secondary">Estimations</p>
                  </div>
                  <div className="bg-primary-elevated rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <AlertTriangle className="w-8 h-8 text-warning" />
                      <span className="text-sm text-warning">+5%</span>
                    </div>
                    <p className="text-2xl font-bold text-primary-text-primary">{stats.overview.total_alertes}</p>
                    <p className="text-sm text-primary-text-secondary">Alertes actives</p>
                  </div>
                </div>

                {/* Activité récente */}
                <div>
                  <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Activité récente</h3>
                  <div className="space-y-3">
                    {stats.recent_activity.map((activity, index) => (
                      <div key={index} className="flex items-center space-x-4 p-3 bg-primary-elevated rounded-lg">
                        <div className={`w-2 h-2 rounded-full ${
                          activity.type === 'error' ? 'bg-danger' :
                          activity.type === 'warning' ? 'bg-warning' : 'bg-success'
                        }`}></div>
                        <div className="flex-1">
                          <p className="text-primary-text-primary">{activity.details}</p>
                          <p className="text-sm text-primary-text-secondary">
                            {activity.user} • {activity.timestamp}
                          </p>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {activeTab === 'database' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Base de données</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="bg-primary-elevated rounded-lg p-4">
                      <p className="text-sm text-primary-text-secondary mb-1">Taille totale</p>
                      <p className="text-2xl font-bold text-primary-text-primary">{stats.database.database_size}</p>
                    </div>
                    <div className="bg-primary-elevated rounded-lg p-4">
                      <p className="text-sm text-primary-text-secondary mb-1">Nombre d'enregistrements</p>
                      <p className="text-2xl font-bold text-primary-text-primary">{stats.database.total_records.toLocaleString()}</p>
                    </div>
                    <div className="bg-primary-elevated rounded-lg p-4">
                      <p className="text-sm text-primary-text-secondary mb-1">Tables</p>
                      <p className="text-2xl font-bold text-primary-text-primary">{stats.database.tables_count}</p>
                    </div>
                  </div>
                  
                  <div className="space-y-4">
                    <div className="bg-primary-elevated rounded-lg p-4">
                      <p className="text-sm text-primary-text-secondary mb-1">Dernière sauvegarde</p>
                      <p className="text-lg font-bold text-primary-text-primary">{stats.database.last_backup}</p>
                      <div className="flex items-center space-x-1 mt-1">
                        <CheckCircle className="w-4 h-4 text-success" />
                        <span className="text-sm text-success">Succès</span>
                      </div>
                    </div>
                    <div className="bg-primary-elevated rounded-lg p-4">
                      <p className="text-sm text-primary-text-secondary mb-1">Temps de requête moyen</p>
                      <p className="text-2xl font-bold text-primary-text-primary">{stats.database.query_avg_time}s</p>
                    </div>
                  </div>
                </div>

                {/* Actions base de données */}
                <div className="flex space-x-4">
                  <button
                    onClick={() => handleSystemAction('backup')}
                    className="flex items-center space-x-2 bg-accent hover:bg-accent-secondary text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
                  >
                    <Download className="w-4 h-4" />
                    <span>Sauvegarder</span>
                  </button>
                  <button
                    onClick={() => handleSystemAction('export_data')}
                    className="flex items-center space-x-2 bg-primary-elevated hover:bg-primary-elevated/90 text-primary-text-primary px-4 py-2 rounded-lg font-medium transition-colors duration-200"
                  >
                    <Upload className="w-4 h-4" />
                    <span>Exporter</span>
                  </button>
                </div>
              </div>
            )}

            {activeTab === 'performance' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Performance système</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="bg-primary-elevated rounded-lg p-4">
                    <p className="text-sm text-primary-text-secondary mb-1">Temps de réponse moyen</p>
                    <p className="text-2xl font-bold text-primary-text-primary">{stats.performance.avg_response_time}ms</p>
                  </div>
                  <div className="bg-primary-elevated rounded-lg p-4">
                    <p className="text-sm text-primary-text-secondary mb-1">Taux de disponibilité</p>
                    <p className="text-2xl font-bold text-success">{stats.performance.uptime_percentage}%</p>
                  </div>
                  <div className="bg-primary-elevated rounded-lg p-4">
                    <p className="text-sm text-primary-text-secondary mb-1">Appels API aujourd'hui</p>
                    <p className="text-2xl font-bold text-primary-text-primary">{stats.performance.api_calls_today.toLocaleString()}</p>
                  </div>
                  <div className="bg-primary-elevated rounded-lg p-4">
                    <p className="text-sm text-primary-text-secondary mb-1">Taux d'erreur</p>
                    <p className="text-2xl font-bold text-danger">{stats.performance.error_rate}%</p>
                  </div>
                </div>

                {/* Actions performance */}
                <div className="flex space-x-4">
                  <button
                    onClick={() => handleSystemAction('cache_clear')}
                    className="flex items-center space-x-2 bg-accent hover:bg-accent-secondary text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
                  >
                    <RefreshCw className="w-4 h-4" />
                    <span>Vider le cache</span>
                  </button>
                  <button
                    onClick={() => handleSystemAction('restart_api')}
                    className="flex items-center space-x-2 bg-warning hover:bg-warning/90 text-white px-4 py-2 rounded-lg font-medium transition-colors duration-200"
                  >
                    <Settings className="w-4 h-4" />
                    <span>Redémarrer API</span>
                  </button>
                </div>
              </div>
            )}

            {activeTab === 'logs' && (
              <div className="space-y-6">
                <h3 className="text-lg font-semibold text-primary-text-primary mb-4">Logs système</h3>
                
                <div className="space-y-3">
                  {stats.system_logs.map((log, index) => (
                    <div key={index} className="flex items-start space-x-4 p-4 bg-primary-elevated rounded-lg">
                      <div className={`w-3 h-3 rounded-full mt-1 ${
                        log.level === 'error' ? 'bg-danger' :
                        log.level === 'warning' ? 'bg-warning' :
                        log.level === 'success' ? 'bg-success' : 'bg-primary-text-secondary'
                      }`}></div>
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <span className={`text-xs font-medium uppercase ${
                            log.level === 'error' ? 'text-danger' :
                            log.level === 'warning' ? 'text-warning' :
                            log.level === 'success' ? 'text-success' : 'text-primary-text-secondary'
                          }`}>
                            {log.level}
                          </span>
                          <span className="text-sm text-primary-text-secondary">{log.timestamp}</span>
                          <span className="text-sm text-primary-text-secondary">• {log.source}</span>
                        </div>
                        <p className="text-primary-text-primary">{log.message}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
