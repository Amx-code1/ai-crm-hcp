import React, { useState } from "react";
import { motion } from "framer-motion";
import { sendMessage } from "../api";


export default function ChatBox() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const handleSend = async (custom) => {
    const text = custom || input;
    if (!text) return;

    setMessages((prev) => [...prev, { text, type: "user" }]);

    const res = await sendMessage(text);

    setMessages((prev) => [
      ...prev,
      { text: formatResponse(res), type: "bot" },
    ]);

    setInput("");
  };

  window.send = (msg) => handleSend(msg);

const formatResponse = (res) => {
  if (Array.isArray(res)) {
    return res.map((item, i) => `${i + 1}. ${item}`).join("\n\n");
  }

  if (typeof res === "object") {
    return JSON.stringify(res, null, 2);
  }

  return res;
};

  return (
    <div className="main">
      <div className="header">AI CRM Assistant</div>

      <div className="chat">
        {messages.map((msg, i) => (
          <motion.div
            key={i}
            className={`message ${msg.type}`}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
          >
            {msg.text}
          </motion.div>
        ))}
      </div>

      <div className="input-area">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Talk to AI..."
        />
        <button onClick={() => handleSend()}>Send</button>
      </div>
    </div>
  );
}