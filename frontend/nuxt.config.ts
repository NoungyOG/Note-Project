import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2024-11-01",
  devtools: { enabled: true },
  css: [
    '~/assets/css/main.css'
  ],
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  vite: {
    plugins: [tailwindcss()],
  },
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:5000/api'
    }
  },
  build: {
    transpile: ['v-calendar']
  },
  ssr: false,
  plugins: [
    { src: '~/plugins/v-calendar.client.js', mode: 'client' }
  ]
});