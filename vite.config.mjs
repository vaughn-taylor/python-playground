import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  root: './src/frontend',
  build: {
    outDir: '../../static',
    emptyOutDir: true,
    manifest: true,
    manifestDir: '.',
    rollupOptions: {
      input: './src/frontend/main.js'
    }
  },
  plugins: [tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src/frontend'),
    },
  },
})
