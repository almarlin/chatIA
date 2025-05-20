import { useState } from "react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";

export default function Footer() {
    return (
        <footer className="bg-gray-100 text-gray-600 mt-10">
            <div className="max-w-6xl mx-auto px-4 py-8">
                <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
                    <div className="text-center md:text-left">
                        <h2 className="text-lg font-semibold text-green-700">Zeta AI</h2>
                        <p className="text-sm">Programación de Inteligencia Artificial.</p>
                        <p className="text-sm">Curso de especialización en IA y Big Data Ilerna 24/25.</p>
                        <p className="text-sm">Álvaro Martínez Lineros</p>
                    </div>

                    <div className="flex space-x-6">
                        <a href="/" className="hover:text-green-700">Inicio</a>
                        <a href="/chat" className="hover:text-green-700">Chat</a>
                        <a href="/login" className="hover:text-green-700">Log In</a>
                        <a href="/register" className="hover:text-green-700">Sign Up</a>
                    </div>
                </div>

                <div className="text-center text-xs text-gray-400 mt-6 ">
                    Zeta AI puede cometer errores. Comprueba la información importante.
                </div>
                <div className="text-center text-xs text-gray-400 mt-6 ">
                    &copy; {new Date().getFullYear()} Zeta AI.
                </div>
            </div>
        </footer>
    );
}
