// Main menu page for the top navigation BarProp

import React from 'react';
import { NavLink } from 'react-router-dom';

interface MainMenuProps {
    onToggleSidebar?: () => void;
}

const MainMenu: React.FC<MainMenuProps> = ({ onToggleSidebar }) => {
    return (
      <header className="fixed top-0 left-0 right-0 z-20 w-full h-16 bg-header flex items-center justify-between px-6 shadow-md border-b border-brand-500/40">
      {/* Left section */}
        <div className="flex items-center gap-4">
          <button
            onClick={onToggleSidebar}
            className="p-2 rounded-xl bg-white hover:bg-brand-100 transition shadow-sm border border-brand-200"
          >
            <span className="text-brand-700 font-bold text-xl">≡</span>
          </button>

          <h1 className="text-brand-900 font-bold text-xl tracking-wide">
            optimusGPT
          </h1>
        </div>

      {/* Right section */}
      <nav className="flex items-center gap-6 text-sm font-medium">
        {/* App navigation */}
        <NavLink
          to="/"
          className={({ isActive }) =>
            `hover:text-brand-600 transition-colors ${
              isActive ? "text-brand-800 underline underline-offset-4" : "text-brand-900"
            }`
          }
        >
          Home
        </NavLink>

        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `hover:text-brand-600 transition-colors ${
              isActive ? "text-brand-800 underline underline-offset-4" : "text-brand-900"
            }`
          }
        >
          Settings
        </NavLink>

        {/* Placeholder marketing links */}
        <a href="#" className="hover:text-brand-600 text-brand-900 hidden md:inline">
          Products
        </a>
        <a href="#" className="hover:text-brand-600 text-brand-900 hidden md:inline">
          Solutions
        </a>
        <a href="#" className="hover:text-brand-600 text-brand-900 hidden md:inline">
          Resources
        </a>
        <a href="#" className="hover:text-brand-600 text-brand-900 hidden md:inline">
          Community
        </a>

        {/* Auth buttons */}
        <button className="px-4 py-2 rounded-xl bg-white border border-brand-700 hover:bg-brand-50 text-brand-900 text-sm">
          Sign in
        </button>

        <button className="px-4 py-2 rounded-xl bg-brand-700 text-white hover:bg-brand-800 text-sm shadow-md">
          Register
        </button>
      </nav>
    </header>
  );
};

export default MainMenu;