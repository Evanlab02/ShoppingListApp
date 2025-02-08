import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: "/static/dashboard/",
  build: {
    manifest: "manifest.json",
    outDir: "../backend/dashboard/static/dashboard",
    rollupOptions: {
      input: {
        "dashboard": "./src/main.tsx"
      }
    }
  },
  server: {
    open: '/dashboard/',
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      }
    }
  }
})
