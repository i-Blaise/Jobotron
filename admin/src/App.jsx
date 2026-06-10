import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Jobs from './pages/Jobs.jsx'
import Controls from './pages/Controls.jsx'
import Logs from './pages/Logs.jsx'

const pages = { dashboard: Dashboard, jobs: Jobs, controls: Controls, logs: Logs }

export default function App() {
  const [page, setPage] = useState('dashboard')
  const [health, setHealth] = useState(null)

  useEffect(() => {
    fetchHealth()
    const interval = setInterval(fetchHealth, 30000)
    return () => clearInterval(interval)
  }, [])

  async function fetchHealth() {
    try {
      const res = await fetch('/health')
      setHealth(await res.json())
    } catch {
      setHealth(null)
    }
  }

  const Page = pages[page]

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      <Sidebar page={page} setPage={setPage} health={health} />
      <main className="flex-1 overflow-auto">
        <Page />
      </main>
    </div>
  )
}
