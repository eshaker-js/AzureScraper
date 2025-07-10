import React from "react"
import type { Architecture } from "../types/architecture"

export interface ArchitectureCardProps {
  architecture: Architecture
  baseUrl?: string  // e.g. "https://learn.microsoft.com"
}

export const ArchitectureCard: React.FC<ArchitectureCardProps> = ({
  architecture,
  baseUrl = "",
}) => {
  const {
    title,
    summary,
    thumbnail_url,
    fetched_at,
    useCases,
    display_products,
    url,
  } = architecture

  const date = new Date(fetched_at).toLocaleString()
  const thumbSrc = thumbnail_url.startsWith("http")
    ? thumbnail_url
    : `${baseUrl}${thumbnail_url}`
  const detailUrl = url.startsWith("http") ? url : `${baseUrl}${url}`

  return (
    <a
      href={detailUrl}
      target="_blank"
      rel="noopener noreferrer"
      className="block bg-white border border-gray-200 rounded-lg shadow-lg hover:shadow-xl transition-shadow overflow-hidden flex flex-col no-underline"
    >
      {/* Thumbnail */}
      <div className="h-48 w-full overflow-hidden">
        <img
          src={thumbSrc}
          alt={`Thumbnail for ${title}`}
          className="object-cover w-full h-full"
        />
      </div>

      <div className="p-6 flex-1 flex flex-col">
        {/* Title & Summary */}
        <h3 className="text-2xl font-bold mb-2 text-gray-900">{title}</h3>
        <p className="text-gray-700 mb-4 flex-1">{summary}</p>

        {/* Products as tags */}
        <div className="flex flex-wrap gap-2 mb-4">
          {display_products.map((prod) => (
            <span
              key={prod}
              className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-1 rounded-full"
            >
              {prod}
            </span>
          ))}
        </div>

        {/* Use Cases */}
        <div className="mb-4">
          <h4 className="text-lg font-semibold mb-2 text-gray-800">Use Cases</h4>
          <ul className="list-disc list-inside text-gray-600 space-y-1">
            {useCases.map((uc, i) => (
              <li key={i}>{uc}</li>
            ))}
          </ul>
        </div>

        {/* Fetched at */}
        <div className="text-xs text-gray-500 mt-auto">
          Fetched: <time dateTime={fetched_at}>{date}</time>
        </div>
      </div>
    </a>
  )
}