import { defineConfig } from 'vite'

export default defineConfig({
  css: {
    postcss: './postcss.config.js'
  },
  build: {
    outDir: 'static',
    rollupOptions: {
      input: 'src/style.css',
      output: {
        assetFileNames: '[name].[ext]'
      }
    }
  }
})
