const KEY_STORAGE = 'jobotron_admin_key'

export function getKey() {
  return localStorage.getItem(KEY_STORAGE) || ''
}

export function setKey(key) {
  localStorage.setItem(KEY_STORAGE, key)
}

export function clearKey() {
  localStorage.removeItem(KEY_STORAGE)
}

export async function api(path, options = {}) {
  const headers = { 'X-Admin-Key': getKey(), ...(options.headers || {}) }
  if (options.body && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json'
  }
  const res = await fetch(path, { ...options, headers })
  if (res.status === 401) {
    clearKey()
    window.dispatchEvent(new Event('jobotron-logout'))
    throw new Error('Unauthorized')
  }
  if (!res.ok) {
    let detail = `HTTP ${res.status}`
    try {
      const data = await res.json()
      if (data.detail) detail = data.detail
    } catch { /* keep default */ }
    throw new Error(detail)
  }
  return res.json()
}
