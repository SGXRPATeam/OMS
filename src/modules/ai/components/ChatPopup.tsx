"use client";

import { useState } from "react";
import { Sparkles, Send } from "lucide-react";
import { getBotReply } from "../mock/botReplies";

type Props = {
  open: boolean;
};

type Message = {
  sender: "user" | "bot";
  text: string;
};

export default function ChatPopup({ open }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    {
      sender: "bot",
      text: "Hello! 👋 I'm your AI-powered OMS assistant. How can I help?",
    },
  ]);

  const [input, setInput] = useState("");

  const sendMessage = (text: string) => {
    if (!text.trim()) return;

    const reply = getBotReply(text);

    setMessages((prev) => [
      ...prev,
      { sender: "user", text },
      { sender: "bot", text: reply },
    ]);

    setInput("");
  };

  if (!open) return null;

  return (
    <div className="fixed bottom-24 right-6 w-[360px] bg-white rounded-2xl shadow-2xl border z-50 overflow-hidden">
      
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-4 py-3">
        <div className="flex items-center gap-2">
          <Sparkles size={18} />
          <span className="font-medium">Always Active • Powered by AI</span>
        </div>
      </div>

      {/* Messages */}
      <div className="h-[350px] overflow-y-auto p-4 space-y-3">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`max-w-[85%] p-3 rounded-xl text-sm ${
              msg.sender === "bot"
                ? "bg-gray-100"
                : "bg-primary text-white ml-auto"
            }`}
          >
            {msg.text}
          </div>
        ))}

        {/* Quick actions */}
        <div className="space-y-2 pt-2">
          <button
            onClick={() => sendMessage("track")}
            className="w-full border rounded-xl p-3 text-left hover:bg-gray-50"
          >
            📦 Track my order
          </button>

          <button
            onClick={() => sendMessage("create")}
            className="w-full border rounded-xl p-3 text-left hover:bg-gray-50"
          >
            ➕ Create a new order
          </button>

          <button
            onClick={() => sendMessage("complaint")}
            className="w-full border rounded-xl p-3 text-left hover:bg-gray-50"
          >
            ⚠ Raise a complaint
          </button>
        </div>
      </div>

      {/* Input */}
      <div className="border-t p-3 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask me anything..."
          className="flex-1 border rounded-lg px-3 py-2 text-sm outline-none"
          onKeyDown={(e) => e.key === "Enter" && sendMessage(input)}
        />

        <button
          onClick={() => sendMessage(input)}
          className="bg-primary text-white px-3 rounded-lg"
        >
          <Send size={16} />
        </button>
      </div>
    </div>
  );
}