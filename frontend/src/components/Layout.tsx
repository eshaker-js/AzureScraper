import type { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

export default function Layout( {children}: LayoutProps) {
  return (
    <main className='min-h-screen bg-gradient-to-b from-blue-50 to-white flex flex-col'>
      <nav className='flex items-center justify-between px-8 py-4'>
        <h1 className='text-2xl font-extrabold text-blue-700'>
          Azure Arch Explorer
        </h1>
      </nav>
      <div className="flex-grow">
        {children}
      </div>
      <footer className='py-4 bg-gray-100 text-center text-sm text-gray-500' />
    </main>
  )
}
