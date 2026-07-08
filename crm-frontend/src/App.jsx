

import ChatPannel from './components/ChatPannel'
import InteractionForm from './components/InteractionForm'


const App = () => {
  return (
    <div className="grid h-screen grid-cols-1 md:grid-cols-2">
      <InteractionForm />
      <ChatPannel />
    </div>
  )
}

export default App