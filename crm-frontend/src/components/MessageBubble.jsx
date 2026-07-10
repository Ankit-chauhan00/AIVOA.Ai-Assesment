

const MessageBubble = ({role, content}) => {
    const isUser = role === 'user'
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] bg-clinical-600 rounded-2xl px-4 py-2.5 text-sm ${
          isUser
            ? 'bg-[var(--clinical)] text-white'
            : 'bg-[var(--assistant)]/10 text-[var(--ink)]'
        }`}
      >
        {content}
      </div>
    </div>
  )
}

export default MessageBubble