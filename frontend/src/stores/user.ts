import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'
import type { User, LoginRequest, RegisterRequest } from '@/types'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))

  const isLoggedIn = computed(() => !!user.value && !!token.value)

  // Initialize user from stored token
  const initUser = async () => {
    if (token.value) {
      try {
        const userData = await authApi.getMe()
        user.value = userData
      } catch (error) {
        logout()
      }
    }
  }

  // Login
  const login = async (data: LoginRequest) => {
    const response = await authApi.login(data)
    token.value = response.access_token
    localStorage.setItem('token', response.access_token)
    await initUser()
  }

  // Register
  const register = async (data: RegisterRequest) => {
    await authApi.register(data)
  }

  // Logout
  const logout = () => {
    user.value = null
    token.value = null
    localStorage.removeItem('token')
  }

  // Update user info
  const updateUser = async (data: Partial<User>) => {
    if (user.value) {
      const updated = await authApi.updateMe(data)
      user.value = updated
    }
  }

  return {
    user,
    token,
    isLoggedIn,
    initUser,
    login,
    register,
    logout,
    updateUser
  }
})