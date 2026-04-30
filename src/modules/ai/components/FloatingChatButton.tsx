"use client";

import { useState } from "react";
import { MessageCircle } from "lucide-react";
import ChatPopup from "./ChatPopup";

export default function FloatingChatButton() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <ChatPopup open={open} />

      <button
        onClick={() => setOpen(!open)}
        className="fixed bottom-6 right-6 w-16 h-16 rounded-full bg-primary text-white shadow-2xl flex items-center justify-center z-50"
      >
        <MessageCircle size={28} />

        <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs w-6 h-6 rounded-full flex items-center justify-center">
          3
        </span>
      </button>
    </>
  );
}