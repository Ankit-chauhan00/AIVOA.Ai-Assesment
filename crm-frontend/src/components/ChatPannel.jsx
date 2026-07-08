import { useDispatch, useSelector } from "react-redux";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";
import { addUserMessage, sendMessage } from "../store/chatSlice";
import { setFormData } from "../store/form_slice";

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
   <div className="flex h-full flex-col">
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
