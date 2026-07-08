import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { sendChatMessage } from '../lib/api'

export const sendMessage = createAsyncThunk(
  'chat/sendMessage',
  async ({ text, history }) => {
    const response = await sendChatMessage(text, history)
    return response
  }
)

const chatSlice = createSlice({
  name: 'chat',
  initialState: {
    messages: [],
    pending: false,
    error: null,
  },
  reducers: {
    addUserMessage: (state, action) => {
      state.messages.push({ role: 'user', content: action.payload })
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => {
        state.pending = true
        state.error = null
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.pending = false
        state.messages.push({
          role: 'assistant',
          content: action.payload.reply,
          toolCalls: action.payload.tool_calls ?? [],
          toolResults: action.payload.tool_results ?? [],
          trace: action.payload.execution_trace ?? [],
        })
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.pending = false
        state.error = action.error.message
      })
  },
})

export const { addUserMessage } = chatSlice.actions
export default chatSlice.reducer