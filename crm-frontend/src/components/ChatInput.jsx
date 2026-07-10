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

  return <div className="flex gap-2  bg-secondary-700 rounded-md p-3">
      <textarea
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={disabled}
        rows={1}
        placeholder="Log a visit or ask something..."
        className="flex-1 resize-none rounded-xl border border-ink-muted  bg-secondary-500 px-3 py-2 text-sm  outline-none"
      />
      <button
        onClick={submit}
        disabled={disabled || !value.trim()}
        className="rounded-xl  px-4 py-2 text-sm text-white disabled:opacity-40 border border-ink-faint bg-clinical-600 hover:scale-95"
      >
        Send
      </button>
    </div>;
};

export default ChatInput;
