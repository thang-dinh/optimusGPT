import React, { useEffect, useState } from "react";
import { SidebarResponse } from "../types/Sidebar";

interface SidebarProps {
  isOpen: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ isOpen }) => {
  const [menuData, setMenuData] = useState<SidebarResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/sidebar")
      .then((res) => {
        if (!res.ok) throw new Error("Failed to load sidebar menu");
        return res.json();
      })
      .then((data) => {
        setMenuData(data);
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
      <h2 className="text-2xl font-bold mb-6">Menu</h2>

      {loading && <p className="text-brand-200">Loading…</p>}
      {error && <p className="text-red-300">{error}</p>}

      {!loading && !error && menuData && (
        <nav className="flex flex-col gap-6">
          {menuData.sections.map((section, index) => (
            <div key={index}>
              {section.title && (
                <h3 className="text-lg font-semibold mb-2">{section.title}</h3>
              )}

              <div className="flex flex-col gap-2 ml-2">
                {section.items.map((item, i) => (
                  <a
                    key={i}
                    href={item.path}
                    className="hover:text-brand-200 transition"
                  >
                    {item.label}
                  </a>
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