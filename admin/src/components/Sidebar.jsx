import { LayoutDashboard, Briefcase, Zap, FileText, Bot } from 'lucide-react'

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'jobs', label: 'Jobs Queue', icon: Briefcase },
  { id: 'controls', label: 'Controls', icon: Zap },
  { id: 'logs', label: 'Logs', icon: FileText },
]

export default function Sidebar({ page, setPage, health }) {
  const isOk = health?.status === 'ok'
  const isDegraded = health?.status === 'degraded'

  const nextRun = health?.next_run
    ? new Date(health.next_run).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    : null

  return (
    <aside className="w-60 bg-slate-900 text-white flex flex-col shrink-0">
      {/* Brand */}
      <div className="p-5 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Bot size={18} />
          </div>
          <div>
            <p className="font-bold text-base leading-tight">Jobotron</p>
            <p className="text-slate-400 text-xs">Admin Panel</p>
          </div>
        </div>
      </div>

      {/* System status */}
      <div className="px-5 py-3 border-b border-slate-800">
        <div className={`inline-flex items-center gap-1.5 text-xs px-3 py-1.5 rounded-full ${
          health === null
            ? 'bg-slate-700 text-slate-400'
            : isOk
            ? 'bg-green-900/60 text-green-300'
            : isDegraded
            ? 'bg-amber-900/60 text-amber-300'
            : 'bg-red-900/60 text-red-300'
        }`}>
          <span className={`w-1.5 h-1.5 rounded-full ${
            health === null ? 'bg-slate-500' : isOk ? 'bg-green-400' : isDegraded ? 'bg-amber-400' : 'bg-red-400'
          }`} />
          {health === null ? 'Connecting…' : isOk ? 'All systems OK' : isDegraded ? 'DB disconnected' : 'Offline'}
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 p-3 space-y-0.5">
        {navItems.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setPage(id)}
            className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
              page === id
                ? 'bg-blue-600 text-white'
                : 'text-slate-400 hover:bg-slate-800 hover:text-white'
            }`}
          >
            <Icon size={17} />
            {label}
          </button>
        ))}
      </nav>

      {/* Next run footer */}
      <div className="p-5 border-t border-slate-800">
        <p className="text-slate-500 text-xs">Next scheduled post</p>
        <p className="text-slate-200 font-mono text-sm mt-0.5">
          {nextRun ?? '—'}
        </p>
      </div>
    </aside>
  )
}
