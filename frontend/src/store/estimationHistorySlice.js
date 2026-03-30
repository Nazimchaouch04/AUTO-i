import { createSlice } from '@reduxjs/toolkit'

const STORAGE_KEY = 'estimation_history_v1'

const loadInitialState = () => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return { items: [] }
    const parsed = JSON.parse(raw)
    if (!parsed || !Array.isArray(parsed.items)) return { items: [] }
    return { items: parsed.items }
  } catch {
    return { items: [] }
  }
}

const initialState = typeof window !== 'undefined' ? loadInitialState() : { items: [] }

const estimationHistorySlice = createSlice({
  name: 'estimationHistory',
  initialState,
  reducers: {
    addEstimation(state, action) {
      const entry = action.payload
      state.items = [entry, ...state.items].slice(0, 5)
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({ items: state.items }))
      } catch {
        // ignore
      }
    },
    setEstimations(state, action) {
      state.items = Array.isArray(action.payload) ? action.payload.slice(0, 5) : []
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify({ items: state.items }))
      } catch {
        // ignore
      }
    },
    clearHistory(state) {
      state.items = []
      try {
        localStorage.removeItem(STORAGE_KEY)
      } catch {
        // ignore
      }
    }
  }
})

export const { addEstimation, setEstimations, clearHistory } = estimationHistorySlice.actions
export default estimationHistorySlice.reducer
