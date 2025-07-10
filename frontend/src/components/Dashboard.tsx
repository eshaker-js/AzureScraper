// src/components/Dashboard.tsx
import { useState } from "react"
import type { Architecture } from "../types/architecture"
import { ArchitectureCard } from "./ArchitectureCard"

const API = "http://localhost:8000"
const THUMB_BASE = "https://learn.microsoft.com"  // adjust if needed

export default function Dashboard({ onBack }: { onBack: () => void }) {
  const [items, setItems] = useState<Architecture[]>([])
  const [skip, setSkip] = useState<number>(0)
  const [message, setMessage] = useState<string>("")
  const top = 5

  const loadInfo = async () => {
    const res = await fetch(`${API}/architectures`)
    const data = (await res.json()) as {
      status: string
      count: number
      results: Architecture[]
    }
    if ((items.length > 0 && data.results.length === items.length) || data.results.length === 0) {
      setMessage("No new info, scrape more before loading again")
      return
    }
    setItems(data.results)
    setMessage("")
  }

  const scrapeMore = async () => {
    await fetch(`${API}/architectures?skip=${skip}&top=${top}`, { method: "POST" })
    setSkip((s) => s + top)
    await loadInfo()
  }

  return (
    <div className="relative bg-gray-50 p-8 min-h-screen">
      <button
        onClick={onBack}
        className="absolute top-4 left-4 text-blue-600 hover:text-blue-800 font-medium"
      >
        ← Back
      </button>

      <h2 className="text-4xl font-bold text-center mb-8">Architecture Dashboard</h2>

      <div className="flex justify-center space-x-4 mb-8">
        <button
          onClick={loadInfo}
          className="px-6 py-3 bg-green-500 hover:bg-green-600 text-white rounded-lg"
        >
          Load Info
        </button>
        <button
          onClick={scrapeMore}
          className="px-6 py-3 bg-blue-500 hover:bg-blue-600 text-white rounded-lg"
        >
          Scrape More Architectures
        </button>
      </div>

      {message && (
        <div className="text-center mb-6">
          <span className="text-red-600 font-medium">{message}</span>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        {items.map((item) => (
          <ArchitectureCard
            key={item.url}
            architecture={item}
            baseUrl={THUMB_BASE}
          />
        ))}
      </div>
    </div>
  )
}
