import request from './request'
import type { User, LoginRequest, RegisterRequest, TokenResponse } from '@/types'

export const authApi = {
  // Register
  register: (data: RegisterRequest): Promise<User> => {
    return request.post('/auth/register', data)
  },

  // Login
  login: (data: LoginRequest): Promise<TokenResponse> => {
    return request.post('/auth/login', data)
  },

  // Get current user
  getMe: (): Promise<User> => {
    return request.get('/auth/me')
  },

  // Update current user
  updateMe: (data: Partial<User>): Promise<User> => {
    return request.put('/auth/me', data)
  }
}