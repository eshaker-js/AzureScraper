// src/components/Dashboard.tsx
import { useState } from "react"
import type { Architecture } from "../types/architecture"

const API =  "http://localhost:8000"

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
    if ((items.length > 0 && data.results.length === items.length)|| data.results.length === 0) {
      setMessage("No new info, scrape more before loading again")
      return
    }
    setItems(data.results)
    setMessage("")
  }

  const scrapeMore = async () => {
    await fetch(`${API}/architectures?skip=${skip}&top=${top}`, {
      method: "POST",
    })
    setSkip((s) => s + top)
    await loadInfo()
  }

  return (
    <div className='relative bg-white p-8 min-h-screen'>
      {/* Back button */}
      <button
        onClick={onBack}
        className='absolute top-4 left-4 text-blue-600 hover:text-blue-800 font-medium'
      >
        ← Back
      </button>

      {/* Page title (optional: center or leave left) */}
      <h2 className='text-3xl font-bold text-center mb-8'>Dashboard</h2>

      {/* Centered action buttons */}
      <div className='flex justify-center space-x-4 mb-8'>
        <button
          onClick={loadInfo}
          className='px-4 py-2 bg-green-500 hover:bg-green-600 text-white rounded'
        >
          Load Info
        </button>
        <button
          onClick={scrapeMore}
          className='px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded'
        >
          Scrape More Architectures
        </button>
      </div>

      {message !== "" && (
        <div className='text-center mb-6'>
          <span className='text-red-600 font-medium'>{message}</span>
        </div>
      )}

      {/* Results grid */}
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6'>
        {items.map((item) => (
          <div key={item.id} className='border rounded-lg p-4 shadow'>
            <h3 className='font-semibold text-xl mb-2'>{item.title}</h3>
            <p className='text-gray-600 mb-2'>{item.summary}</p>
            <p className='text-sm text-gray-500'>
              Fetched at: {new Date(item.fetched_at).toLocaleString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  )
}
