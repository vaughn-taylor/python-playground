import { defineConfig } from 'vite'

export default defineConfig({
  root: './frontend',
  build: {
    outDir: '../static',
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: './frontend/main.js'
    }
  }
})
