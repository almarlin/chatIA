import logo from '../images/logo.svg';
import Navbar from "../components/navbar";
import Footer from "../components/footer";

function Home() {
    return (
        <div className="flex flex-col min-h-screen">
            <Navbar />

            <main className="flex-grow">
                <div className="mt-1 bg-green-700 p-10 sm:p-16 lg:p-24 flex items-center gap-6">
                    {/* Título */}
                    <h1 className="text-6xl text-white font-bold">Zeta AI</h1>

                    {/* Logo SVG */}
                    <div className="w-16 h-16">
                        <img src={logo} className="w-full h-full" />
                    </div>
                </div>

                <div className="max-w-4xl mx-auto p-4 sm:p-6 lg:p-8 space-y-8">
                    <div className="flex items-start gap-6">
                        <div className="w-1/2">
                            <p className="text-2xl font-semibold text-gray-800">¿Quién es Zeta AI?</p>
                        </div>
                        <div className="w-1/2">
                            <p className="text-lg text-gray-600">
                                Zeta es un asistente inteligente diseñado capaz de mantener conversaciones sencillas. Puede responder preguntas,
                                contarte historias y mucho más.
                            </p>
                        </div>
                    </div>

                    <div className="flex items-start gap-6">
                        <div className="w-1/2">
                            <p className="text-2xl font-semibold text-gray-800">¿Cómo puedo empezar a usarlo?</p>
                        </div>
                        <div className="w-1/2">
                            <p className="text-lg text-gray-600">
                                Simplemente <a className="text-blue-600" href="/login">inicia sesión</a> o <a className="text-blue-600" href="/register">regístrate</a> y ¡comienza a chatear!
                            </p>
                        </div>
                    </div>
                </div>
            </main>

            <Footer />
        </div>
    );
}

export default Home;
