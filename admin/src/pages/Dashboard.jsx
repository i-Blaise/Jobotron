import { useEffect, useState } from 'react'
import { Database, Clock, Briefcase, Calendar, RefreshCw } from 'lucide-react'
import { api } from '../lib/api.js'

export default function Dashboard() {
  const [health, setHealth] = useState(null)
  const [schedule, setSchedule] = useState(null)
  const [jobs, setJobs] = useState(null)
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState(null)

  useEffect(() => {
    loadAll()
    const interval = setInterval(loadAll, 30000)
    return () => clearInterval(interval)
  }, [])

  async function loadAll() {
    const [h, s, j] = await Promise.allSettled([
      api('/health'),
      api('/schedule'),
      api('/jobs'),
    ])
    if (h.status === 'fulfilled') setHealth(h.value)
    if (s.status === 'fulfilled') setSchedule(s.value)
    if (j.status === 'fulfilled') setJobs(j.value)
    setLastUpdated(new Date())
    setLoading(false)
  }

  if (loading) {
    return (
      <div className="p-8 flex items-center gap-3 text-slate-400">
        <RefreshCw size={16} className="animate-spin" />
        Loading dashboard…
      </div>
    )
  }

  const nextRunDate = health?.next_run ? new Date(health.next_run) : null

  return (
    <div className="p-8 max-w-4xl">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-slate-800">Dashboard</h2>
        {lastUpdated && (
          <span className="text-xs text-slate-400">
            Updated {lastUpdated.toLocaleTimeString()}
          </span>
        )}
      </div>

      <div className="grid grid-cols-2 gap-4 mb-8">
        <StatCard
          icon={Database}
          label="Database"
          value={health?.db_connected ? 'Connected' : 'Disconnected'}
          ok={health?.db_connected}
        />
        <StatCard
          icon={Clock}
          label="Scheduler"
          value={health?.scheduler_running ? 'Running' : 'Stopped'}
          ok={health?.scheduler_running}
        />
        <StatCard
          icon={Briefcase}
          label="Jobs in Queue"
          value={jobs?.count ?? '—'}
          ok
          neutral
        />
        <StatCard
          icon={Calendar}
          label="Next Post"
          value={nextRunDate ? nextRunDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '—'}
          ok
          neutral
        />
      </div>

      {schedule?.jobs?.length > 0 && (
        <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-100">
            <h3 className="font-semibold text-slate-700">Scheduler</h3>
          </div>
          <div className="divide-y divide-slate-100">
            {schedule.jobs.map(job => (
              <div key={job.id} className="px-6 py-4 flex items-center justify-between">
                <div>
                  <p className="font-medium text-slate-800 text-sm">{job.name}</p>
                  <p className="text-slate-400 text-xs font-mono mt-0.5">{job.trigger}</p>
                </div>
                <div className="text-right">
                  <p className="text-xs text-slate-400 mb-0.5">Next run</p>
                  <p className="text-sm font-semibold text-blue-600">
                    {new Date(job.next_run).toLocaleString([], {
                      month: 'short', day: 'numeric',
                      hour: '2-digit', minute: '2-digit',
                    })}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function StatCard({ icon: Icon, label, value, ok, neutral }) {
  const color = neutral
    ? 'text-blue-600 bg-blue-50'
    : ok
    ? 'text-green-600 bg-green-50'
    : 'text-red-500 bg-red-50'

  const textColor = neutral ? 'text-slate-800' : ok ? 'text-green-700' : 'text-red-600'

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 flex items-center gap-4">
      <div className={`p-3 rounded-lg shrink-0 ${color}`}>
        <Icon size={20} />
      </div>
      <div>
        <p className="text-slate-500 text-xs font-medium uppercase tracking-wide">{label}</p>
        <p className={`font-semibold text-base mt-0.5 ${textColor}`}>{String(value)}</p>
      </div>
    </div>
  )
}
