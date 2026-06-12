import { useEffect, useState } from 'react'
import { Trash2, RefreshCw, AlertTriangle, ExternalLink } from 'lucide-react'
import { api } from '../lib/api.js'

export default function Jobs() {
  const [jobs, setJobs] = useState([])
  const [count, setCount] = useState(0)
  const [loading, setLoading] = useState(true)
  const [deleting, setDeleting] = useState(null)
  const [clearing, setClearing] = useState(false)
  const [maxPosts, setMaxPosts] = useState(3)

  useEffect(() => { loadJobs() }, [])

  async function loadJobs() {
    setLoading(true)
    try {
      const data = await api('/jobs')
      setJobs(data.jobs || [])
      setCount(data.count || 0)
      if (data.max_post_count != null) setMaxPosts(data.max_post_count + 1)
    } finally {
      setLoading(false)
    }
  }

  async function handleDelete(id) {
    setDeleting(id)
    try {
      await api(`/jobs/${id}`, { method: 'DELETE' })
      await loadJobs()
    } finally {
      setDeleting(null)
    }
  }

  async function handleClearAll() {
    if (!confirm('Remove all jobs from the queue? This cannot be undone.')) return
    setClearing(true)
    try {
      await api('/jobs', { method: 'DELETE' })
      await loadJobs()
    } finally {
      setClearing(false)
    }
  }

  const postBadge = (n) => {
    if (n === 0) return 'bg-blue-100 text-blue-700'
    if (n === 1) return 'bg-amber-100 text-amber-700'
    return 'bg-slate-100 text-slate-500'
  }

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Jobs Queue</h2>
          <p className="text-slate-500 text-sm mt-1">
            {count} job{count !== 1 ? 's' : ''} queued (max {maxPosts} posts each)
          </p>
        </div>
        <div className="flex gap-2">
          <button
            onClick={loadJobs}
            className="flex items-center gap-2 px-4 py-2 text-sm border border-slate-200 rounded-lg hover:bg-slate-50 text-slate-600 transition-colors"
          >
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            Refresh
          </button>
          {jobs.length > 0 && (
            <button
              onClick={handleClearAll}
              disabled={clearing}
              className="flex items-center gap-2 px-4 py-2 text-sm bg-red-50 text-red-600 border border-red-200 rounded-lg hover:bg-red-100 disabled:opacity-50 transition-colors"
            >
              <AlertTriangle size={14} />
              {clearing ? 'Clearing…' : 'Clear All'}
            </button>
          )}
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden">
        {loading ? (
          <div className="p-12 text-center text-slate-400">
            <RefreshCw size={20} className="animate-spin mx-auto mb-2" />
            Loading jobs…
          </div>
        ) : jobs.length === 0 ? (
          <div className="p-12 text-center">
            <p className="text-slate-400 font-medium">Queue is empty</p>
            <p className="text-slate-300 text-sm mt-1">Trigger a scrape from Controls to populate it</p>
          </div>
        ) : (
          <table className="w-full">
            <thead className="bg-slate-50 border-b border-slate-200">
              <tr>
                <th className="text-left px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">Job Title</th>
                <th className="text-left px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">Source</th>
                <th className="text-center px-6 py-3 text-xs font-semibold text-slate-500 uppercase tracking-wide">Posted</th>
                <th className="px-6 py-3" />
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {jobs.map(job => (
                <tr key={job._id} className="hover:bg-slate-50 group">
                  <td className="px-6 py-4">
                    <a
                      href={job.link}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-slate-800 font-medium text-sm hover:text-blue-600 flex items-center gap-1.5 group/link"
                    >
                      {job.name}
                      <ExternalLink size={12} className="opacity-0 group-hover/link:opacity-100 transition-opacity" />
                    </a>
                  </td>
                  <td className="px-6 py-4">
                    <span className="text-xs text-slate-500 bg-slate-100 px-2 py-1 rounded-md">
                      {job.link.includes('jobberman') ? 'Jobberman' : 'Jobwebghana'}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-center">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${postBadge(job.numberTimesPosted)}`}>
                      {job.numberTimesPosted} / {maxPosts}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button
                      onClick={() => handleDelete(job._id)}
                      disabled={deleting === job._id}
                      className="p-1.5 text-slate-300 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors disabled:opacity-40"
                      title="Remove job"
                    >
                      <Trash2 size={15} />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
