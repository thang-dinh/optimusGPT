import React, { useEffect, useState } from "react";
import { NavLink } from "react-router-dom";
import { SidebarResponse } from "../types/Sidebar";
import { api } from "../api/client";

interface SidebarProps {
  isOpen: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen }) => {
  const [menuData, setMenuData] = useState<SidebarResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .get<SidebarResponse>("/sidebar")
      .then((res) => {
        setMenuData(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError("Unable to load menu.");
        setLoading(false);
      });
  }, []);

  return (
    <aside
      className={`h-screen bg-brand-500 text-white w-64 fixed top-16 left-0 shadow-xl p-6 transition-transform duration-300
                  ${isOpen ? "translate-x-0" : "-translate-x-64"}`}
    >
      <h2 className="text-2xl font-bold mb-6 tracking-wide">Menu</h2>

      {loading && <p className="text-brand-200">Loading…</p>}
      {error && <p className="text-red-300">{error}</p>}

      {!loading && !error && menuData && (
        <nav className="flex flex-col gap-6 overflow-y-auto pr-2">
          {menuData.sections.map((section, index) => (
            <div key={index}>
              {section.title && (
                <h3 className="text-xs uppercase tracking-wide text-brand-100/80 mb-2">{section.title}</h3>
              )}

              <div className="flex flex-col gap-1 ml-1">
                {section.items.map((item, i) => (
                  <NavLink
                    key={i}
                    to={item.path}
                    className={({ isActive }) =>
                      `block px-3 py-1.5 rounded-lg text-sm transition-colors ${
                        isActive
                          ? "bg-brand-400/90 text-white font-semibold shadow-sm"
                          : "text-brand-50 hover:bg-brand-400/50"
                      }`
                    }
                  >
                    {item.label}
                  </NavLink>
                ))}
              </div>
            </div>
          ))}
        </nav>
      )}
    </aside>
  );
};

export default Sidebar;