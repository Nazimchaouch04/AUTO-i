import { createSlice } from '@reduxjs/toolkit';

const getInitialState = () => {
  const token = localStorage.getItem('access_token');
  return {
    user: null,
    profil: null,
    abonnement: null,
    accessToken: token || null,
    refreshToken: localStorage.getItem('refresh_token') || null,
    isAuthenticated: !!token,
    loading: false,
    error: null,
  };
};

const userSlice = createSlice({
  name: 'user',
  initialState: getInitialState(),
  reducers: {
    setCredentials: (state, action) => {
      const { user, profil, abonnement, access, refresh } = action.payload;
      state.user = user;
      state.profil = profil || null;
      state.abonnement = abonnement || null;
      state.accessToken = access;
      state.refreshToken = refresh;
      state.isAuthenticated = true;
      state.error = null;
      localStorage.setItem('access_token', access);
      if (refresh) localStorage.setItem('refresh_token', refresh);
    },
    logout: (state) => {
      state.user = null;
      state.profil = null;
      state.abonnement = null;
      state.accessToken = null;
      state.refreshToken = null;
      state.isAuthenticated = false;
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
    },
    updateProfil: (state, action) => {
      state.profil = { ...state.profil, ...action.payload };
    },
    setLoading: (state, action) => {
      state.loading = action.payload;
    },
    setError: (state, action) => {
      state.error = action.payload;
      state.loading = false;
    },
  },
});

export const {
  setCredentials,
  logout,
  updateProfil,
  setLoading,
  setError,
} = userSlice.actions;
export default userSlice.reducer;
