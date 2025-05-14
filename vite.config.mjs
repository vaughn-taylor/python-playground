
import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

export default defineConfig({
  root: './frontend',
  base: '/static/assets/',
  build: {
    outDir: '../static/assets',
    assetsDir: '.',
    emptyOutDir: true,
    manifest: true,
    manifestDir: '.',
    rollupOptions: {
      input: path.resolve(__dirname, 'frontend/main.js')
    }
  },
  plugins: [tailwindcss()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'frontend'),
    },
  },
})
