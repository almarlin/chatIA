import { useState } from "react";
import { Bars3Icon, XMarkIcon } from "@heroicons/react/24/outline";

export default function Navbar() {
    const [open, setOpen] = useState(false);

    return (
        <nav className="bg-white shadow-md px-6 py-4">
            <div className="flex justify-between items-center">
                <div className="text-2xl font-bold text-green-700">ZetaAI</div>

                <div className="hidden md:flex space-x-6">
                    <a href="/" className="text-gray-700 hover:text-green-700">Home</a>
                    <a href="/chat" className="text-gray-700 hover:text-green-700">Chat</a>
                    <a href="/login" className="text-gray-700 hover:text-green-700">Log In</a>
                    <a href="/register" className="text-gray-700 hover:text-green-700">Sign Up</a>
                </div>

                <div className="md:hidden">
                    <button onClick={() => setOpen(!open)} className="text-gray-700 focus:outline-none">
                        {open ? (
                            <XMarkIcon className="h-6 w-6" />
                        ) : (
                            <Bars3Icon className="h-6 w-6" />
                        )}
                    </button>
                </div>
            </div>

            {open && (
                <div className="md:hidden mt-4 space-y-2">
                    <a href="/" className="block text-gray-700 hover:text-green-700">Home</a>
                    <a href="/chat" className="block text-gray-700 hover:text-green-700">Chat</a>
                    <a href="/login" className="block text-gray-700 hover:text-green-700">Log In</a>
                    <a href="/register" className="block text-gray-700 hover:text-green-700">Sign In</a>
                </div>
            )}
        </nav>
    );
}
