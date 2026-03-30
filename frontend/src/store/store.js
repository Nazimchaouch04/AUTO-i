import { configureStore } from '@reduxjs/toolkit'
import estimationHistoryReducer from './estimationHistorySlice'

export const store = configureStore({
  reducer: {
    estimationHistory: estimationHistoryReducer
  }
})
