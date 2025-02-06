import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: "/static/dashboard/",
  build: {
    outDir: "../backend/dashboard/static/dashboard",
  },
  server: {
    open: '/dashboard/',
    proxy: {
      '/apis/shopping': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
