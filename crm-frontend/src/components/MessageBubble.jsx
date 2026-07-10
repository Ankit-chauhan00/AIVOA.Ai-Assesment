import { FaUser, FaBrain } from 'react-icons/fa'

const MessageBubble = ({ role, content }) => {
  const isUser = role === 'user'

  return (
    <div className={`flex items-end gap-2 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <FaBrain
          size={32}
          className="text-assistant-600 bg-assistant-50 p-1.5 rounded-full shrink-0"
        />
      )}

      <div
        className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm ${
          isUser
            ? 'bg-clinical-600 text-white'
            : 'bg-assistant-100 text-ink'
        }`}
      >
        {content}
      </div>

      {isUser && (
        <FaUser
          size={32}
          className="text-white bg-clinical-100 p-1.5 rounded-full shrink-0"
        />
      )}
    </div>
  )
}

export default MessageBubble