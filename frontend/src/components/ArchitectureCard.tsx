// src/components/ArchitectureCard.tsx
import React, { useState } from "react"
import type { Architecture } from "../types/architecture"

export interface ArchitectureCardProps {
  architecture: Architecture
  baseUrl?: string // e.g. "https://learn.microsoft.com"
}


// I wanted a clickable card with every architecture, I use the thumbnail that comes with the object from the Microsoft API
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
  const [open, setOpen] = useState(false)

  const date = new Date(fetched_at).toLocaleString()
  const thumbSrc = thumbnail_url.startsWith("http")
    ? thumbnail_url
    : `${baseUrl}${thumbnail_url}`
  const detailUrl = url.startsWith("http") ? url : `${baseUrl}${url}`

  return (
    <a
      href={detailUrl}
      target='_blank'
      rel='noopener noreferrer'
      className='
        group
        bg-white
        border
        border-gray-100
        rounded-2xl
        shadow-sm
        hover:shadow-md
        transition
        duration-200
        overflow-hidden
        flex
        flex-col
        no-underline
      '
    >
      {/* Thumbnail */}
      <div className='w-full h-32 overflow-hidden flex-shrink-0'>
        <img
          src={thumbSrc}
          alt={`Thumbnail for ${title}`}
          className='w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300'
        />
      </div>

      <div className='p-5 flex-1 flex flex-col'>
        {/* Title */}
        <h3 className='text-xl font-semibold text-gray-900 mb-2 line-clamp-2'>
          {title}
        </h3>

        {/* Summary */}
        <p className='text-gray-600 text-sm mb-4 line-clamp-3'>{summary}</p>

        {/* Product tags: horizontal scroll if many */}
        <div className='mb-4 flex space-x-2 overflow-x-auto pb-1'>
          {display_products.map((prod) => (
            <span
              key={prod}
              className='
                flex-shrink-0
                bg-blue-50
                text-blue-700
                text-xs
                font-medium
                px-2
                py-1
                rounded-full
              '
            >
              {prod}
            </span>
          ))}
        </div>

        {/* Use Cases toggle */}
        {useCases.length > 0 && (
          <div className='mb-4'>
            <button
              onClick={(e) => {
                e.preventDefault()
                setOpen((o) => !o)
              }}
              className='text-sm text-blue-600 hover:underline mb-2'
            >
              {open ? "Hide Use Cases" : "Show Use Cases"}
            </button>

            {open && (
              <ul className='list-disc list-inside text-gray-600 space-y-1 text-sm'>
                {useCases.map((uc, i) => (
                  <li key={i}>{uc}</li>
                ))}
              </ul>
            )}
          </div>
        )}

        {/* Fetched at */}
        <div className='mt-auto text-xs text-gray-400'>
          Fetched:{" "}
          <time dateTime={fetched_at} className='italic'>
            {date}
          </time>
        </div>
      </div>
    </a>
  )
}
