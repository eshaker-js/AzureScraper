interface Props {
  onStart: () => void
}

export default function LandingPage({ onStart }: Props) {
  return (
    <section className='flex-grow flex flex-col items-center justify-center text-center px-4'>
      <h2 className='text-5xl font-bold text-blue-800 mb-4'>
        Explore Azure Architectures
      </h2>
      <p className='text-lg text-gray-700 max-w-2xl mb-8'>
        Instantly fetch, browse, and save Azure reference architectures—all in
        one place.
      </p>
      <button
        onClick={onStart}
        className='bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg shadow-lg'
      >
        Get Started
      </button>
    </section>
  )
}
