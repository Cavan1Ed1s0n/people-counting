"use client";

import { useEffect, useState } from "react";

type Item = {
  id: number;
  created_at: string;
  original_filename: string;
  processed_url: string;
  people_count: number;
};
type Page = { total: number; page: number; page_size: number; items: Item[] };

export default function HistoryPage() {
  const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000/api";

  const [page, setPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);
  const [q, setQ] = useState("");
  const [minCount, setMinCount] = useState<string>("");
  const [maxCount, setMaxCount] = useState<string>("");
  const [data, setData] = useState<Page | null>(null);

  const fetchPage = async () => {
    const params = new URLSearchParams();
    params.set("page", String(page));
    params.set("page_size", String(pageSize));
    if (q) params.set("q", q);
    if (minCount) params.set("min_count", minCount);
    if (maxCount) params.set("max_count", maxCount);

    const res = await fetch(`${API_BASE}/history?${params.toString()}`);
    const json = await res.json();
    setData(json);
  };

  useEffect(() => { fetchPage(); /* eslint-disable-next-line */ }, [page, pageSize]);

  return (
    <main style={{ maxWidth: 1000, margin: "2rem auto", padding: "1rem" }}>
      <h1>History</h1>
      <div style={{ display: "flex", gap: 8, alignItems: "center", flexWrap: "wrap" }}>
        <input placeholder="Search filename..." value={q} onChange={(e) => setQ(e.target.value)} />
        <input placeholder="Min count" type="number" value={minCount} onChange={(e) => setMinCount(e.target.value)} />
        <input placeholder="Max count" type="number" value={maxCount} onChange={(e) => setMaxCount(e.target.value)} />
        <button onClick={() => { setPage(1); fetchPage(); }}>Apply</button>
        <div style={{ marginLeft: "auto" }}>
          Page size:{" "}
          <select value={pageSize} onChange={(e) => { setPageSize(Number(e.target.value)); setPage(1); }}>
            {[5,10,20,50].map(n => <option key={n} value={n}>{n}</option>)}
          </select>
        </div>
      </div>

      <table style={{ width: "100%", marginTop: 16, borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>When</th>
            <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Filename</th>
            <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>People</th>
            <th style={{ borderBottom: "1px solid #ddd", textAlign: "left" }}>Preview</th>
          </tr>
        </thead>
        <tbody>
          {data?.items?.map(item => (
            <tr key={item.id}>
              <td style={{ padding: 8 }}>{new Date(item.created_at).toLocaleString()}</td>
              <td style={{ padding: 8 }}>{item.original_filename}</td>
              <td style={{ padding: 8 }}>{item.people_count}</td>
              <td style={{ padding: 8 }}>
                {/* eslint-disable-next-line @next/next/no-img-element */}
                <img src={item.processed_url} alt="thumb" style={{ maxWidth: 180, border: "1px solid #eee" }} />
              </td>
            </tr>
          ))}
          {!data?.items?.length && <tr><td colSpan={4} style={{ padding: 12 }}>No records.</td></tr>}
        </tbody>
      </table>

      <div style={{ display: "flex", gap: 8, marginTop: 16, alignItems: "center" }}>
        <button disabled={page<=1} onClick={() => setPage(p => Math.max(1, p-1))}>Prev</button>
        <span>Page {page}</span>
        <button
        disabled={data ? page * pageSize >= data.total : false}
        onClick={() => setPage(p => p + 1)}
      >
        Next
      </button>
        <span style={{ marginLeft: "auto" }}>{data ? `Total: ${data.total}` : ""}</span>
      </div>

      <div style={{ marginTop: 24 }}>
        <a href="/">← Back to Upload</a>
      </div>
    </main>
  );
}
