import { useDispatch, useSelector } from "react-redux";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";
import { addUserMessage, sendMessage } from "../store/chatSlice";

const ChatPannel = () => {
  const dispatch = useDispatch();

  const messages = useSelector((state) => state.chat.messages);
  const pending = useSelector((state) => state.chat.pending);
  const error = useSelector((state) => state.chat.error);

  const handleSend = (text) => {
    const history = messages.map(({ role, content }) => ({ role, content }));
    dispatch(addUserMessage(text));
    dispatch(sendMessage({ text, history }));
  };

  return (
    <div className="flex h-full flex-col">
      <div className="flex-1 space-y-3 overflow-y-auto p-4">
        {messages.map((m, i) => (
          <MessageBubble key={i} role={m.role} content={m.content} />
        ))}

        {pending && (
          <div className="text-sm text-[var(--ink-muted)]">Thinking...</div>
        )}

        {error && (
          <div className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
            {error}
          </div>
        )}
      </div>

      <ChatInput onSend={handleSend} disabled={pending} />
    </div>
  );
};

export default ChatPannel;
