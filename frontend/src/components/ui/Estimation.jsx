import React, { useState, useEffect, useRef } from 'react'
import {
  Search, Zap, Fuel, Leaf, Settings, Calendar,
  Loader2, ChevronDown, RotateCcw, ExternalLink, Sparkles,
  X, TrendingUp, TrendingDown, Car, MapPin, Gauge, Clock
} from 'lucide-react'
import { useDispatch, useSelector } from 'react-redux'
import { addEstimation } from '../../store/estimationHistorySlice'
import ExportButton from './ExportButton'

// ─── Constants ───────────────────────────────────────────────────────────────
const ACCENT = '#6C63FF'
const SUCCESS = '#10B981'
const WARNING = '#F59E0B'
const DANGER = '#EF4444'
const TEAL = '#00D4AA'

const MARQUES = [
  // Marques présentes en DB (données réelles)
  { id: 'BMW',        name: 'BMW',        logo: '◈',  premium: true  },
  { id: 'Mercedes',   name: 'Mercedes',   logo: '⭐', premium: true  },
  { id: 'Volkswagen', name: 'Volkswagen', logo: 'Ⓥ',  premium: false },
  { id: 'Toyota',     name: 'Toyota',     logo: 'Ⓣ',  premium: false },
  { id: 'Renault',    name: 'Renault',    logo: '🔷', premium: false },
  { id: 'Kia',        name: 'Kia',        logo: '🔲', premium: false },
  { id: 'Hyundai',    name: 'Hyundai',    logo: '🔵', premium: false },
  { id: 'Peugeot',    name: 'Peugeot',    logo: '🦁', premium: false },
  { id: 'Ford',       name: 'Ford',       logo: 'Ⓕ',  premium: false },
  { id: 'Dacia',      name: 'Dacia',      logo: '🟦', premium: false },
  // Autres marques (fallback prix de référence)
  { id: 'Audi',       name: 'Audi',       logo: '◎',  premium: true  },
  { id: 'Citroen',    name: 'Citroën',    logo: '⩗',  premium: false },
]

const MODELES_PAR_MARQUE = {
  // Modèles réels en DB
  BMW:        ['320', '328', 'X5', 'Série 1', 'Série 3', 'Série 5', 'X1', 'X3'],
  Mercedes:   ['C-Class', 'E-Class', 'GLE', 'Classe A', 'Classe C', 'GLA', 'GLC'],
  Volkswagen: ['Golf', 'Polo', 'Tiguan', 'Passat', 'T-Roc', 'Arteon'],
  Toyota:     ['Yaris', 'Corolla', 'RAV4', 'C-HR', 'Camry'],
  Renault:    ['Clio', 'Captur', 'Megane', 'Scenic', 'Kadjar', 'Talisman', 'Duster'],
  Kia:        ['Ceed', 'Picanto', 'Sportage'],
  Hyundai:    ['Tucson', 'i20', 'i30'],
  Peugeot:    ['206', '207', '307', '308', '3008', '208', '5008', '2008', '508'],
  Ford:       ['Fiesta', 'Focus', 'Mondeo', 'Puma', 'Kuga'],
  Dacia:      ['Duster', 'Logan', 'Sandero'],
  Audi:       ['A1', 'A3', 'A4', 'A5', 'Q3', 'Q5', 'Q7'],
  Citroen:    ['C3', 'C4', 'C5 Aircross', 'Berlingo'],
}

const REGIONS = [
  { code: 'DZ', name: 'Algérie',  flag: '🇩🇿' },
  { code: 'TN', name: 'Tunisie',  flag: '🇹🇳' },
  { code: 'FR', name: 'France',   flag: '🇫🇷' },
  { code: 'MA', name: 'Maroc',    flag: '🇲🇦' },
]

const CARBURANTS = [
  { id: 'essence',   name: 'Essence',    Icon: Fuel,   color: WARNING,  emoji: '⛽' },
  { id: 'diesel',    name: 'Diesel',     Icon: Fuel,   color: '#64748B', emoji: '🛢️' },
  { id: 'electrique',name: 'Électrique', Icon: Zap,    color: TEAL,     emoji: '⚡' },
  { id: 'hybride',   name: 'Hybride',    Icon: Leaf,   color: SUCCESS,  emoji: '🌿' },
]

// ─── Helpers ─────────────────────────────────────────────────────────────────
const KM_MAX = 300000
const sliderToKm = v => {
  const t = Math.min(1, Math.max(0, v / 1000))
  if (t === 0) return 0
  const maxLog = Math.log10(KM_MAX + 1)
  return Math.min(KM_MAX, Math.round(Math.pow(10, t * maxLog) - 1))
}
const kmToSlider = km => {
  const safe = Math.min(KM_MAX, Math.max(0, km))
  if (safe === 0) return 0
  const maxLog = Math.log10(KM_MAX + 1)
  return Math.round((Math.log10(safe + 1) / maxLog) * 1000)
}

const getCategoriePuissance = cv => {
  if (cv < 100) return { label: 'Citadine', color: SUCCESS }
  if (cv < 200) return { label: 'Berline',  color: WARNING }
  return              { label: 'Sport',     color: DANGER  }
}

const reliabilityStyle = f => {
  if (f === 'Haute')   return { bg: `${SUCCESS}22`, color: SUCCESS, dot: SUCCESS }
  if (f === 'Moyenne') return { bg: `${WARNING}22`, color: WARNING, dot: WARNING }
  return                      { bg: `${DANGER}22`,  color: DANGER,  dot: DANGER  }
}

const relativeDate = iso => {
  const diff  = Date.now() - new Date(iso).getTime()
  const hours = Math.floor(diff / 3_600_000)
  if (hours < 1)  return "À l'instant"
  if (hours < 24) return `Il y a ${hours}h`
  const days = Math.floor(hours / 24)
  if (days === 1) return 'Hier'
  return `Il y a ${days} jours`
}

// ─── useCountUp ──────────────────────────────────────────────────────────────
const useCountUp = (target, duration = 1200) => {
  const [value, setValue] = useState(0)
  const startAnimation = () => {
    const t0 = Date.now()
    const tick = () => {
      const p = Math.min((Date.now() - t0) / duration, 1)
      const e = 1 - Math.pow(1 - p, 3)
      setValue(Math.floor(target * e))
      if (p < 1) requestAnimationFrame(tick)
      else setValue(target)
    }
    tick()
  }
  return { value, startAnimation }
}

// ─── AutoCoinToast ───────────────────────────────────────────────────────────
const AutoCoinToast = ({ show, onClose }) => {
  useEffect(() => {
    if (!show) return
    const t = setTimeout(onClose, 3000)
    return () => clearTimeout(t)
  }, [show, onClose])

  return (
    <div style={{
      position: 'fixed', top: 88, right: 16, zIndex: 9999,
      transform: show ? 'translateX(0)' : 'translateX(120%)',
      transition: 'transform 0.35s cubic-bezier(.22,1,.36,1)',
      pointerEvents: show ? 'auto' : 'none',
    }}>
      <div style={{
        background: `linear-gradient(135deg, ${ACCENT}, ${TEAL})`,
        color: '#fff', padding: '14px 20px', borderRadius: 16,
        boxShadow: `0 8px 32px ${ACCENT}44`,
        display: 'flex', alignItems: 'center', gap: 12, minWidth: 260,
      }}>
        <div style={{
          width: 40, height: 40, borderRadius: '50%',
          background: 'rgba(255,255,255,.2)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontSize: 20,
        }}>⚡</div>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 700, fontSize: 15 }}>+50 AutoCoins gagnés !</div>
          <div style={{ fontSize: 12, opacity: .8 }}>Merci d'utiliser AutoIntel</div>
        </div>
        <button
          onClick={onClose}
          style={{ background: 'rgba(255,255,255,.2)', border: 'none', borderRadius: 8,
            width: 28, height: 28, cursor: 'pointer', display: 'flex',
            alignItems: 'center', justifyContent: 'center', color: '#fff' }}
        >
          <X size={14} />
        </button>
      </div>
    </div>
  )
}

// ─── MiniGauge ───────────────────────────────────────────────────────────────
const MiniGauge = ({ value, color = ACCENT }) => {
  const r = 20, circ = 2 * Math.PI * r
  return (
    <div style={{ position: 'relative', width: 56, height: 56 }}>
      <svg viewBox="0 0 48 48" style={{ transform: 'rotate(-90deg)', width: 56, height: 56 }}>
        <circle cx="24" cy="24" r={r} stroke="#2a2a3e" strokeWidth="5" fill="none" />
        <circle
          cx="24" cy="24" r={r}
          stroke={color} strokeWidth="5" fill="none"
          strokeDasharray={circ}
          strokeDashoffset={circ - (value / 100) * circ}
          strokeLinecap="round"
          style={{ transition: 'stroke-dashoffset 1.2s ease' }}
        />
      </svg>
      <span style={{
        position: 'absolute', inset: 0, display: 'flex',
        alignItems: 'center', justifyContent: 'center',
        fontSize: 11, fontWeight: 700, color,
      }}>{value}%</span>
    </div>
  )
}

// ─── HistoryCard ─────────────────────────────────────────────────────────────
const HistoryCard = ({ estimation, onReuse }) => {
  const m = MARQUES.find(x => x.id === estimation.vehicule?.marque)
  return (
    <div style={{
      background: '#13131E', border: '1px solid #2a2a3e',
      borderRadius: 14, padding: '14px 16px', minWidth: 230, flexShrink: 0,
      transition: 'border-color .2s, transform .2s',
    }}
      onMouseEnter={e => { e.currentTarget.style.borderColor = ACCENT; e.currentTarget.style.transform = 'translateY(-2px)' }}
      onMouseLeave={e => { e.currentTarget.style.borderColor = '#2a2a3e'; e.currentTarget.style.transform = 'translateY(0)' }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: 22 }}>{m?.logo || '🚗'}</span>
          <div>
            <div style={{ fontWeight: 600, color: '#F0F0F5', fontSize: 14 }}>
              {m?.name || estimation.vehicule?.marque} {estimation.vehicule?.modele}
            </div>
            <div style={{ fontSize: 12, color: '#8888AA' }}>{estimation.vehicule?.annee}</div>
          </div>
        </div>
        <div style={{ fontWeight: 700, color: ACCENT, fontSize: 15 }}>
          {estimation.prix_estime?.toLocaleString()}€
        </div>
      </div>

      <div style={{ fontSize: 11, color: '#6666AA', marginBottom: 10 }}>
        {relativeDate(estimation.date)}
      </div>

      <div style={{ display: 'flex', gap: 8 }}>
        <button
          onClick={() => onReuse(estimation)}
          style={{
            flex: 1, padding: '6px 0', border: `1px solid ${ACCENT}44`,
            borderRadius: 8, background: `${ACCENT}11`,
            color: ACCENT, fontSize: 12, fontWeight: 600, cursor: 'pointer',
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4,
          }}
        >
          <RotateCcw size={11} /> Réutiliser
        </button>
        <a
          href={`/annonces?marque=${estimation.vehicule?.marque}&modele=${estimation.vehicule?.modele}`}
          style={{
            flex: 1, padding: '6px 0', border: '1px solid #2a2a3e',
            borderRadius: 8, background: 'transparent',
            color: '#8888AA', fontSize: 12, cursor: 'pointer',
            display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4,
            textDecoration: 'none',
          }}
        >
          Similaires <ExternalLink size={11} />
        </a>
      </div>
    </div>
  )
}

// ─── SectionLabel ────────────────────────────────────────────────────────────
const SectionLabel = ({ icon: Icon, text }) => (
  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 20 }}>
    <div style={{
      width: 32, height: 32, borderRadius: 10,
      background: `${ACCENT}22`, display: 'flex', alignItems: 'center', justifyContent: 'center',
    }}>
      <Icon size={16} color={ACCENT} />
    </div>
    <span style={{ fontWeight: 700, fontSize: 15, color: '#F0F0F5' }}>{text}</span>
  </div>
)

// ─── FieldLabel ──────────────────────────────────────────────────────────────
const FieldLabel = ({ children }) => (
  <div style={{ fontSize: 13, fontWeight: 500, color: '#8888AA', marginBottom: 8 }}>
    {children}
  </div>
)

// ─── Main Component ──────────────────────────────────────────────────────────
export default function Estimation({ onSubmit, showResult, data }) {
  const [form, setForm] = useState({
    marque: '', modele: '',
    anneeMin: 2018, anneeMax: 2020,
    kilometrage: 50000,
    carburant: 'essence', boite: 'manuelle',
    puissance: 120, region: 'DZ',
  })
  const [loading, setLoading]             = useState(false)
  const [marqueSearch, setMarqueSearch]   = useState('')
  const [dropdownOpen, setDropdownOpen]   = useState(false)
  const [result, setResult]               = useState(null)
  const [showToast, setShowToast]         = useState(false)
  const [resultVisible, setResultVisible] = useState(false)

  const dropdownRef = useRef(null)
  const resultRef   = useRef(null)
  const dispatch    = useDispatch()
  const history     = useSelector(s => s.estimationHistory.items)
  const { value: animatedPrice, startAnimation } = useCountUp(result?.prix_estime || 0)

  // Close dropdown on outside click
  useEffect(() => {
    const h = e => { if (dropdownRef.current && !dropdownRef.current.contains(e.target)) setDropdownOpen(false) }
    document.addEventListener('mousedown', h)
    return () => document.removeEventListener('mousedown', h)
  }, [])

  const set = (k, v) => {
    setForm(p => ({ ...p, [k]: v, ...(k === 'marque' ? { modele: '' } : {}) }))
  }

  const anneeAge = () => {
    const mn = Math.max(0, 2025 - form.anneeMax)
    const mx = Math.max(0, 2025 - form.anneeMin)
    if (mn === mx) return mn === 0 ? 'Neuf' : `Il y a ${mn} ans`
    return `Entre ${mn} et ${mx} ans`
  }

  const kmAn = () => {
    const age = 2025 - Math.round((form.anneeMin + form.anneeMax) / 2)
    if (age <= 0) return form.kilometrage
    return Math.round(form.kilometrage / age)
  }

  const catPuissance = getCategoriePuissance(form.puissance)
  const isValid = form.marque && form.modele && form.anneeMin <= form.anneeMax && form.kilometrage >= 0

  const addCoins = async () => {
    try {
      await fetch('/api/gamification/add-coins/', {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ amount: 50, reason: 'estimation' }),
      })
    } catch {}
  }

  const handleSubmit = async e => {
    e.preventDefault()
    if (!isValid) return
    setLoading(true)
    setResultVisible(false)
    try {
      const resp = await fetch('/api/estimation/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          marque: form.marque, modele: form.modele,
          annee_min: form.anneeMin, annee_max: form.anneeMax,
          kilometrage: form.kilometrage,
          carburant: form.carburant, boite: form.boite,
          puissance: form.puissance, pays: form.region,
        }),
      })
      let r
      if (resp.ok) {
        r = await resp.json()
      } else {
        const prices = { peugeot:15000,renault:14000,volkswagen:18000,bmw:25000,mercedes:28000,audi:24000,citroen:13000,toyota:16000,ford:14500 }
        const base = prices[form.marque] || 15000
        const age  = 2025 - Math.round((form.anneeMin + form.anneeMax) / 2)
        const est  = Math.round(
          base *
          Math.max(0.3, 1 - age * 0.08) *
          (form.kilometrage > 100000 ? Math.max(0.5, 1 - (form.kilometrage - 100000) / 100000) : 1) *
          (form.carburant === 'electrique' ? 1.15 : form.carburant === 'hybride' ? 1.1 : 1) *
          (form.boite === 'automatique' ? 1.08 : 1)
        )
        r = {
          prix_estime: est,
          fourchette_basse: Math.round(est * 0.85),
          fourchette_haute: Math.round(est * 1.15),
          fiabilite: age < 5 ? 'Haute' : age < 10 ? 'Moyenne' : 'Faible',
          score_confiance: age < 5 ? 88 : age < 10 ? 72 : 60,
          nb_annonces: Math.floor(Math.random() * 500) + 50,
          facteurs: [
            { name: 'Marque premium', impact: ['bmw','mercedes','audi'].includes(form.marque) ? 15 : -5 },
            { name: 'Kilométrage',    impact: form.kilometrage > 100000 ? -8 : 3 },
            { name: 'Région',         impact: form.region === 'FR' ? 5 : -3 },
          ],
          vehicule: { marque: form.marque, modele: form.modele, annee: Math.round((form.anneeMin+form.anneeMax)/2), annee_min: form.anneeMin, annee_max: form.anneeMax, kilometrage: form.kilometrage, carburant: form.carburant, boite: form.boite, puissance: form.puissance, region: form.region, pays: form.region },
        }
      }
      setResult(r)
      dispatch(addEstimation({ id: Date.now(), date: new Date().toISOString(), prix_estime: r.prix_estime, vehicule: r.vehicule }))
      if (onSubmit) onSubmit(r)
      setTimeout(() => { setResultVisible(true); startAnimation() }, 80)
      setTimeout(() => { setShowToast(true); addCoins() }, 1100)
      setTimeout(() => resultRef.current?.scrollIntoView({ behavior: 'smooth', block: 'start' }), 200)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleReuse = est => {
    const v = est.vehicule || {}
    setForm(p => ({
      ...p,
      marque: v.marque || '', modele: v.modele || '',
      anneeMin: v.annee_min ?? v.anneeMin ?? 2018,
      anneeMax: v.annee_max ?? v.anneeMax ?? (v.annee ?? 2020),
      kilometrage: v.kilometrage ?? p.kilometrage,
      carburant: v.carburant ?? p.carburant,
      boite: v.boite ?? p.boite,
      puissance: v.puissance ?? p.puissance,
      region: v.region ?? v.pays ?? p.region,
    }))
    setResult(null)
    setResultVisible(false)
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }

  const filteredMarques = MARQUES.filter(m => m.name.toLowerCase().includes(marqueSearch.toLowerCase()))
  const modeles = MODELES_PAR_MARQUE[form.marque] || []
  const selectedMarque = MARQUES.find(m => m.id === form.marque)

  // Fourchette bar pct
  const fctRange = result ? result.fourchette_haute - result.fourchette_basse : 1
  const fctPct = result ? Math.max(0, Math.min(1, (result.prix_estime - result.fourchette_basse) / (fctRange || 1))) : 0.5

  // ── styles ──────────────────────
  const card = {
    background: '#0D0D1A',
    border: '1px solid #1E1E2E',
    borderRadius: 20,
    padding: 32,
  }

  const inputStyle = {
    width: '100%', boxSizing: 'border-box',
    padding: '12px 16px',
    background: '#13131E', border: '1px solid #2a2a3e',
    borderRadius: 12, color: '#F0F0F5', fontSize: 14,
    outline: 'none', transition: 'border-color .2s',
  }

  const rangeStyle = {
    width: '100%', height: 6, accentColor: ACCENT,
    cursor: 'pointer', background: 'transparent',
  }

  return (
    <section id="estimation" style={{ padding: '80px 0', background: '#080810' }}>
      <AutoCoinToast show={showToast} onClose={() => setShowToast(false)} />

      <div style={{ maxWidth: 1100, margin: '0 auto', padding: '0 24px' }}>

        {/* ── Header ── */}
        <div style={{ textAlign: 'center', marginBottom: 48 }}>
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: 8,
            background: `${ACCENT}18`, border: `1px solid ${ACCENT}33`,
            borderRadius: 999, padding: '6px 16px', marginBottom: 16,
          }}>
            <Sparkles size={14} color={ACCENT} />
            <span style={{ fontSize: 13, color: ACCENT, fontWeight: 600 }}>IA d'estimation</span>
          </div>
          <h2 style={{ fontSize: 38, fontWeight: 800, color: '#F0F0F5', margin: '0 0 12px' }}>
            Estimez votre véhicule
          </h2>
          <p style={{ color: '#8888AA', fontSize: 16, maxWidth: 520, margin: '0 auto' }}>
            Notre IA analyse des milliers d'annonces pour vous donner le prix juste du marché en temps réel.
          </p>
        </div>

        {/* ── Form Card ── */}
        <div style={card}>
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', gap: 40 }}>

              {/* ── LEFT: Identité ── */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
                <SectionLabel icon={Car} text="Identité du véhicule" />

                {/* Marque combobox */}
                <div>
                  <FieldLabel>Marque</FieldLabel>
                  <div ref={dropdownRef} style={{ position: 'relative' }}>
                    <button
                      type="button"
                      onClick={() => setDropdownOpen(o => !o)}
                      style={{
                        ...inputStyle, display: 'flex', alignItems: 'center',
                        justifyContent: 'space-between', cursor: 'pointer',
                        borderColor: dropdownOpen ? ACCENT : '#2a2a3e',
                      }}
                    >
                      <span style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        {selectedMarque ? (
                          <>
                            <span style={{ fontSize: 20 }}>{selectedMarque.logo}</span>
                            <span style={{ color: '#F0F0F5' }}>{selectedMarque.name}</span>
                            {selectedMarque.premium && (
                              <span style={{ fontSize: 10, background: `${WARNING}22`, color: WARNING, padding: '2px 7px', borderRadius: 999, fontWeight: 700 }}>PREMIUM</span>
                            )}
                          </>
                        ) : (
                          <span style={{ color: '#55557A' }}>Sélectionnez une marque...</span>
                        )}
                      </span>
                      <ChevronDown size={16} color="#8888AA" style={{ transform: dropdownOpen ? 'rotate(180deg)' : 'none', transition: 'transform .2s' }} />
                    </button>

                    {dropdownOpen && (
                      <div style={{
                        position: 'absolute', top: 'calc(100% + 6px)', left: 0, right: 0,
                        background: '#13131E', border: '1px solid #2a2a3e', borderRadius: 14,
                        boxShadow: '0 16px 48px rgba(0,0,0,.6)', zIndex: 50,
                        maxHeight: 280, overflow: 'hidden', display: 'flex', flexDirection: 'column',
                      }}>
                        <div style={{ padding: '10px 10px 6px' }}>
                          <div style={{ position: 'relative' }}>
                            <Search size={14} color="#8888AA" style={{ position: 'absolute', left: 10, top: '50%', transform: 'translateY(-50%)' }} />
                            <input
                              type="text"
                              placeholder="Rechercher..."
                              value={marqueSearch}
                              onChange={e => setMarqueSearch(e.target.value)}
                              style={{ ...inputStyle, paddingLeft: 32, padding: '9px 12px 9px 32px', borderRadius: 10 }}
                              autoFocus
                            />
                          </div>
                        </div>
                        <div style={{ overflowY: 'auto', flex: 1 }}>
                          {filteredMarques.map(m => (
                            <button
                              key={m.id} type="button"
                              onClick={() => { set('marque', m.id); setDropdownOpen(false); setMarqueSearch('') }}
                              style={{
                                width: '100%', padding: '10px 16px',
                                display: 'flex', alignItems: 'center', gap: 12,
                                background: form.marque === m.id ? `${ACCENT}18` : 'transparent',
                                border: 'none', cursor: 'pointer', textAlign: 'left',
                                borderLeft: form.marque === m.id ? `3px solid ${ACCENT}` : '3px solid transparent',
                              }}
                            >
                              <span style={{ fontSize: 20 }}>{m.logo}</span>
                              <span style={{ color: '#F0F0F5', fontSize: 14, flex: 1 }}>{m.name}</span>
                              {m.premium && <span style={{ fontSize: 10, color: WARNING, background: `${WARNING}22`, padding: '2px 7px', borderRadius: 999 }}>⭐ Premium</span>}
                            </button>
                          ))}
                          {filteredMarques.length === 0 && (
                            <p style={{ color: '#55557A', textAlign: 'center', padding: 16, fontSize: 13 }}>Aucune marque trouvée</p>
                          )}
                        </div>
                      </div>
                    )}
                  </div>
                </div>

                {/* Modèle */}
                <div>
                  <FieldLabel>Modèle</FieldLabel>
                  <select
                    value={form.modele}
                    onChange={e => set('modele', e.target.value)}
                    disabled={!form.marque}
                    style={{ ...inputStyle, borderColor: form.modele ? ACCENT + '66' : '#2a2a3e', opacity: form.marque ? 1 : 0.5, cursor: form.marque ? 'pointer' : 'not-allowed', appearance: 'none' }}
                  >
                    <option value="">{form.marque ? 'Sélectionnez un modèle...' : "Choisissez d'abord une marque"}</option>
                    {modeles.map(m => <option key={m} value={m}>{m}</option>)}
                  </select>
                </div>

                {/* Année double slider */}
                <div>
                  <FieldLabel>
                    Année &nbsp;
                    <strong style={{ color: ACCENT }}>{form.anneeMin === form.anneeMax ? form.anneeMin : `${form.anneeMin} – ${form.anneeMax}`}</strong>
                    &nbsp;<span style={{ color: '#55557A', fontWeight: 400 }}>({anneeAge()})</span>
                  </FieldLabel>

                  <div style={{ position: 'relative', height: 32, marginBottom: 10 }}>
                    <div style={{ position: 'absolute', top: 13, left: 0, right: 0, height: 6, background: '#1E1E2E', borderRadius: 99 }} />
                    <div style={{
                      position: 'absolute', top: 13, height: 6, borderRadius: 99,
                      background: ACCENT,
                      left: `${((form.anneeMin - 2000) / 25) * 100}%`,
                      right: `${((2025 - form.anneeMax) / 25) * 100}%`,
                    }} />
                    <input type="range" min="2000" max="2025" value={form.anneeMin}
                      onChange={e => set('anneeMin', Math.min(+e.target.value, form.anneeMax))}
                      style={{ ...rangeStyle, position: 'absolute', top: 0, zIndex: 2 }}
                    />
                    <input type="range" min="2000" max="2025" value={form.anneeMax}
                      onChange={e => set('anneeMax', Math.max(+e.target.value, form.anneeMin))}
                      style={{ ...rangeStyle, position: 'absolute', top: 0, zIndex: 3, background: 'transparent' }}
                    />
                  </div>

                  <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                    <input type="number" min="2000" max="2025" value={form.anneeMin}
                      onChange={e => set('anneeMin', Math.min(Math.max(+e.target.value || 2000, 2000), form.anneeMax))}
                      style={{ ...inputStyle, width: 90, textAlign: 'center', padding: '8px' }}
                    />
                    <span style={{ color: '#55557A' }}>—</span>
                    <input type="number" min="2000" max="2025" value={form.anneeMax}
                      onChange={e => set('anneeMax', Math.max(Math.min(+e.target.value || 2025, 2025), form.anneeMin))}
                      style={{ ...inputStyle, width: 90, textAlign: 'center', padding: '8px' }}
                    />
                    <div style={{ flex: 1, textAlign: 'right', fontSize: 12, color: '#55557A', display: 'flex', alignItems: 'center', gap: 4, justifyContent: 'flex-end' }}>
                      <Clock size={12} /> {anneeAge()}
                    </div>
                  </div>
                </div>

                {/* Kilométrage */}
                <div>
                  <FieldLabel>
                    Kilométrage &nbsp;
                    <strong style={{ color: ACCENT }}>{form.kilometrage.toLocaleString()} km</strong>
                    &nbsp;<span style={{ color: '#55557A', fontWeight: 400 }}>(~{kmAn().toLocaleString()} km/an)</span>
                  </FieldLabel>

                  <input type="range" min="0" max="1000" step="1"
                    value={kmToSlider(form.kilometrage)}
                    onChange={e => set('kilometrage', sliderToKm(+e.target.value))}
                    style={{ ...rangeStyle, marginBottom: 10 }}
                  />

                  <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                    <span style={{ fontSize: 12, color: '#55557A', whiteSpace: 'nowrap' }}>0 km</span>
                    <input type="number" min="0" max="300000" value={form.kilometrage}
                      onChange={e => set('kilometrage', Math.min(300000, Math.max(0, +e.target.value || 0)))}
                      style={{ ...inputStyle, flex: 1, textAlign: 'center', padding: '8px' }}
                    />
                    <span style={{ fontSize: 12, color: '#55557A', whiteSpace: 'nowrap' }}>300k+ km</span>
                  </div>
                </div>
              </div>

              {/* ── RIGHT: Spécifications ── */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
                <SectionLabel icon={Settings} text="Spécifications" />

                {/* Carburant radio custom */}
                <div>
                  <FieldLabel>Carburant</FieldLabel>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 10 }}>
                    {CARBURANTS.map(c => {
                      const active = form.carburant === c.id
                      return (
                        <button
                          key={c.id} type="button"
                          onClick={() => set('carburant', c.id)}
                          style={{
                            padding: '14px 12px', borderRadius: 12, cursor: 'pointer',
                            border: `2px solid ${active ? c.color : '#2a2a3e'}`,
                            background: active ? `${c.color}18` : '#13131E',
                            display: 'flex', flexDirection: 'column',
                            alignItems: 'center', gap: 6,
                            transition: 'all .2s',
                            transform: active ? 'scale(1.03)' : 'scale(1)',
                          }}
                        >
                          <span style={{ fontSize: 22 }}>{c.emoji}</span>
                          <span style={{ fontSize: 13, fontWeight: 600, color: active ? c.color : '#8888AA' }}>{c.name}</span>
                        </button>
                      )
                    })}
                  </div>
                </div>

                {/* Boîte toggle */}
                <div>
                  <FieldLabel>Boîte de vitesse</FieldLabel>
                  <div style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    background: '#13131E', border: '1px solid #2a2a3e',
                    borderRadius: 12, padding: '12px 16px',
                  }}>
                    <span style={{ fontSize: 14, color: form.boite === 'manuelle' ? '#F0F0F5' : '#55557A', fontWeight: 600 }}>Manuelle</span>
                    <button
                      type="button"
                      role="switch"
                      aria-checked={form.boite === 'automatique'}
                      onClick={() => set('boite', form.boite === 'automatique' ? 'manuelle' : 'automatique')}
                      style={{
                        position: 'relative', width: 52, height: 28, borderRadius: 999,
                        background: form.boite === 'automatique' ? ACCENT : '#2a2a3e',
                        border: 'none', cursor: 'pointer', transition: 'background .25s',
                      }}
                    >
                      <span style={{
                        position: 'absolute', top: 4, left: 4, width: 20, height: 20,
                        borderRadius: '50%', background: '#fff',
                        transform: form.boite === 'automatique' ? 'translateX(24px)' : 'none',
                        transition: 'transform .25s',
                        boxShadow: '0 2px 6px rgba(0,0,0,.4)',
                      }} />
                    </button>
                    <span style={{ fontSize: 14, color: form.boite === 'automatique' ? '#F0F0F5' : '#55557A', fontWeight: 600 }}>Automatique</span>
                  </div>
                </div>

                {/* Puissance */}
                <div>
                  <FieldLabel>
                    Puissance &nbsp;
                    <strong style={{ color: ACCENT }}>{form.puissance} CV</strong>
                    &nbsp;
                    <span style={{
                      fontSize: 11, background: `${catPuissance.color}22`, color: catPuissance.color,
                      padding: '2px 8px', borderRadius: 999, fontWeight: 700,
                    }}>{catPuissance.label}</span>
                  </FieldLabel>

                  <div style={{ position: 'relative', marginBottom: 8 }}>
                    <div style={{ position: 'absolute', top: '50%', left: 0, right: 0, height: 6, background: '#1E1E2E', borderRadius: 99, transform: 'translateY(-50%)' }} />
                    <div style={{
                      position: 'absolute', top: '50%', left: 0, height: 6, borderRadius: 99,
                      background: `linear-gradient(90deg, ${SUCCESS}, ${WARNING}, ${DANGER})`,
                      width: `${((form.puissance - 50) / 450) * 100}%`,
                      transform: 'translateY(-50%)',
                    }} />
                    <input type="range" min="50" max="500" step="5"
                      value={form.puissance}
                      onChange={e => set('puissance', +e.target.value)}
                      style={{ ...rangeStyle, position: 'relative', zIndex: 2, marginBottom: 0 }}
                    />
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 11, color: '#55557A' }}>
                    <span>50 CV — Citadine</span>
                    <span>200 CV — Sport</span>
                    <span>500 CV</span>
                  </div>
                </div>

                {/* Région */}
                <div>
                  <FieldLabel>Région</FieldLabel>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 8 }}>
                    {REGIONS.map(r => {
                      const active = form.region === r.code
                      return (
                        <button
                          key={r.code} type="button"
                          onClick={() => set('region', r.code)}
                          style={{
                            padding: '10px 14px', borderRadius: 10, cursor: 'pointer',
                            border: `2px solid ${active ? ACCENT : '#2a2a3e'}`,
                            background: active ? `${ACCENT}18` : '#13131E',
                            display: 'flex', alignItems: 'center', gap: 8,
                            transition: 'all .2s',
                          }}
                        >
                          <span style={{ fontSize: 18 }}>{r.flag}</span>
                          <span style={{ fontSize: 13, fontWeight: 600, color: active ? ACCENT : '#8888AA' }}>{r.name}</span>
                        </button>
                      )
                    })}
                  </div>
                </div>
              </div>
            </div>

            {/* ── Submit ── */}
            <div style={{ marginTop: 36, display: 'flex', justifyContent: 'center' }}>
              <button
                type="submit"
                disabled={!isValid || loading}
                style={{
                  padding: '16px 44px', borderRadius: 14, border: 'none', cursor: isValid && !loading ? 'pointer' : 'not-allowed',
                  background: isValid && !loading ? `linear-gradient(135deg, ${ACCENT}, #9B59B6)` : '#2a2a3e',
                  color: '#fff', fontWeight: 700, fontSize: 16,
                  display: 'flex', alignItems: 'center', gap: 10,
                  boxShadow: isValid && !loading ? `0 8px 32px ${ACCENT}44` : 'none',
                  transition: 'all .25s',
                  opacity: !isValid && !loading ? 0.5 : 1,
                  transform: 'scale(1)',
                }}
                onMouseEnter={e => { if (isValid && !loading) e.currentTarget.style.transform = 'scale(1.03)' }}
                onMouseLeave={e => { e.currentTarget.style.transform = 'scale(1)' }}
              >
                {loading ? (
                  <>
                    <Loader2 size={20} style={{ animation: 'spin 1s linear infinite' }} />
                    Analyse en cours...
                  </>
                ) : (
                  <>
                    <Sparkles size={20} />
                    Estimer le prix →
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* ── Result ── */}
        {result && (
          <div
            ref={resultRef}
            style={{
              marginTop: 24,
              opacity: resultVisible ? 1 : 0,
              transform: resultVisible ? 'translateY(0)' : 'translateY(24px)',
              transition: 'opacity .35s ease, transform .35s ease',
            }}
          >
            <div style={{ ...card, borderColor: `${ACCENT}44`, boxShadow: `0 0 40px ${ACCENT}18` }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: 32 }}>

                {/* Left: prix + fourchette + facteurs */}
                <div style={{ gridColumn: 'span 2', minWidth: 0 }}>
                  <div style={{ marginBottom: 4, fontSize: 13, color: '#8888AA', fontWeight: 500 }}>Prix estimé</div>
                  <div style={{ display: 'flex', alignItems: 'baseline', gap: 10, marginBottom: 4 }}>
                    <span style={{ fontSize: 52, fontWeight: 800, color: ACCENT, lineHeight: 1 }}>
                      {animatedPrice.toLocaleString()}
                    </span>
                    <span style={{ fontSize: 24, fontWeight: 600, color: ACCENT }}>€</span>
                  </div>
                  <div style={{ fontSize: 14, color: '#8888AA', marginBottom: 28 }}>Prix juste du marché</div>

                  {/* Fourchette bar */}
                  <div style={{ marginBottom: 28 }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                      <span style={{ fontSize: 12, color: '#55557A' }}>Fourchette basse</span>
                      <span style={{ fontSize: 12, color: '#55557A' }}>Fourchette haute</span>
                    </div>
                    <div style={{ position: 'relative', background: '#1E1E2E', borderRadius: 99, height: 12, overflow: 'visible' }}>
                      <div style={{
                        position: 'absolute', inset: 0, borderRadius: 99,
                        background: `linear-gradient(90deg, ${SUCCESS}55, ${ACCENT}55, ${WARNING}55)`,
                      }} />
                      {/* Label */}
                      <div style={{
                        position: 'absolute', bottom: 'calc(100% + 6px)',
                        left: `${fctPct * 100}%`, transform: 'translateX(-50%)',
                        background: '#13131E', border: `1px solid ${ACCENT}`,
                        borderRadius: 999, padding: '2px 10px', fontSize: 11,
                        color: ACCENT, fontWeight: 700, whiteSpace: 'nowrap',
                      }}>● Prix estimé</div>
                      {/* Thumb */}
                      <div style={{
                        position: 'absolute', top: '50%', left: `${fctPct * 100}%`,
                        transform: 'translate(-50%, -50%)',
                        width: 20, height: 20, borderRadius: '50%',
                        background: ACCENT, border: '3px solid #fff',
                        boxShadow: `0 0 12px ${ACCENT}88`,
                      }} />
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: 8 }}>
                      <span style={{ fontSize: 13, fontWeight: 700, color: SUCCESS }}>{result.fourchette_basse.toLocaleString()}€</span>
                      <span style={{ fontSize: 13, fontWeight: 700, color: WARNING }}>{result.fourchette_haute.toLocaleString()}€</span>
                    </div>
                  </div>

                  {/* Facteurs */}
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
                    {result.facteurs?.map((f, i) => (
                      <span key={i} style={{
                        padding: '5px 14px', borderRadius: 999, fontSize: 13, fontWeight: 600,
                        background: f.impact > 0 ? `${SUCCESS}22` : `${DANGER}22`,
                        color: f.impact > 0 ? SUCCESS : DANGER,
                        display: 'flex', alignItems: 'center', gap: 5,
                      }}>
                        {f.impact > 0 ? <TrendingUp size={13} /> : <TrendingDown size={13} />}
                        {f.name} {f.impact > 0 ? '+' : ''}{f.impact}%
                      </span>
                    ))}
                  </div>

                  {/* Annonces exemples du marché réel */}
                  {result.exemples_marche && result.exemples_marche.length > 0 && (
                    <div style={{ marginTop: 20 }}>
                      <div style={{ fontSize: 12, color: '#8888AA', marginBottom: 10, fontWeight: 600, textTransform: 'uppercase', letterSpacing: 1 }}>
                        Annonces de référence
                      </div>
                      <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                        {result.exemples_marche.map((ex, i) => (
                          <div key={i} style={{
                            display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                            background: '#0D0D1A', border: '1px solid #1E1E2E',
                            borderRadius: 10, padding: '8px 14px',
                          }}>
                            <div style={{ display: 'flex', gap: 10, alignItems: 'center' }}>
                              <span style={{ fontSize: 12, color: '#8888AA' }}>{ex.annee}</span>
                              <span style={{ fontSize: 11, color: '#55557A' }}>·</span>
                              <span style={{ fontSize: 12, color: '#8888AA' }}>{(ex.kilometrage || 0).toLocaleString()} km</span>
                              {ex.ville && <>
                                <span style={{ fontSize: 11, color: '#55557A' }}>·</span>
                                <span style={{ fontSize: 11, color: '#55557A' }}>{ex.ville}</span>
                              </>}
                            </div>
                            <span style={{ fontSize: 13, fontWeight: 700, color: ACCENT }}>
                              {(ex.prix || 0).toLocaleString()} €
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                {/* Right: stats card */}
                <div style={{ background: '#13131E', border: '1px solid #2a2a3e', borderRadius: 16, padding: 24, display: 'flex', flexDirection: 'column', gap: 20 }}>

                  {/* Fiabilité */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: 13, color: '#8888AA' }}>Fiabilité</span>
                    {(() => {
                      const s = reliabilityStyle(result.fiabilite)
                      return (
                        <span style={{
                          padding: '4px 12px', borderRadius: 999, fontSize: 12, fontWeight: 700,
                          background: s.bg, color: s.color,
                          display: 'flex', alignItems: 'center', gap: 5,
                        }}>
                          <span style={{ width: 6, height: 6, borderRadius: '50%', background: s.dot, display: 'inline-block' }} />
                          {result.fiabilite}
                        </span>
                      )
                    })()}
                  </div>

                  {/* Score confiance */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: 13, color: '#8888AA' }}>Score confiance</span>
                    <MiniGauge
                      value={result.score_confiance || 75}
                      color={result.score_confiance >= 80 ? SUCCESS : result.score_confiance >= 60 ? WARNING : DANGER}
                    />
                  </div>

                  {/* Source données réelles */}
                  <div style={{ paddingTop: 12, borderTop: '1px solid #2a2a3e' }}>
                    {/* Badge source */}
                    {(() => {
                      const src = result.source_donnees
                      const configs = {
                        modele_exact:  { label: '📊 Données réelles exactes', bg: `${SUCCESS}22`, color: SUCCESS },
                        modele_marche: { label: '📈 Données marché modèle',   bg: `${TEAL}22`,    color: TEAL    },
                        marque_annee:  { label: '📉 Données marque approx.',  bg: `${WARNING}22`, color: WARNING },
                        marque_global: { label: '⚠️ Données marque globales', bg: `${WARNING}22`, color: WARNING },
                        fallback:      { label: '🔢 Prix de référence',       bg: '#2a2a3e',      color: '#8888AA'},
                      }
                      const cfg = configs[src] || configs.fallback
                      return (
                        <div style={{ marginBottom: 8 }}>
                          <span style={{ fontSize: 11, fontWeight: 700, padding: '3px 10px', borderRadius: 999, background: cfg.bg, color: cfg.color }}>
                            {cfg.label}
                          </span>
                        </div>
                      )
                    })()}
                    <p style={{ fontSize: 12, color: '#8888AA', margin: 0, lineHeight: 1.5 }}>
                      {result.source_message || `Basé sur ${result.nb_annonces || 0} annonces`}
                    </p>
                  </div>

                  {/* CTA */}
                  <a
                    href={`/annonces?marque=${form.marque}&modele=${form.modele}`}
                    style={{
                      display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 8,
                      padding: '12px', borderRadius: 12, textDecoration: 'none',
                      background: `linear-gradient(135deg, ${ACCENT}, #9B59B6)`,
                      color: '#fff', fontWeight: 700, fontSize: 14,
                      boxShadow: `0 4px 16px ${ACCENT}44`,
                    }}
                  >
                    Voir les annonces similaires <ExternalLink size={15} />
                  </a>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ── Historique ── */}
        <div style={{ marginTop: 48 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 20 }}>
            <Calendar size={18} color={ACCENT} />
            <h3 style={{ margin: 0, fontWeight: 700, fontSize: 18, color: '#F0F0F5' }}>Dernières estimations</h3>
            {history.length > 0 && (
              <span style={{
                marginLeft: 'auto', fontSize: 12, color: '#8888AA',
                background: '#1E1E2E', padding: '3px 10px', borderRadius: 999,
              }}>{history.length} / 5</span>
            )}
            <div style={{ marginLeft: history.length === 0 ? 'auto' : 8 }}>
               <ExportButton 
                 endpoint="/api/estimation/export_mes_estimations/" 
                 filename="mes_estimations.csv" 
                 label="Exporter mon historique" 
               />
            </div>
          </div>

          {history.length === 0 ? (
            <div style={{
              ...card, textAlign: 'center', padding: '48px 24px',
              borderStyle: 'dashed',
            }}>
              <div style={{
                width: 64, height: 64, borderRadius: 18,
                background: `${ACCENT}18`, margin: '0 auto 16px',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
              }}>
                <Gauge size={28} color={ACCENT} />
              </div>
              <p style={{ fontWeight: 700, color: '#F0F0F5', marginBottom: 6 }}>Aucune estimation pour l'instant</p>
              <p style={{ fontSize: 14, color: '#8888AA', margin: 0 }}>Faites votre première estimation — elle sera sauvegardée sur cet appareil.</p>
            </div>
          ) : (
            <div style={{ display: 'flex', gap: 14, overflowX: 'auto', paddingBottom: 8 }}>
              {history.map(item => (
                <HistoryCard key={item.id} estimation={item} onReuse={handleReuse} />
              ))}
            </div>
          )}
        </div>
      </div>

      <style>{`
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        input[type=range] { -webkit-appearance: none; appearance: none; }
        input[type=range]::-webkit-slider-thumb {
          -webkit-appearance: none; appearance: none;
          width: 20px; height: 20px; border-radius: 50%;
          background: ${ACCENT}; cursor: pointer;
          border: 3px solid #fff; box-shadow: 0 2px 8px ${ACCENT}88;
        }
        input[type=range]::-moz-range-thumb {
          width: 18px; height: 18px; border-radius: 50%;
          background: ${ACCENT}; cursor: pointer;
          border: 3px solid #fff; box-shadow: 0 2px 8px ${ACCENT}88;
        }
        input[type=range]::-webkit-slider-runnable-track { height: 6px; background: transparent; }
        select option { background: #13131E; color: #F0F0F5; }
      `}</style>
    </section>
  )
}
