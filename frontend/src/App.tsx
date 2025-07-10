// src/App.jsx
import { useState } from "react"
import LandingPage from "./components/LandingPage"
import Dashboard from "./components/Dashboard"
import Layout from "./components/Layout"

export default function App() {
  const [started, setStarted] = useState(false)

  return (
    <div className='min-h-screen'>
      <Layout>
        {!started ? (
          <LandingPage onStart={() => setStarted(true)} />
        ) : (
          <Dashboard onBack={() => setStarted(false)}/>
        )}
      </Layout>
    </div>
  )
}
