import { configureStore } from '@reduxjs/toolkit'
import estimationHistoryReducer from './estimationHistorySlice'
import userReducer from './userSlice'

export const store = configureStore({
  reducer: {
    estimationHistory: estimationHistoryReducer,
    user: userReducer
  }
})
