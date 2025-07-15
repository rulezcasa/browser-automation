// src/App.jsx
import { useState, useEffect, useRef } from "react";

function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [thinking, setThinking] = useState(""); // NEW

  const websocket = useRef(null);

  useEffect(() => {
    // Add welcome message
    setMessages([
      { from: "system", text: "Welcome! How can I assist you today?" },
    ]);

    websocket.current = new WebSocket("ws://localhost:8000/chat");

websocket.current.onmessage = (event) => {
  const data = event.data;

  if (data.startsWith("thinking:")) {
    setThinking(data.replace("thinking:", "").trim());
  } else if (data.startsWith("clarification:")) {
    setMessages((prev) => [
      ...prev,
      { from: "bot", text: data.replace("clarification:", "").trim() },
    ]);
  } else if (data.startsWith("response:")) {
    setMessages((prev) => [
      ...prev,
      { from: "bot", text: data.replace("response:", "").trim() },
    ]);
    setThinking(""); // Clear thinking once response is sent
  } else if (data.startsWith("screenshot:")) {
    const base64 = data.replace("screenshot:", "").trim();
    setMessages((prev) => [
      ...prev,
      { from: "bot", image: base64 },
    ]);
  } else {
    // Fallback
    setMessages((prev) => [...prev, { from: "bot", text: data }]);
  }
};


    return () => websocket.current.close();
  }, []);

  const sendMessage = () => {
    if (input.trim()) {
      setMessages((prev) => [...prev, { from: "user", text: input }]);
      websocket.current.send(input);
      setInput("");
    }
  };

  return (
    <div style={styles.container}>
      <h2>Browser Automation Agent</h2>
      {thinking && (
  <div style={styles.thinking}>
    <em>🤔 {thinking}</em>
  </div>
)}

      <div style={styles.chatBox}>
{messages.map((msg, i) => (
  <div
    key={i}
    style={msg.from === "user" ? styles.userMsg : styles.botMsg}
  >
    <strong>{msg.from === "user" ? "You" : "Bot"}:</strong>{" "}
    {msg.text && <span>{msg.text}</span>}
    {msg.image && (
      <div>
        <img
          src={`data:image/png;base64,${msg.image}`}
          alt="Screenshot"
          style={styles.screenshot}
        />
      </div>
    )}
  </div>
))}

      </div>
      <div style={styles.inputBox}>
        <input
          style={styles.input}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type your message..."
        />
        <button style={styles.button} onClick={sendMessage}>
          Send
        </button>
        <button style={styles.button} onClick={() => window.location.reload()}>
          Clear chat
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 600,
    margin: "0 auto",
    padding: 20,
    fontFamily: "sans-serif",
  },
  chatBox: {
    height: 400,
    overflowY: "scroll",
    border: "1px solid #ccc",
    padding: 10,
    marginBottom: 10,
    backgroundColor: "#f9f9f9",
  },
  inputBox: { display: "flex" },
  input: { flex: 1, padding: 10, fontSize: 16 },
  button: { padding: "10px 20px", fontSize: 16 },
  userMsg: { textAlign: "right", margin: "5px 0" },
  botMsg: { textAlign: "left", margin: "5px 0", color: "#333" },

  screenshot: {
  maxWidth: "100%",
  marginTop: 10,
  borderRadius: 8,
  boxShadow: "0 0 5px rgba(0,0,0,0.2)",
},
};

export default ChatWindow;
