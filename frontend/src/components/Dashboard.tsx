// src/components/Dashboard.tsx
import { useState } from "react"
import type { Architecture } from "../types/architecture"
import { ArchitectureCard } from "./ArchitectureCard"

const API = "http://localhost:8000"
const THUMB_BASE = "https://learn.microsoft.com"

// This is where the action in the frontend happens
// The dashboard is responsible for communicating with the backend and loading the data

export default function Dashboard({ onBack }: { onBack: () => void }) {
  const [items, setItems] = useState<Architecture[]>([]) // Architecture objects
  const [skip, setSkip] = useState<number>(0) // Skip variable so we get a fresh batch on every scrape (hopefully)
  const [message, setMessage] = useState<string>("") // Message if the user tries to load without scraping new data
  const top = 5 //5 feels like a solid number for scrape amount
  const [loading, setLoading] = useState<boolean>(false) // Loading for when we scrape

  const loadInfo = async () => {
    // Function that calls GET, loads existing rows from db
    if (!loading) {
      setLoading(true)
    }
    const res = await fetch(`${API}/architectures`)
    const data = (await res.json()) as {
      status: string
      count: number
      results: Architecture[]
    }
    if (
      (items.length > 0 && data.results.length === items.length) ||
      data.results.length === 0
    ) {
      setMessage("No new info, scrape more before loading again") // if the database didnt return more items than we have, safe to say nothing new
      setLoading(false)
      return
    }
    setItems(data.results)
    setMessage("")
    setLoading(false)
  }

  const scrapeMore = async () => {
    setLoading(true) // gets turned off in loadInfo
    await fetch(`${API}/architectures?skip=${skip}&top=${top}`, {
      method: "POST",
    }) // post request to scrape more
    setSkip((s) => s + top)
    await loadInfo() // obviously if we scraped more we want to see it, instantly calls the load function
  }

  return (
    <div className='relative bg-gray-50 p-8 min-h-screen'>

      {/* Back to home screen */}

      <button
        onClick={onBack}
        className='absolute top-4 left-4 text-blue-600 hover:text-blue-800 font-medium'
      >
        ← Back
      </button>

      <h2 className='text-4xl font-bold text-center mb-8'>
        Architecture Dashboard
      </h2>

      {/* Scrape or Load from DB or show Loading */}

      <div className='flex justify-center space-x-4 mb-8'>
        <button
          onClick={loadInfo}
          disabled={loading}
          className={`px-6 py-3 rounded-lg text-white transition ${
            loading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-green-500 hover:bg-green-600"
          }`}
        >
          {loading ? "Loading..." : "Load Info"}
        </button>
        <button
          onClick={scrapeMore}
          disabled={loading}
          className={`px-6 py-3 rounded-lg text-white transition ${
            loading
              ? "bg-gray-400 cursor-not-allowed"
              : "bg-blue-500 hover:bg-blue-600"
          }`}
        >
          {loading ? "Loading..." : "Scrape More"}
        </button>
      </div>

      {/* warning message */}

      {message && (
        <div className='text-center mb-6'>
          <span className='text-red-600 font-medium'>{message}</span>
        </div>
      )}

      {/* component for each architecture object */}
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8'>
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
