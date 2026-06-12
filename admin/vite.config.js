import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/health': 'http://localhost:8000',
      '/jobs': 'http://localhost:8000',
      '/scrape': 'http://localhost:8000',
      '/post': 'http://localhost:8000',
      '/logs': 'http://localhost:8000',
      '/schedule': 'http://localhost:8000',
    },
  },
})
