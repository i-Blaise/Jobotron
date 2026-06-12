import { useState, useEffect } from 'react'
import Sidebar from './components/Sidebar.jsx'
import Dashboard from './pages/Dashboard.jsx'
import Jobs from './pages/Jobs.jsx'
import Controls from './pages/Controls.jsx'
import Logs from './pages/Logs.jsx'
import Settings from './pages/Settings.jsx'
import Login from './pages/Login.jsx'
import { getKey, clearKey } from './lib/api.js'

const pages = { dashboard: Dashboard, jobs: Jobs, controls: Controls, logs: Logs, settings: Settings }

export default function App() {
  const [page, setPage] = useState('dashboard')
  const [health, setHealth] = useState(null)
  const [authed, setAuthed] = useState(() => Boolean(getKey()))

  useEffect(() => {
    const onLogout = () => setAuthed(false)
    window.addEventListener('jobotron-logout', onLogout)
    return () => window.removeEventListener('jobotron-logout', onLogout)
  }, [])

  useEffect(() => {
    if (!authed) return
    fetchHealth()
    const interval = setInterval(fetchHealth, 30000)
    return () => clearInterval(interval)
  }, [authed])

  async function fetchHealth() {
    try {
      const res = await fetch('/health')
      setHealth(await res.json())
    } catch {
      setHealth(null)
    }
  }

  function handleLogout() {
    clearKey()
    setAuthed(false)
  }

  if (!authed) {
    return <Login onLogin={() => setAuthed(true)} />
  }

  const Page = pages[page]

  return (
    <div className="flex h-screen bg-slate-50 overflow-hidden">
      <Sidebar page={page} setPage={setPage} health={health} onLogout={handleLogout} />
      <main className="flex-1 overflow-auto">
        <Page />
      </main>
    </div>
  )
}
