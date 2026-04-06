import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// --- THUNKS Async ---

export const loginUser = createAsyncThunk(
  'user/login',
  async ({ email, password }, { rejectWithValue, dispatch }) => {
    try {
      const response = await fetch(`${API_URL}/api/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })

      if (!response.ok) {
        const errorData = await response.json()
        return rejectWithValue(errorData.detail || 'Erreur de connexion')
      }

      const tokens = await response.json()
      // tokens.access et tokens.refresh 
      
      // Récupérer le profile complet avec le token nouvellement créé
      const profileResponse = await fetch(`${API_URL}/api/auth/profile/`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${tokens.access}`
        }
      })
      
      if (!profileResponse.ok) {
        return rejectWithValue('Erreur lors du chargement du profil')
      }
      
      const profileData = await profileResponse.json()

      return {
        tokens,
        ...profileData
      }
    } catch (err) {
      return rejectWithValue(err.message || 'Erreur de connexion serveur')
    }
  }
)

export const registerUser = createAsyncThunk(
  'user/register',
  async (userData, { rejectWithValue }) => {
    try {
      const response = await fetch(`${API_URL}/api/auth/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        // Convert array messages or object to string
        const errorMsg = Object.values(errorData).flat().join(', ') || 'Erreur d\'inscription'
        return rejectWithValue(errorMsg)
      }

      const data = await response.json()
      // data: access_token, refresh_token, user_data, profil_data

      return {
        tokens: {
          access: data.access_token,
          refresh: data.refresh_token
        },
        user: data.user_data,
        profil: data.profil_data,
        abonnement: null // Sera chargé plus tard ou au rafraichissement
      }
    } catch (err) {
      return rejectWithValue(err.message || 'Erreur serveur')
    }
  }
)

export const fetchProfile = createAsyncThunk(
  'user/fetchProfile',
  async (_, { getState, rejectWithValue }) => {
    const { user } = getState()
    const token = user.accessToken

    if (!token) return rejectWithValue('Aucun token')

    try {
      const response = await fetch(`${API_URL}/api/auth/profile/`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      
      if (!response.ok) {
        // Optionnel : Gérer le refresh token ici si 401
        return rejectWithValue('Session expirée')
      }
      
      return await response.json()
    } catch (err) {
      return rejectWithValue(err.message)
    }
  }
)

export const updateProfile = createAsyncThunk(
  'user/updateProfile',
  async (profileData, { getState, rejectWithValue }) => {
    const { user } = getState()
    const token = user.accessToken
    try {
      const response = await fetch(`${API_URL}/api/auth/profile/`, {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(profileData)
      })
      if (!response.ok) throw new Error('Update failed')
      return await response.json()
    } catch (err) {
      return rejectWithValue(err.message)
    }
  }
)


// Load tokens from localStorage
const storedAccess = localStorage.getItem('access_token')
const storedRefresh = localStorage.getItem('refresh_token')

const initialState = {
  user: null,
  profil: {
    xp: 0,
    niveau: 1,
    autocoin_balance: 0,
    nom_niveau: 'Inconnu',
    progression_pct: 0
  },
  abonnement: null,
  accessToken: storedAccess,
  refreshToken: storedRefresh,
  isAuthenticated: !!storedAccess,
  loading: false,
  error: null
}

const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    logoutUser: (state) => {
      state.user = null
      state.profil = initialState.profil
      state.abonnement = null
      state.accessToken = null
      state.refreshToken = null
      state.isAuthenticated = false
      state.loading = false
      state.error = null
      
      // Cleanup localStorage
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    },
    clearError: (state) => {
      state.error = null
    }
  },
  extraReducers: (builder) => {
    builder
      // Login
      .addCase(loginUser.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(loginUser.fulfilled, (state, action) => {
        state.loading = false
        state.isAuthenticated = true
        state.accessToken = action.payload.tokens.access
        state.refreshToken = action.payload.tokens.refresh
        state.user = action.payload.user
        state.profil = action.payload.profil || state.profil
        state.abonnement = action.payload.abonnement || null

        // Store tokens
        localStorage.setItem('access_token', state.accessToken)
        localStorage.setItem('refresh_token', state.refreshToken)
      })
      .addCase(loginUser.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })

      // Register
      .addCase(registerUser.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(registerUser.fulfilled, (state, action) => {
        state.loading = false
        state.isAuthenticated = true
        state.accessToken = action.payload.tokens.access
        state.refreshToken = action.payload.tokens.refresh
        state.user = action.payload.user
        state.profil = action.payload.profil || state.profil
        state.abonnement = action.payload.abonnement || null

        // Store tokens
        localStorage.setItem('access_token', state.accessToken)
        localStorage.setItem('refresh_token', state.refreshToken)
      })
      .addCase(registerUser.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })

      // Fetch Profile
      .addCase(fetchProfile.fulfilled, (state, action) => {
        state.user = action.payload.user
        state.profil = action.payload.profil || state.profil
        state.abonnement = action.payload.abonnement || null
      })
      .addCase(fetchProfile.rejected, (state) => {
        // Si récupération échoue, on déconnecte
        state.isAuthenticated = false
        state.accessToken = null
        state.refreshToken = null
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      })
      
      // Update Profile
      .addCase(updateProfile.fulfilled, (state, action) => {
        state.user = action.payload.user
        state.profil = action.payload.profil || state.profil
      })
  }
})

export const { logoutUser, clearError } = userSlice.actions
export default userSlice.reducer
