import { useState } from "react";

const ChatInput = ({ onSend, disabled }) => {
  const [value, setValue] = useState("");

  const submit = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  return <div className="flex gap-2 border-t border-[var(--border)] p-3">
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        rows={1}
        placeholder="Log a visit or ask something..."
        className="flex-1 resize-none rounded-xl border border-[var(--border)] px-3 py-2 text-sm focus:border-[var(--assistant)] outline-none"
      />
      <button
        onClick={submit}
        disabled={disabled || !value.trim()}
        className="rounded-xl bg-[var(--assistant)] px-4 py-2 text-sm text-white disabled:opacity-40"
      >
        Send
      </button>
    </div>;
};

export default ChatInput;
