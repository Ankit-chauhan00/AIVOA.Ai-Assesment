import { configureStore } from '@reduxjs/toolkit'
import chatReducer from './chatSlice'
import formReducer from './form_slice'

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    form: formReducer,
  },
})