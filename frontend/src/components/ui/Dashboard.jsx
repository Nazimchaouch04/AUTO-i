import React, { useState, useEffect } from 'react'
import { 
  TrendingUp, TrendingDown, List, Tag, BarChart3, Target, 
  Car, Star, Activity, PieChart as PieChartIcon, ExternalLink,
  Loader2, AlertCircle
} from 'lucide-react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, Area, AreaChart, PieChart, Pie, Cell, ReferenceLine, Legend, Label
} from 'recharts'

const COLORS = {
  accent: '#6C63FF',
  'accent-secondary': '#00D4AA',
  warning: '#F59E0B',
  danger: '#EF4444',
  success: '#10B981'
}

const FUEL_COLORS = {
  'Essence': '#6C63FF',
  'Diesel': '#00D4AA',
  'Électrique': '#F59E0B',
  'Hybride': '#EF4444'
}

const API_BASE = '/api'

const useDashboardData = (period) => {
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [data, setData] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      try {
        const [kpiRes, chartsRes, dealsRes] = await Promise.allSettled([
          fetch(`${API_BASE}/dashboard/kpis?period=${period}`),
          fetch(`${API_BASE}/dashboard/charts?period=${period}`),
          fetch(`${API_BASE}/dashboard/deals?period=${period}`)
        ])

        const kpiData = kpiRes.status === 'fulfilled' ? await kpiRes.value.json().catch(() => null) : null
        const chartsData = chartsRes.status === 'fulfilled' ? await chartsRes.value.json().catch(() => null) : null
        const dealsData = dealsRes.status === 'fulfilled' ? await dealsRes.value.json().catch(() => null) : null

        setData({
          kpis: kpiData || getMockKPIs(),
          charts: chartsData || getMockCharts(),
          deals: dealsData || getMockDeals()
        })
        setError(null)
      } catch (err) {
        setError(err.message)
        setData({
          kpis: getMockKPIs(),
          charts: getMockCharts(),
          deals: getMockDeals()
        })
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [period])

  return { loading, error, data }
}

const getMockKPIs = () => ({
  annoncesActives: { value: 12453, change: 12, trend: 'up', yesterday: 11119 },
  bonnesAffaires: { value: 147, change: 23, trend: 'up', yesterday: 119 },
  prixMoyen: { value: 15234, change: -2.3, trend: 'down', currency: '€' },
  precisionML: { value: 87.5, change: 3.2, trend: 'up' }
})

const getMockCharts = () => ({
  prixParMarque: [
    { marque: 'Peugeot', prix: 14500, annonces: 2341 },
    { marque: 'Renault', prix: 13800, annonces: 2156 },
    { marque: 'Volkswagen', prix: 18200, annonces: 1987 },
    { marque: 'BMW', prix: 24800, annonces: 1234 },
    { marque: 'Mercedes', prix: 26500, annonces: 987 },
    { marque: 'Audi', prix: 23100, annonces: 1123 },
    { marque: 'Citroën', prix: 12100, annonces: 1876 },
    { marque: 'Ford', prix: 16500, annonces: 943 }
  ],
  evolutionMarche: [
    { mois: 'Jan', prix_moyen: 14800, prix_median: 14200 },
    { mois: 'Fév', prix_moyen: 14950, prix_median: 14350 },
    { mois: 'Mar', prix_moyen: 15100, prix_median: 14500 },
    { mois: 'Avr', prix_moyen: 15080, prix_median: 14480 },
    { mois: 'Mai', prix_moyen: 15180, prix_median: 14600 },
    { mois: 'Juin', prix_moyen: 15234, prix_median: 14700 }
  ],
  carburants: [
    { name: 'Essence', value: 5234, count: 5234 },
    { name: 'Diesel', value: 4521, count: 4521 },
    { name: 'Électrique', value: 1456, count: 1456 },
    { name: 'Hybride', value: 1242, count: 1242 }
  ]
})

const getMockDeals = () => [
  { id: 1, marque: 'Renault', model: 'Clio IV', annee: 2019, prix: 8900, prixEstime: 11500, km: 45000, image: 'https://images.unsplash.com/photo-1542362567-b07e54358753?w=400', url: '#', badge: '-23%' },
  { id: 2, marque: 'Peugeot', model: '308', annee: 2020, prix: 14500, prixEstime: 17800, km: 32000, image: 'https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=400', url: '#', badge: '-19%' },
  { id: 3, marque: 'Volkswagen', model: 'Golf VIII', annee: 2021, prix: 21000, prixEstime: 26500, km: 18000, image: 'https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=400', url: '#', badge: '-21%' }
]

const SkeletonCard = () => (
  <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 animate-pulse">
    <div className="flex items-center space-x-3 mb-4">
      <div className="w-12 h-12 bg-primary-elevated rounded-lg"></div>
      <div>
        <div className="h-3 w-20 bg-primary-elevated rounded mb-2"></div>
        <div className="h-6 w-16 bg-primary-elevated rounded"></div>
      </div>
    </div>
    <div className="h-2 w-full bg-primary-elevated rounded"></div>
  </div>
)

const SkeletonChart = ({ height = 300 }) => (
  <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 animate-pulse">
    <div className="h-6 w-40 bg-primary-elevated rounded mb-6"></div>
    <div className="flex items-center justify-center" style={{ height }}>
      <Loader2 className="w-8 h-8 text-primary-elevated animate-spin" />
    </div>
  </div>
)

const ErrorState = ({ message, onRetry }) => (
  <div className="bg-primary-card border border-danger/30 rounded-xl p-8 text-center">
    <AlertCircle className="w-12 h-12 text-danger mx-auto mb-4" />
    <p className="text-primary-text-secondary mb-4">{message}</p>
    {onRetry && (
      <button 
        onClick={onRetry}
        className="px-4 py-2 bg-accent text-white rounded-lg hover:bg-accent/90 transition-colors"
      >
        Réessayer
      </button>
    )}
  </div>
)

const EmptyState = ({ message }) => (
  <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-8 text-center">
    <div className="w-16 h-16 bg-primary-elevated rounded-full flex items-center justify-center mx-auto mb-4">
      <List className="w-8 h-8 text-primary-text-secondary" />
    </div>
    <p className="text-primary-text-secondary">{message}</p>
  </div>
)

const KPICard = ({ title, value, change, trend, icon: Icon, color = 'accent', badge, showPulse, gauge }) => {
  const isPositive = trend === 'up'
  const colorValue = COLORS[color] || COLORS.accent
  
  return (
    <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 hover:shadow-card-hover transition-all duration-300">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="p-3 rounded-lg" style={{ backgroundColor: `${colorValue}15` }}>
            <Icon className="w-6 h-6" style={{ color: colorValue }} />
          </div>
          <div>
            <h3 className="text-primary-text-secondary text-sm font-medium">{title}</h3>
            <p className="text-2xl font-bold text-primary-text-primary">{value}</p>
          </div>
        </div>
        {badge && (
          <span className="px-2 py-1 bg-success/20 text-success text-xs font-medium rounded-full flex items-center gap-1">
            <span className={`w-2 h-2 rounded-full bg-success ${showPulse ? 'animate-pulse' : ''}`}></span>
            {badge}
          </span>
        )}
      </div>
      <div className="flex items-center justify-between">
        <div className={`flex items-center space-x-1 ${isPositive ? 'text-success' : 'text-danger'}`}>
          {isPositive ? <TrendingUp className="w-4 h-4" /> : <TrendingDown className="w-4 h-4" />}
          <span className="text-sm font-medium">{change > 0 ? '+' : ''}{change}%</span>
        </div>
        <span className="text-xs text-primary-text-secondary">vs hier</span>
      </div>
      {gauge && (
        <GaugeChart value={gauge.value} color={colorValue} />
      )}
    </div>
  )
}

const CustomBarTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-gray-900 border border-gray-700 rounded-lg p-4 shadow-xl">
        <p className="font-semibold text-white mb-2">{payload[0].payload.marque}</p>
        <p className="text-purple-400">Prix moyen: {payload[0].value.toLocaleString()}€</p>
        <p className="text-cyan-400">{payload[0].payload.annonces} annonces</p>
      </div>
    )
  }
  return null
}

const CustomLineTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-gray-900 border border-gray-700 rounded-lg p-3 shadow-xl">
        <p className="text-gray-400 text-sm mb-1">{label}</p>
        {payload.map((entry, index) => (
          <p key={index} style={{ color: entry.color }}>
            {entry.name}: {entry.value.toLocaleString()}€
          </p>
        ))}
      </div>
    )
  }
  return null
}

const CustomLegend = ({ payload }) => (
  <div className="flex items-center justify-center gap-6 mb-4">
    {payload.map((entry, index) => (
      <div key={index} className="flex items-center gap-2">
        <div className="w-3 h-3 rounded-full" style={{ backgroundColor: entry.color }}></div>
        <span className="text-primary-text-secondary text-sm">{entry.value}</span>
      </div>
    ))}
  </div>
)

const GaugeChart = ({ value, color = '#6C63FF' }) => {
  // SVG semi-circle gauge
  const radius = 36
  const stroke = 6
  const normalizedValue = Math.min(Math.max(value, 0), 100)
  const circumference = Math.PI * radius
  const strokeDashoffset = circumference - (normalizedValue / 100) * circumference

  return (
    <div className="relative w-24 h-14 mx-auto mt-3">
      <svg viewBox="0 0 80 45" className="w-full h-full overflow-visible">
        {/* Background arc */}
        <path
          d={`M 4 40 A ${radius} ${radius} 0 0 1 76 40`}
          fill="none"
          stroke="#374151"
          strokeWidth={stroke}
          strokeLinecap="round"
        />
        {/* Value arc */}
        <path
          d={`M 4 40 A ${radius} ${radius} 0 0 1 76 40`}
          fill="none"
          stroke={color}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={strokeDashoffset}
          className="transition-all duration-1000 ease-out"
        />
        {/* Value dot at the end */}
        <circle
          cx={4 + (72 * normalizedValue / 100)}
          cy={40 - Math.sin((normalizedValue / 100) * Math.PI) * radius}
          r="4"
          fill={color}
          className="transition-all duration-1000 ease-out"
        />
      </svg>
      {/* Centered label */}
      <div className="absolute bottom-0 left-1/2 transform -translate-x-1/2 text-center">
        <span className="text-xs text-primary-text-secondary font-medium">{value}%</span>
      </div>
    </div>
  )
}

const AnnonceCard = ({ deal }) => {
  const ecart = Math.round(((deal.prixEstime - deal.prix) / deal.prixEstime) * 100)
  const barWidth = Math.min((deal.prix / deal.prixEstime) * 100, 100)
  
  return (
    <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl overflow-hidden hover:shadow-card-hover transition-all duration-300 group">
      <div className="relative h-40 overflow-hidden">
        <img 
          src={deal.image} 
          alt={`${deal.marque} ${deal.model}`}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />
        {deal.badge && ecart > 20 && (
          <div className="absolute top-3 left-3 px-2 py-1 bg-danger text-white text-xs font-bold rounded flex items-center gap-1">
            🔥 {deal.badge}
          </div>
        )}
      </div>
      <div className="p-4">
        <div className="flex items-start justify-between mb-2">
          <div>
            <h4 className="font-semibold text-primary-text-primary">{deal.marque} {deal.model}</h4>
            <p className="text-sm text-primary-text-secondary">{deal.annee} • {deal.km.toLocaleString()} km</p>
          </div>
          <span className="text-lg font-bold text-accent">{deal.prix.toLocaleString()}€</span>
        </div>
        
        <div className="mt-3">
          <div className="flex justify-between text-xs text-primary-text-secondary mb-1">
            <span>Prix annonce</span>
            <span>Prix estimé</span>
          </div>
          <div className="w-full bg-primary-elevated rounded-full h-2 overflow-hidden">
            <div className="flex">
              <div 
                className="h-full bg-accent rounded-l-full"
                style={{ width: `${barWidth}%` }}
              ></div>
              <div 
                className="h-full bg-success"
                style={{ width: `${100 - barWidth}%` }}
              ></div>
            </div>
          </div>
          <p className="text-xs text-primary-text-secondary mt-1">
            Prix marché: <span className="text-success font-medium">{deal.prixEstime.toLocaleString()}€</span>
          </p>
        </div>
        
        <a 
          href={deal.url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-4 w-full flex items-center justify-center gap-2 px-4 py-2 bg-primary-elevated hover:bg-accent text-primary-text-primary hover:text-white rounded-lg transition-colors text-sm font-medium"
        >
          Voir l'annonce
          <ExternalLink className="w-4 h-4" />
        </a>
      </div>
    </div>
  )
}

export default function Dashboard() {
  const [selectedPeriod, setSelectedPeriod] = useState('7j')
  const { loading, error, data } = useDashboardData(selectedPeriod)

  const handlePeriodChange = (period) => {
    setSelectedPeriod(period)
  }

  const formatPrix = (value, currency = '€') => {
    return `${value.toLocaleString()} ${currency}`
  }

  const totalAnnonces = data?.charts?.carburants?.reduce((sum, item) => sum + item.count, 0) || 0

  return (
    <div className="min-h-screen bg-primary-bg pt-20 pb-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* En-tête avec filtres période */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 space-y-4 sm:space-y-0">
          <div>
            <h1 className="text-3xl font-bold text-primary-text-primary mb-2">Tableau de Bord</h1>
            <p className="text-primary-text-secondary">Vue d'ensemble du marché automobile</p>
          </div>
          
          {/* Filtres période avec skeleton */}
          <div className="flex items-center space-x-2 bg-primary-card rounded-lg p-1 border border-primary-border/DEFAULT">
            {['7j', '30j', '90j', '1an'].map((period) => (
              <button
                key={period}
                onClick={() => handlePeriodChange(period)}
                disabled={loading}
                className={`px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                  selectedPeriod === period
                    ? 'bg-accent text-white'
                    : 'bg-transparent text-primary-text-secondary hover:bg-primary-elevated'
                } ${loading ? 'opacity-50 cursor-not-allowed' : ''}`}
              >
                {period}
              </button>
            ))}
          </div>
        </div>

        {/* SECTION 1: KPI Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
          {loading ? (
            <>
              <SkeletonCard />
              <SkeletonCard />
              <SkeletonCard />
              <SkeletonCard />
            </>
          ) : error ? (
            <div className="col-span-4">
              <ErrorState message="Erreur lors du chargement des KPIs" onRetry={() => setSelectedPeriod(selectedPeriod)} />
            </div>
          ) : data?.kpis ? (
            <>
              <KPICard 
                title="Annonces actives" 
                value={data.kpis.annoncesActives.value.toLocaleString()}
                change={data.kpis.annoncesActives.change}
                trend={data.kpis.annoncesActives.trend}
                icon={List}
                color="accent"
              />
              <KPICard 
                title="Bonnes affaires" 
                value={data.kpis.bonnesAffaires.value}
                change={data.kpis.bonnesAffaires.change}
                trend={data.kpis.bonnesAffaires.trend}
                icon={Tag}
                color="success"
                badge={data.kpis.bonnesAffaires.value > 0 ? 'En cours' : null}
                showPulse={data.kpis.bonnesAffaires.value > 0}
              />
              <KPICard 
                title="Prix moyen marché" 
                value={formatPrix(data.kpis.prixMoyen.value, data.kpis.prixMoyen.currency)}
                change={data.kpis.prixMoyen.change}
                trend={data.kpis.prixMoyen.trend}
                icon={BarChart3}
                color="warning"
              />
              <KPICard 
                title="Précision ML" 
                value={`${data.kpis.precisionML.value}%`}
                change={data.kpis.precisionML.change}
                trend={data.kpis.precisionML.trend}
                icon={Target}
                color="accent-secondary"
                gauge={{ value: data.kpis.precisionML.value }}
              />
            </>
          ) : (
            <div className="col-span-4">
              <EmptyState message="Aucune donnée disponible" />
            </div>
          )}
        </div>

        {/* SECTION 2: Graphiques */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          
          {/* BarChart - Prix moyen par marque */}
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-primary-text-primary">Prix moyen par marque</h3>
              <div className="flex items-center space-x-2 text-sm text-primary-text-secondary">
                <BarChart3 className="w-4 h-4" />
                <span>Derniers 30 jours</span>
              </div>
            </div>
            
            {loading ? (
              <SkeletonChart height={280} />
            ) : data?.charts?.prixParMarque?.length > 0 ? (
              <ResponsiveContainer width="100%" height={280}>
                <BarChart data={data.charts.prixParMarque} margin={{ top: 20, right: 20, left: 0, bottom: 5 }}>
                  <defs>
                    <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#6C63FF" />
                      <stop offset="100%" stopColor="#00D4AA" />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                  <XAxis 
                    dataKey="marque" 
                    tick={{ fill: '#9CA3AF', fontSize: 12 }} 
                    axisLine={{ stroke: '#374151' }}
                  />
                  <YAxis 
                    tick={{ fill: '#9CA3AF', fontSize: 12 }} 
                    axisLine={{ stroke: '#374151' }}
                    tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
                  />
                  <Tooltip content={<CustomBarTooltip />} />
                  <Bar 
                    dataKey="prix" 
                    fill="url(#barGradient)" 
                    radius={[4, 4, 0, 0]}
                    animationDuration={800}
                    animationEasing="ease-out"
                    label={{
                      position: 'top',
                      fill: '#9CA3AF',
                      fontSize: 11,
                      formatter: (value) => `${(value / 1000).toFixed(1)}k€`
                    }}
                  />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <EmptyState message="Aucune donnée de prix disponible" />
            )}
          </div>

          {/* LineChart - Évolution du marché */}
          <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-lg font-semibold text-primary-text-primary">Évolution du marché 6 mois</h3>
              <div className="flex items-center space-x-2 text-sm text-primary-text-secondary">
                <Activity className="w-4 h-4" />
                <span>6 derniers mois</span>
              </div>
            </div>
            
            {loading ? (
              <SkeletonChart height={280} />
            ) : data?.charts?.evolutionMarche?.length > 0 ? (
              <>
                <CustomLegend payload={[
                  { value: 'Prix moyen', color: '#6C63FF' },
                  { value: 'Prix médian', color: '#00D4AA' }
                ]} />
                <ResponsiveContainer width="100%" height={240}>
                  <AreaChart data={data.charts.evolutionMarche} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="colorPrixMoyen" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#6C63FF" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#6C63FF" stopOpacity={0}/>
                      </linearGradient>
                      <linearGradient id="colorPrixMedian" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#00D4AA" stopOpacity={0.3}/>
                        <stop offset="95%" stopColor="#00D4AA" stopOpacity={0}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" opacity={0.3} />
                    <XAxis 
                      dataKey="mois" 
                      tick={{ fill: '#9CA3AF', fontSize: 12 }}
                      axisLine={{ stroke: '#374151' }}
                    />
                    <YAxis 
                      tick={{ fill: '#9CA3AF', fontSize: 12 }}
                      axisLine={{ stroke: '#374151' }}
                      tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
                    />
                    <Tooltip content={<CustomLineTooltip />} />
                    <ReferenceLine 
                      x={data.charts.evolutionMarche[data.charts.evolutionMarche.length - 1]?.mois} 
                      stroke="#10B981" 
                      strokeDasharray="5 5"
                      label={{ 
                        value: 'Aujourd\'hui', 
                        fill: '#10B981', 
                        fontSize: 11,
                        position: 'top'
                      }} 
                    />
                    <Area 
                      type="monotone" 
                      dataKey="prix_moyen" 
                      stroke="#6C63FF" 
                      strokeWidth={2}
                      fillOpacity={1} 
                      fill="url(#colorPrixMoyen)" 
                      dot={{ fill: '#fff', stroke: '#6C63FF', strokeWidth: 2, r: 4 }}
                      activeDot={{ fill: '#6C63FF', stroke: '#fff', strokeWidth: 2, r: 6 }}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="prix_median" 
                      stroke="#00D4AA" 
                      strokeWidth={2}
                      fillOpacity={1} 
                      fill="url(#colorPrixMedian)" 
                      dot={{ fill: '#fff', stroke: '#00D4AA', strokeWidth: 2, r: 4 }}
                      activeDot={{ fill: '#00D4AA', stroke: '#fff', strokeWidth: 2, r: 6 }}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </>
            ) : (
              <EmptyState message="Aucune donnée d'évolution disponible" />
            )}
          </div>
        </div>

        {/* SECTION 3: Meilleures affaires */}
        <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6 mb-8">
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <h3 className="text-lg font-semibold text-primary-text-primary">Meilleures affaires du moment</h3>
              <span className="flex items-center gap-1.5 px-2 py-1 bg-success/20 text-success text-xs font-medium rounded-full">
                <span className="w-2 h-2 rounded-full bg-success animate-pulse"></span>
                Live
              </span>
            </div>
          </div>
          
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <SkeletonCard />
              <SkeletonCard />
              <SkeletonCard />
            </div>
          ) : error ? (
            <ErrorState message="Erreur lors du chargement des bonnes affaires" />
          ) : data?.deals?.length > 0 ? (
            <>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                {data.deals.map((deal) => (
                  <AnnonceCard key={deal.id} deal={deal} />
                ))}
              </div>
              <div className="text-center">
                <button className="inline-flex items-center gap-2 px-6 py-3 bg-accent text-white rounded-lg hover:bg-accent/90 transition-colors font-medium">
                  Voir toutes les bonnes affaires →
                </button>
              </div>
            </>
          ) : (
            <EmptyState message="Aucune bonne affaire trouvée pour cette période" />
          )}
        </div>

        {/* PieChart - Répartition carburants (en dessous) */}
        <div className="bg-primary-card border border-primary-border/DEFAULT rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h3 className="text-lg font-semibold text-primary-text-primary">Répartition carburants</h3>
            <div className="flex items-center space-x-2 text-sm text-primary-text-secondary">
              <PieChartIcon className="w-4 h-4" />
              <span>Par type</span>
            </div>
          </div>
          
          {loading ? (
            <SkeletonChart height={250} />
          ) : data?.charts?.carburants?.length > 0 ? (
            <div className="flex flex-col md:flex-row items-center justify-center gap-8">
              <div className="relative">
                <ResponsiveContainer width={280} height={250}>
                  <PieChart>
                    <Pie
                      data={data.charts.carburants}
                      cx="50%"
                      cy="50%"
                      innerRadius={60}
                      outerRadius={100}
                      paddingAngle={2}
                      dataKey="value"
                      startAngle={90}
                      animationDuration={800}
                      animationBegin={0}
                    >
                      {data.charts.carburants.map((entry, index) => (
                        <Cell 
                          key={`cell-${index}`} 
                          fill={FUEL_COLORS[entry.name] || COLORS.accent}
                        />
                      ))}
                    </Pie>
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#1F2937', 
                        border: '1px solid #374151',
                        borderRadius: '8px'
                      }}
                      itemStyle={{ color: '#fff' }}
                      formatter={(value, name) => [value.toLocaleString(), name]}
                    />
                  </PieChart>
                </ResponsiveContainer>
                {/* Label central */}
                <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                  <span className="text-2xl font-bold text-primary-text-primary">{totalAnnonces.toLocaleString()}</span>
                  <span className="text-xs text-primary-text-secondary">annonces</span>
                </div>
              </div>
              
              {/* Légende personnalisée */}
              <div className="flex flex-col gap-3">
                {data.charts.carburants.map((item, index) => (
                  <div key={index} className="flex items-center gap-3">
                    <div 
                      className="w-4 h-4 rounded"
                      style={{ backgroundColor: FUEL_COLORS[item.name] || COLORS.accent }}
                    ></div>
                    <span className="text-primary-text-primary font-medium w-24">{item.name}</span>
                    <span className="text-primary-text-secondary text-sm">
                      {Math.round((item.count / totalAnnonces) * 100)}%
                    </span>
                    <span className="text-primary-text-secondary text-sm">
                      ({item.count.toLocaleString()})
                    </span>
                  </div>
                ))}
                <div className="mt-2 pt-2 border-t border-primary-border/DEFAULT">
                  <span className="text-primary-text-primary font-semibold">
                    Total: {totalAnnonces.toLocaleString()} annonces
                  </span>
                </div>
              </div>
            </div>
          ) : (
            <EmptyState message="Aucune donnée de carburants disponible" />
          )}
        </div>

      </div>
    </div>
  )
}
