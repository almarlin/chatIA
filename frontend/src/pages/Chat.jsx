import { useState } from "react";

function Chat() {
  const [message, setMessage] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const username = localStorage.getItem("user");

  const sendMessage = () => {
    const userMessage = { from: "user", text: message };
    const botMessage = { from: "bot", text: "" };

    setChatLog((prev) => {
      const newLog = [...prev, userMessage, botMessage];
      startStreamingResponse(newLog.length - 1); // índice del mensaje del bot
      return newLog;
    });

    setMessage("");
  };
  const startStreamingResponse = (botIndex) => {
  const url = `http://localhost:8000/chat/stream?user_id=${encodeURIComponent(username)}&message=${encodeURIComponent(message)}`;
  const eventSource = new EventSource(url);

  eventSource.onmessage = (event) => {
    const chunk = event.data;
    setChatLog((prev) => {
      const updated = [...prev];
      // Asegúrate de que el índice aún sea válido
      if (updated[botIndex]) {
        updated[botIndex] = {
          ...updated[botIndex],
          text: updated[botIndex].text + chunk,
        };
      }
      return updated;
    });
  };

  eventSource.onerror = (err) => {
    console.error("Error de streaming:", err);
    eventSource.close();
  };
};


  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-xl mb-4">Zeta</h1>
      <div className="border p-4 mb-4 h-64 overflow-y-scroll bg-gray-100 rounded">
        {chatLog.map((msg, i) => (
          <div key={i} className={`mb-2 ${msg.from === "user" ? "text-right" : "text-left"}`}>
            <span className="inline-block bg-white p-2 rounded shadow whitespace-pre-line">{msg.text}</span>
          </div>
        ))}
      </div>
      <div className="flex">
        <input
          className="border flex-1 p-2 mr-2"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Escribe tu mensaje..."
        />
        <button onClick={sendMessage} className="bg-blue-600 text-white px-4 py-2 rounded">Enviar</button>
      </div>
    </div>
  );
}

export default Chat;
