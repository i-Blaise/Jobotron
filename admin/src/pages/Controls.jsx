import { useState } from 'react'
import { Search, Send, Loader, CheckCircle, XCircle } from 'lucide-react'

export default function Controls() {
  const [scrapeState, setScrapeState] = useState('idle')
  const [postState, setPostState] = useState('idle')
  const [scrapeResult, setScrapeResult] = useState(null)
  const [postResult, setPostResult] = useState(null)

  async function handleScrape() {
    setScrapeState('loading')
    setScrapeResult(null)
    try {
      const data = await fetch('/scrape', { method: 'POST' }).then(r => r.json())
      setScrapeResult(data)
      setScrapeState('success')
    } catch (err) {
      setScrapeResult({ error: err.message })
      setScrapeState('error')
    }
  }

  async function handlePost() {
    setPostState('loading')
    setPostResult(null)
    try {
      const data = await fetch('/post', { method: 'POST' }).then(r => r.json())
      setPostResult(data)
      setPostState('success')
    } catch (err) {
      setPostResult({ error: err.message })
      setPostState('error')
    }
  }

  return (
    <div className="p-8 max-w-3xl">
      <h2 className="text-2xl font-bold text-slate-800 mb-1">Controls</h2>
      <p className="text-slate-500 text-sm mb-8">Manually trigger bot actions outside the schedule</p>

      <div className="grid grid-cols-2 gap-6">
        <ActionCard
          icon={Search}
          iconColor="blue"
          title="Scrape Jobs"
          description="Fetch new listings from Jobwebghana and Jobberman, then save them to the queue."
          buttonLabel="Scrape Now"
          state={scrapeState}
          result={scrapeResult}
          onAction={handleScrape}
        />
        <ActionCard
          icon={Send}
          iconColor="green"
          title="Post Job"
          description="Pick the next queued job, summarise it with AI, and post it to Twitter/X. Takes ~30s."
          buttonLabel="Post Now"
          state={postState}
          result={postResult}
          onAction={handlePost}
        />
      </div>
    </div>
  )
}

const colorMap = {
  blue: {
    icon: 'bg-blue-50 text-blue-600',
    button: 'bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white',
  },
  green: {
    icon: 'bg-green-50 text-green-600',
    button: 'bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white',
  },
}

function ActionCard({ icon: Icon, iconColor, title, description, buttonLabel, state, result, onAction }) {
  const c = colorMap[iconColor]
  const isLoading = state === 'loading'

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6 flex flex-col">
      <div className={`inline-flex p-3 rounded-xl mb-4 w-fit ${c.icon}`}>
        <Icon size={22} />
      </div>
      <h3 className="font-semibold text-slate-800 text-base mb-2">{title}</h3>
      <p className="text-slate-500 text-sm mb-6 flex-1">{description}</p>

      <button
        onClick={onAction}
        disabled={isLoading}
        className={`flex items-center justify-center gap-2 px-5 py-2.5 rounded-lg text-sm font-medium transition-colors ${c.button}`}
      >
        {isLoading ? (
          <><Loader size={14} className="animate-spin" /> Running…</>
        ) : buttonLabel}
      </button>

      {result && (
        <div className={`mt-4 p-3 rounded-lg text-xs font-mono whitespace-pre-wrap break-all ${
          state === 'error' ? 'bg-red-50 text-red-700 border border-red-100' : 'bg-slate-50 text-slate-600 border border-slate-100'
        }`}>
          <div className="flex items-center gap-1.5 mb-1.5">
            {state === 'success'
              ? <CheckCircle size={13} className="text-green-500 shrink-0" />
              : <XCircle size={13} className="text-red-500 shrink-0" />}
            <span className="font-semibold">{state === 'success' ? 'Result' : 'Error'}</span>
          </div>
          {JSON.stringify(result, null, 2)}
        </div>
      )}
    </div>
  )
}
