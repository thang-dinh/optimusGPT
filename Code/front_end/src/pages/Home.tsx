// src/pages/Home.tsx
import React, { useState } from "react";
import { api } from "../api/client";

export function Home() {
  const [prompt, setPrompt] = useState("");
  const [response, setResponse] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await api.post("/solve", { prompt });
      // Adjust depending on your backend response shape
      setResponse(res.data.answer ?? JSON.stringify(res.data));
    } catch (err: any) {
      console.error(err);
      setError("Something went wrong talking to the backend.");
    } finally {
      setLoading(false);
    }
  };

   return (
    <div className="space-y-6">
      {/* Page Title */}
      <div className="space-y-1">
        <h2 className="text-2xl font-semibold text-brand-900">
          Chat with Optimus GPT agents
        </h2>
        <p className="text-sm text-brand-900/80">
          Send a prompt to the FastAPI backend and see the response below.
        </p>
      </div>

      {/* Card */}
      <div className="bg-brand-100/90 border border-brand-700/40 rounded-2xl shadow-md p-5 sm:p-6 space-y-5">
        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block space-y-1">
            <span className="text-sm font-medium text-brand-900">
              Prompt
            </span>
            <textarea
              className="w-full rounded-xl border border-brand-700/40 bg-brand-50/80 text-brand-900 text-sm p-3 outline-none shadow-inner focus:border-brand-600 focus:ring-2 focus:ring-brand-400/70 resize-vertical min-h-[100px]"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Ask a question, describe a problem, or say hi…"
            />
          </label>

          <div className="flex items-center gap-3">
            <button
              type="submit"
              className="inline-flex items-center justify-center px-4 py-2.5 rounded-full bg-brand-600 text-white text-sm font-semibold shadow hover:bg-brand-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              disabled={loading || !prompt.trim()}
            >
              {loading ? "Thinking…" : "Send"}
            </button>

            <button
              type="button"
              className="text-xs text-brand-900/70 hover:text-brand-900 underline-offset-2 hover:underline"
              onClick={() => {
                setPrompt("");
                setResponse(null);
                setError(null);
              }}
            >
              Clear
            </button>
          </div>
        </form>

        {/* Error */}
        {error && (
          <div className="mt-2 rounded-xl border border-red-400 bg-red-100/80 px-3 py-2 text-xs text-red-800">
            {error}
          </div>
        )}

        {/* Response */}
        {response && (
          <div className="mt-3 rounded-2xl bg-brand-200/90 border border-brand-700/30 px-4 py-3 shadow-inner">
            <h3 className="text-sm font-semibold text-brand-900 mb-1.5">
              Response
            </h3>
            <p className="text-sm whitespace-pre-wrap text-brand-900/90">
              {response}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}