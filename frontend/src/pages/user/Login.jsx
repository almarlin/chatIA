import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Footer from "../../components/footer";
import Navbar from "../../components/navbar";
import logo from '../../images/logo.svg';
import { useAuth } from "../../context/AuthContext";


function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { login: setAuthenticated } = useAuth(); // renombramos para evitar conflicto con tu función

  const login = async () => {
    const res = await fetch("http://localhost:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    if (res.ok) {
      localStorage.setItem("user", username);
      setAuthenticated(); // <- Esto activa isAuthenticated = true
      navigate("/chat");
    } else {
      alert("Inicio de sesión fallido");
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-gray-100">
      <Navbar />

      <div className="flex-grow flex items-center justify-center">
        <div className="bg-white p-8 rounded-2xl shadow-md w-full max-w-md">
          <div className="flex justify-center mb-4">
            <img src={logo} className="w-20 h-20" alt="Logo Zeta" />
          </div>
          <h1 className="text-3xl font-semibold text-center text-green-700 mb-6">Iniciar sesión</h1>

          <div className="flex flex-col space-y-4">
            <input
              className="border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Usuario"
              onChange={(e) => setUsername(e.target.value)}
            />
            <input
              type="password"
              className="border border-gray-300 p-3 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500"
              placeholder="Contraseña"
              onChange={(e) => setPassword(e.target.value)}
            />
            <button
              onClick={login}
              className="bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-lg transition duration-200"
            >
              Entrar
            </button>
            <p className="text-sm text-center text-gray-500 mt-2">
              ¿No tienes cuenta?{" "}
              <a
                href="/login"
                className="text-blue-500 hover:text-blue-700 font-medium transition-colors duration-200"
              >
                Regístrate
              </a>
            </p>
          </div>
        </div>
      </div>

      <Footer />
    </div>

  );
}

export default Login;
