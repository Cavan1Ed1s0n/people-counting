"use client";

import { useState } from "react";

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<{ people_count: number; processed_url: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setLoading(true);
    const form = new FormData();
    form.append("file", file);
    const res = await fetch(`${API_BASE}/upload`, { method: "POST", body: form });
    const data = await res.json();
    setResult({ people_count: data.people_count, processed_url: data.processed_url });
    setLoading(false);
  };

  return (
    <main style={{ maxWidth: 800, margin: "2rem auto", padding: "1rem" }}>
      <h1>People Detector</h1>
      <form onSubmit={onSubmit}>
        <input type="file" accept="image/*" onChange={(e) => setFile(e.target.files?.[0] ?? null)} />
        <button type="submit" disabled={!file || loading} style={{ marginLeft: 12 }}>
          {loading ? "Processing..." : "Upload & Detect"}
        </button>
      </form>

      {result && (
        <section style={{ marginTop: 24 }}>
          <h2>Result</h2>
          <p>People count: <b>{result.people_count}</b></p>
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={result.processed_url} alt="Processed" style={{ maxWidth: "100%", border: "1px solid #ddd" }} />
        </section>
      )}

      <section style={{ marginTop: 24 }}>
        <a href="/history">View History →</a>
      </section>
    </main>
  );
}
