// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxt/ui'],
  css: ['~/assets/css/main.css'],
  ui: {
    fonts: false, // Полностью отключает интеграцию с @nuxt/fonts
  },
  runtimeConfig: {
    apiInternal: 'http://service.backend:8000/backend/api/v1/',
    public: {
      apiBase: '/backend/api/v1/' // для клиента
    },
  },  
  vite: {
    optimizeDeps: {
      include: [
        '@vue/devtools-core',
        '@vue/devtools-kit',
      ]
    }
  },
  // nitro: {
  //   devProxy: {
  //     '/backend': {
  //       target: 'http://service.backend:8000',
  //       changeOrigin: true
  //     }
  //   }
  // },  
})
