//App.tsx

import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import { Home } from "./pages/Home";
import { Settings } from "./pages/Settings";


export default function App() {
    return (
        <Router>
            <div className="min-h-screen bg-brand-300 text-gray-900 flex flex-col">
                {/* Top Header */}
                <header className="w-full bg-header p-4 shadow-md flex justify-between items-center">
                    <h1 className="text-xl font-bold">Optimus GPT</h1>
                    <nav className="flex gap-4">
                        <Link className="hover:underline" to="/">Home</Link>
                        <Link className="hover:underline" to="/settings">Settings</Link>
                    </nav>
                </header>


                {/* Main Content */}
                <main className="flex-1 p-6">
                    <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/settings" element={<Settings />} />
                    </Routes>
                </main>


                {/* Footer */}
                <footer className="w-full p-4 text-center text-sm opacity-70">
                    © {new Date().getFullYear()} Optimus GPT
                </footer>
            </div>
        </Router>
    );
}