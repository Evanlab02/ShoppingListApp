import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react-swc'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: "/shopping/dashboard/",
  server: {
    open: '/shopping/dashboard/',
    proxy: {
      '/apis/shopping': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
