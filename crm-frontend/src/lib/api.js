import axios from 'axios'

const client = axios.create({
  baseURL: '',
  timeout: 30000,
  headers: { 'Content-Type': 'application/json' },
})

export async function sendChatMessage(message, history = []) {
  const formattedHistory = history.map((h) => [h.role, h.content])
  const { data } = await client.post('/chat', { message, history: formattedHistory })
  return data
}