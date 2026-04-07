import { configureStore } from '@reduxjs/toolkit';
import userReducer from './userSlice';

// Importe les autres slices s'ils existent
let annoncesReducer;
let gamificationReducer;
try {
  annoncesReducer = require('./annoncesSlice').default;
} catch (e) {}
try {
  gamificationReducer = require('./gamificationSlice').default;
} catch (e) {}

const reducers = { user: userReducer };
if (annoncesReducer) reducers.annonces = annoncesReducer;
if (gamificationReducer) reducers.gamification = gamificationReducer;

export const store = configureStore({ reducer: reducers });
export default store;
