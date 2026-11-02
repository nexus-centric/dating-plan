import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { VitePWA } from 'vite-plugin-pwa'
export default defineConfig({
  base: process.env.VITE_BASE || '/',
  plugins: [react(), VitePWA({
    registerType: 'autoUpdate',
    includeAssets: ['icon.svg'],
    workbox: { globPatterns: ['**/*.{js,css,html,svg,woff2}'] },
    manifest: { name: 'Hẹn Hò Sài Gòn', short_name: 'HẹnHò', lang: 'vi', description: 'Lên kế hoạch hẹn hò ở trung tâm TP.HCM',
      theme_color: '#fdf8f9', background_color: '#fdf8f9', display: 'standalone', start_url: '.', scope: '.',
      icons: [{ src: 'icon.svg', sizes: 'any', type: 'image/svg+xml', purpose: 'any maskable' }] },
  })],
})
