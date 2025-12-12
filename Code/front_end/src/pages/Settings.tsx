// src/pages/Settings.tsx

import React from "react";

export function Settings() {
  return (
    <div className="space-y-6">
      {/* Page Title */}
      <div className="space-y-1">
        <h2 className="text-2xl font-semibold text-brand-900">
          Settings
        </h2>
        <p className="text-sm text-brand-900/80">
          Configure how Optimus GPT behaves in your workspace.
        </p>
      </div>

      {/* Card */}
      <div className="bg-brand-100/90 border border-brand-700/40 rounded-2xl shadow-md p-5 sm:p-6 space-y-5">
        {/* Example setting 1 */}
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-medium text-brand-900">
              Enable verbose responses
            </p>
            <p className="text-xs text-brand-900/75">
              When enabled, Optimus GPT will include more detail in answers.
            </p>
          </div>
          <label className="inline-flex items-center cursor-pointer">
            <input type="checkbox" className="sr-only peer" defaultChecked />
            <span className="w-10 h-5 bg-brand-200 rounded-full peer-checked:bg-brand-600 transition-colors relative">
              <span className="absolute top-0.5 left-0.5 w-4 h-4 bg-white rounded-full shadow peer-checked:translate-x-5 transition-transform" />
            </span>
          </label>
        </div>

        {/* Example setting 2 */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-brand-900">
            Default prompt prefix
          </label>
          <input
            type="text"
            className="w-full rounded-xl border border-brand-700/40 bg-brand-50/80 text-brand-900 text-sm px-3 py-2 outline-none shadow-inner focus:border-brand-600 focus:ring-2 focus:ring-brand-400/70"
            placeholder="e.g., 'You are a helpful assistant for my capstone project…'"
          />
          <p className="text-[11px] text-brand-900/75">
            This text will be automatically prepended to prompts (not wired up
            yet – this is just UI for now).
          </p>
        </div>

        {/* Example setting 3 */}
        <div className="space-y-2">
          <label className="text-sm font-medium text-brand-900">
            Theme intensity
          </label>
          <select className="w-full rounded-xl border border-brand-700/40 bg-brand-50/80 text-brand-900 text-sm px-3 py-2 outline-none focus:border-brand-600 focus:ring-2 focus:ring-brand-400/70">
            <option>Soft lavender (current)</option>
            <option>High contrast</option>
            <option>Minimal</option>
          </select>
        </div>
      </div>
    </div>
  );
}