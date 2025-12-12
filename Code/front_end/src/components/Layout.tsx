// layout for all pages to reuse structure and styles

import React, { useState } from "react";
import MainMenu from "./MainMenu";
import Sidebar from "./Sidebar";

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen bg-brand-300 text-brand-900">
      {/* Top nav */}
      <MainMenu onToggleSidebar={() => setIsSidebarOpen((prev) => !prev)} />

      {/* Sidebar */}
      <Sidebar isOpen={isSidebarOpen} />

      {/* Main content */}
      <main
        className={`transition-all duration-300 pt-20 px-6 pb-8 ${
          isSidebarOpen ? "ml-64" : "ml-0"
        }`}
      >
        {children}
      </main>
    </div>
  );
};

export default Layout;