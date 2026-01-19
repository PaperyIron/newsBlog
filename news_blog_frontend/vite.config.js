//vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/server': {  // Using /server instead of /api
        target: 'http://localhost:5555',
        changeOrigin: true,
        secure: false,
        rewrite: (path) => path.replace(/^\/server/, '')  // Remove /server prefix
      }
    },
  },
})