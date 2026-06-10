import { useEffect, useState, useRef } from 'react'
import { RefreshCw, Download, ChevronDown } from 'lucide-react'

export default function Logs() {
  const [logs, setLogs] = useState([])
  const [total, setTotal] = useState(0)
  const [lines, setLines] = useState(100)
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => { loadLogs() }, [lines])

  async function loadLogs() {
    setLoading(true)
    try {
      const data = await fetch(`/logs?lines=${lines}`).then(r => r.json())
      setLogs(data.logs || [])
      setTotal(data.total_lines || 0)
      setTimeout(() => bottomRef.current?.scrollIntoView({ behavior: 'smooth' }), 80)
    } finally {
      setLoading(false)
    }
  }

  function downloadLogs() {
    const blob = new Blob([logs.join('')], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `jobotron-${new Date().toISOString().split('T')[0]}.log`
    a.click()
    URL.revokeObjectURL(url)
  }

  const startLine = total - logs.length + 1

  return (
    <div className="p-8 flex flex-col" style={{ height: '100%' }}>
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="text-2xl font-bold text-slate-800">Logs</h2>
          <p className="text-slate-500 text-sm mt-1">{total} total entries</p>
        </div>
        <div className="flex items-center gap-2">
          <div className="relative">
            <select
              value={lines}
              onChange={e => setLines(Number(e.target.value))}
              className="appearance-none text-sm border border-slate-200 rounded-lg px-3 py-2 pr-8 text-slate-600 bg-white cursor-pointer"
            >
              <option value={50}>Last 50</option>
              <option value={100}>Last 100</option>
              <option value={250}>Last 250</option>
              <option value={500}>Last 500</option>
            </select>
            <ChevronDown size={14} className="absolute right-2.5 top-2.5 text-slate-400 pointer-events-none" />
          </div>
          <button
            onClick={loadLogs}
            className="flex items-center gap-2 px-4 py-2 text-sm border border-slate-200 rounded-lg hover:bg-slate-50 text-slate-600 transition-colors"
          >
            <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
            Refresh
          </button>
          <button
            onClick={downloadLogs}
            disabled={logs.length === 0}
            className="flex items-center gap-2 px-4 py-2 text-sm border border-slate-200 rounded-lg hover:bg-slate-50 text-slate-600 transition-colors disabled:opacity-40"
          >
            <Download size={14} />
            Download
          </button>
        </div>
      </div>

      <div className="flex-1 bg-slate-950 rounded-xl overflow-auto min-h-0">
        <div className="p-4 font-mono text-xs">
          {loading && logs.length === 0 ? (
            <p className="text-slate-500 flex items-center gap-2">
              <RefreshCw size={12} className="animate-spin" /> Loading logs…
            </p>
          ) : logs.length === 0 ? (
            <p className="text-slate-500">No log entries found.</p>
          ) : (
            logs.map((line, i) => {
              const isError = line.toLowerCase().includes('error') || line.toLowerCase().includes('fail')
              return (
                <div
                  key={i}
                  className={`flex gap-3 hover:bg-slate-900 px-2 py-0.5 rounded leading-5 ${
                    isError ? 'text-red-400' : 'text-slate-300'
                  }`}
                >
                  <span className="text-slate-600 select-none w-8 text-right shrink-0">
                    {startLine + i}
                  </span>
                  <span className="whitespace-pre-wrap break-all">{line.trim()}</span>
                </div>
              )
            })
          )}
          <div ref={bottomRef} />
        </div>
      </div>
    </div>
  )
}
