import { useState } from 'react'
import { Bot, Lock, Loader } from 'lucide-react'
import { setKey } from '../lib/api.js'

export default function Login({ onLogin }) {
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!password || loading) return
    setLoading(true)
    setError(null)
    try {
      const res = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password }),
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        throw new Error(data.detail || `HTTP ${res.status}`)
      }
      setKey(password)
      onLogin()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="h-screen flex items-center justify-center bg-slate-900">
      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-2xl p-8 w-full max-w-sm shadow-xl"
      >
        <div className="flex items-center gap-3 mb-6">
          <div className="bg-blue-600 p-2.5 rounded-xl text-white">
            <Bot size={22} />
          </div>
          <div>
            <p className="font-bold text-lg text-slate-800 leading-tight">Jobotron</p>
            <p className="text-slate-400 text-xs">Admin Portal</p>
          </div>
        </div>

        <label className="block text-sm font-medium text-slate-600 mb-1.5">
          Admin password
        </label>
        <div className="relative mb-4">
          <Lock size={15} className="absolute left-3 top-3 text-slate-400" />
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            autoFocus
            className="w-full border border-slate-200 rounded-lg pl-9 pr-3 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="••••••••"
          />
        </div>

        {error && (
          <p className="text-red-600 text-xs mb-4 bg-red-50 border border-red-100 rounded-lg px-3 py-2">
            {error}
          </p>
        )}

        <button
          type="submit"
          disabled={loading || !password}
          className="w-full flex items-center justify-center gap-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white rounded-lg py-2.5 text-sm font-medium transition-colors"
        >
          {loading ? <><Loader size={14} className="animate-spin" /> Signing in…</> : 'Sign in'}
        </button>
      </form>
    </div>
  )
}
