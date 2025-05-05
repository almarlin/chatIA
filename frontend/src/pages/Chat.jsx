import { useState } from "react";

function Chat() {
  const [message, setMessage] = useState("");
  const [chatLog, setChatLog] = useState([]);
  const username = localStorage.getItem("user");

  const sendMessage = async () => {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: username, message }),
    });
    const data = await res.json();
    setChatLog([...chatLog, { from: "user", text: message }, { from: "bot", text: data.respuesta }]);
    setMessage("");
  };

  return (
    <div className="p-4 max-w-xl mx-auto">
      <h1 className="text-xl mb-4">Chat con IA</h1>
      <div className="border p-4 mb-4 h-64 overflow-y-scroll bg-gray-100 rounded">
        {chatLog.map((msg, i) => (
          <div key={i} className={`mb-2 ${msg.from === "user" ? "text-right" : "text-left"}`}>
            <span className="inline-block bg-white p-2 rounded shadow">{msg.text}</span>
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
