import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

export const useThemeStore = defineStore('theme', () => {
  // State
  const isDark = ref(false)
  const theme = ref('light')
  const systemPreference = ref('light')

  // Actions
  const initializeTheme = () => {
    // Check system preference
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    systemPreference.value = mediaQuery.matches ? 'dark' : 'light'

    // Check localStorage
    const savedTheme = localStorage.getItem('theme')
    
    if (savedTheme) {
      theme.value = savedTheme
      isDark.value = savedTheme === 'dark'
    } else {
      // Use system preference
      theme.value = systemPreference.value
      isDark.value = systemPreference.value === 'dark'
    }

    // Apply theme
    applyTheme()

    // Listen for system preference changes
    mediaQuery.addEventListener('change', (e) => {
      systemPreference.value = e.matches ? 'dark' : 'light'
      if (theme.value === 'system') {
        isDark.value = e.matches
        applyTheme()
      }
    })
  }

  const setTheme = (newTheme) => {
    theme.value = newTheme
    
    if (newTheme === 'system') {
      isDark.value = systemPreference.value === 'dark'
    } else {
      isDark.value = newTheme === 'dark'
    }
    
    localStorage.setItem('theme', newTheme)
    applyTheme()
  }

  const toggleTheme = () => {
    const newTheme = isDark.value ? 'light' : 'dark'
    setTheme(newTheme)
  }

  const applyTheme = () => {
    const root = document.documentElement
    
    if (isDark.value) {
      root.classList.add('dark')
    } else {
      root.classList.remove('dark')
    }

    // Update meta theme-color
    const metaThemeColor = document.querySelector('meta[name="theme-color"]')
    if (metaThemeColor) {
      metaThemeColor.setAttribute('content', isDark.value ? '#0f172a' : '#ffffff')
    }
  }

  // Watch for theme changes
  watch(isDark, () => {
    applyTheme()
  })

  return {
    // State
    isDark,
    theme,
    systemPreference,
    
    // Actions
    initializeTheme,
    setTheme,
    toggleTheme,
    applyTheme
  }
})

