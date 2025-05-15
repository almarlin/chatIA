import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const register = async () => {
    const res = await fetch("http://localhost:8000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (res.ok) navigate("/login");
    else alert("Registro fallido");
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-2xl mb-4">Registro</h1>
      <input className="border p-2 mb-2" placeholder="Usuario" onChange={(e) => setUsername(e.target.value)} />
      <input className="border p-2 mb-4" type="password" placeholder="Contraseña" onChange={(e) => setPassword(e.target.value)} />
      <button onClick={register} className="bg-blue-500 text-white px-4 py-2">Registrarse</button>
    </div>
  );
}

export default Register;
