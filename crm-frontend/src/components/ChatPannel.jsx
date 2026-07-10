import { useDispatch, useSelector } from "react-redux";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";
import { addUserMessage, sendMessage } from "../store/chatSlice";
import { setFormData } from "../store/form_slice";
import { LiaRobotSolid } from "react-icons/lia";

const ChatPannel = () => {
  const dispatch = useDispatch()
  const messages = useSelector((state) => state.chat.messages)
  const pending = useSelector((state) => state.chat.pending)
  const error = useSelector((state) => state.chat.error)

  const handleSend = async (text) => {
    const history = messages.map(({ role, content }) => ({ role, content }))
    dispatch(addUserMessage(text))
    const result = await dispatch(sendMessage({ text, history }))

    const toolResults = result.payload?.tool_results ?? []
    const withFormData = toolResults.find((r) => r?.output?.form_data)
    if (withFormData) {
      dispatch(setFormData(withFormData.output.form_data))
    }
  }

  return (
   <div className="flex h-full bg-secondary w-[60%] p-5 rounded-md flex-col">
    <span className="text-surface-muted items-center gap-4 flex inline-[40%] text-lg font-light bg-secondary-700 px-3 py-1 rounded-md">
      Chat with your AI HCP Agent!! 
      <LiaRobotSolid size={32} className="bg-assistant-600 p-1 rounded-full"/>
      </span>

      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.map((m, i) => (
          <MessageBubble key={i} role={m.role} content={m.content} />
        ))}
        {pending && <div className="text-sm text-[var(--ink-muted)]">Thinking...</div>}
        {error && <div className="text-sm text-red-600">{error}</div>}
      </div>
      <ChatInput onSend={handleSend} disabled={pending} />
    </div>
  );
};

export default ChatPannel;
