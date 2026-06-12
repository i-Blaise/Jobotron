import { useEffect, useState } from 'react'
import { Clock, Tag, Globe, SlidersHorizontal, RefreshCw, Save, CheckCircle, XCircle, X, Plus } from 'lucide-react'
import { api } from '../lib/api.js'

const SOURCE_LABELS = { jobwebghana: 'Jobwebghana', jobberman: 'Jobberman' }

export default function Settings() {
  const [config, setConfig] = useState(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [saveState, setSaveState] = useState(null) // { ok, message }
  const [keywordInput, setKeywordInput] = useState('')

  useEffect(() => { loadConfig() }, [])

  async function loadConfig() {
    setLoading(true)
    try {
      setConfig(await api('/config'))
    } catch (err) {
      setSaveState({ ok: false, message: `Failed to load config: ${err.message}` })
    } finally {
      setLoading(false)
    }
  }

  async function handleSave() {
    setSaving(true)
    setSaveState(null)
    try {
      const updated = await api('/config', {
        method: 'PUT',
        body: JSON.stringify({
          schedule_hours: config.schedule_hours,
          keywords: config.keywords,
          sources: config.sources,
          max_post_count: config.max_post_count,
          min_queue_size: config.min_queue_size,
        }),
      })
      setConfig(updated)
      setSaveState({ ok: true, message: 'Settings saved and applied — no restart needed.' })
    } catch (err) {
      setSaveState({ ok: false, message: err.message })
    } finally {
      setSaving(false)
    }
  }

  function toggleHour(hour) {
    const hours = config.schedule_hours.includes(hour)
      ? config.schedule_hours.filter(h => h !== hour)
      : [...config.schedule_hours, hour].sort((a, b) => a - b)
    setConfig({ ...config, schedule_hours: hours })
  }

  function addKeyword() {
    const k = keywordInput.trim()
    if (!k || config.keywords.some(x => x.toLowerCase() === k.toLowerCase())) {
      setKeywordInput('')
      return
    }
    setConfig({ ...config, keywords: [...config.keywords, k] })
    setKeywordInput('')
  }

  function removeKeyword(keyword) {
    setConfig({ ...config, keywords: config.keywords.filter(k => k !== keyword) })
  }

  if (loading) {
    return (
      <div className="p-8 flex items-center gap-3 text-slate-400">
        <RefreshCw size={16} className="animate-spin" /> Loading settings…
      </div>
    )
  }

  if (!config) {
    return (
      <div className="p-8">
        <p className="text-red-600 text-sm">{saveState?.message || 'Could not load settings.'}</p>
        <button onClick={loadConfig} className="mt-3 text-sm text-blue-600 hover:underline">Retry</button>
      </div>
    )
  }

  const noHours = config.schedule_hours.length === 0

  return (
    <div className="p-8 max-w-3xl">
      <h2 className="text-2xl font-bold text-slate-800 mb-1">Settings</h2>
      <p className="text-slate-500 text-sm mb-8">
        Stored in the database and applied live — changes survive restarts and deploys
      </p>

      <div className="space-y-6">
        <Section icon={Clock} title="Posting schedule" subtitle="Hours of the day (Africa/Accra) when the bot scrapes and posts">
          <div className="grid grid-cols-12 gap-1.5">
            {Array.from({ length: 24 }, (_, h) => (
              <button
                key={h}
                onClick={() => toggleHour(h)}
                className={`py-1.5 rounded-md text-xs font-mono font-medium transition-colors ${
                  config.schedule_hours.includes(h)
                    ? 'bg-blue-600 text-white'
                    : 'bg-slate-100 text-slate-500 hover:bg-slate-200'
                }`}
              >
                {String(h).padStart(2, '0')}
              </button>
            ))}
          </div>
          {noHours && <p className="text-amber-600 text-xs mt-2">Select at least one hour.</p>}
        </Section>

        <Section icon={Tag} title="Job search keywords" subtitle="Only Jobweb listings whose title matches a keyword are picked up; keywords also form the Jobberman search query. Leave empty to accept everything.">
          <div className="flex flex-wrap gap-2 mb-3">
            {config.keywords.length === 0 && (
              <span className="text-slate-400 text-sm italic">No keywords — all jobs accepted</span>
            )}
            {config.keywords.map(k => (
              <span key={k} className="inline-flex items-center gap-1.5 bg-blue-50 text-blue-700 text-sm px-3 py-1 rounded-full">
                {k}
                <button onClick={() => removeKeyword(k)} className="hover:text-blue-900">
                  <X size={13} />
                </button>
              </span>
            ))}
          </div>
          <div className="flex gap-2">
            <input
              value={keywordInput}
              onChange={e => setKeywordInput(e.target.value)}
              onKeyDown={e => { if (e.key === 'Enter') { e.preventDefault(); addKeyword() } }}
              placeholder="e.g. developer, accountant, remote…"
              className="flex-1 border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            <button
              onClick={addKeyword}
              className="flex items-center gap-1.5 px-4 py-2 text-sm bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg transition-colors"
            >
              <Plus size={14} /> Add
            </button>
          </div>
        </Section>

        <Section icon={Globe} title="Sources" subtitle="Disable a job board if it breaks or you want to pause it">
          <div className="space-y-3">
            {Object.entries(SOURCE_LABELS).map(([id, label]) => (
              <label key={id} className="flex items-center justify-between cursor-pointer">
                <span className="text-sm text-slate-700">{label}</span>
                <button
                  onClick={() => setConfig({
                    ...config,
                    sources: { ...config.sources, [id]: !config.sources[id] },
                  })}
                  className={`w-10 h-5.5 rounded-full relative transition-colors ${
                    config.sources[id] ? 'bg-blue-600' : 'bg-slate-300'
                  }`}
                  style={{ height: '22px' }}
                >
                  <span
                    className="absolute top-0.5 w-[18px] h-[18px] bg-white rounded-full shadow transition-all"
                    style={{ left: config.sources[id] ? '20px' : '2px' }}
                  />
                </button>
              </label>
            ))}
          </div>
        </Section>

        <Section icon={SlidersHorizontal} title="Posting behavior" subtitle="Queue and reposting tuning">
          <div className="grid grid-cols-2 gap-6">
            <NumberField
              label="Max reposts per job"
              hint="A job is dropped from the queue after being posted this many extra times"
              value={config.max_post_count}
              min={1} max={10}
              onChange={v => setConfig({ ...config, max_post_count: v })}
            />
            <NumberField
              label="Min queue size"
              hint="Scrapers run when fewer than this many jobs are queued"
              value={config.min_queue_size}
              min={0} max={50}
              onChange={v => setConfig({ ...config, min_queue_size: v })}
            />
          </div>
        </Section>
      </div>

      <div className="flex items-center gap-4 mt-8">
        <button
          onClick={handleSave}
          disabled={saving || noHours}
          className="flex items-center gap-2 px-6 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white rounded-lg text-sm font-medium transition-colors"
        >
          {saving ? <RefreshCw size={14} className="animate-spin" /> : <Save size={14} />}
          {saving ? 'Saving…' : 'Save settings'}
        </button>
        {saveState && (
          <span className={`flex items-center gap-1.5 text-sm ${saveState.ok ? 'text-green-600' : 'text-red-600'}`}>
            {saveState.ok ? <CheckCircle size={15} /> : <XCircle size={15} />}
            {saveState.message}
          </span>
        )}
      </div>
    </div>
  )
}

function Section({ icon: Icon, title, subtitle, children }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-6">
      <div className="flex items-center gap-2.5 mb-1">
        <Icon size={17} className="text-blue-600" />
        <h3 className="font-semibold text-slate-800">{title}</h3>
      </div>
      <p className="text-slate-400 text-xs mb-5">{subtitle}</p>
      {children}
    </div>
  )
}

function NumberField({ label, hint, value, min, max, onChange }) {
  return (
    <div>
      <label className="block text-sm font-medium text-slate-600 mb-1.5">{label}</label>
      <input
        type="number"
        value={value}
        min={min}
        max={max}
        onChange={e => onChange(Number(e.target.value))}
        className="w-24 border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      />
      <p className="text-slate-400 text-xs mt-1.5">{hint}</p>
    </div>
  )
}
