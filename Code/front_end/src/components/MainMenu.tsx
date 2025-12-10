// Main menu page for the top navigation BarProp

import React from 'react';

interface MainMenuProps {
    onToggleSidebar?: () => void;
}

const MainMenu: React.FC<MainMenuProps> = ({ onToggleSidebar }) => {
    return (
        <header className="w-full h-16 bg-header flex items-center justify-between px-6 shadow-md">
      {/* Left section */}
      <div className="flex items-center gap-4">
        <button
          onClick={onToggleSidebar}
          className="p-2 rounded-xl bg-white hover:bg-brand-100 transition"
        >
          <span className="text-brand-700 font-bold text-xl">≡</span>
        </button>

        <h1 className="text-brand-900 font-bold text-xl tracking-wide">
          optimusGPT
        </h1>
      </div>

      {/* Right section */}
      <nav className="flex items-center gap-6 text-brand-900 font-medium">
        <a href="#" className="hover:text-brand-600">Products</a>
        <a href="#" className="hover:text-brand-600">Solutions</a>
        <a href="#" className="hover:text-brand-600">Resources</a>
        <a href="#" className="hover:text-brand-600">Community</a>

        <button className="px-4 py-2 rounded-xl bg-white border border-brand-700 hover:bg-brand-50">
          Sign in
        </button>

        <button className="px-4 py-2 rounded-xl bg-brand-700 text-white hover:bg-brand-800">
          Register
        </button>
      </nav>
    </header>
  );
};

export default MainMenu;