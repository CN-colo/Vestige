import request from './request'
import type { ApiKey, ApiKeyCreate, ApiKeyCreated, ApiKeyUpdate } from '@/types'

export const apiKeyApi = {
  // Get user's API keys
  getList: (): Promise<ApiKey[]> => {
    return request.get('/keys')
  },

  // Create API key
  create: (data: ApiKeyCreate): Promise<ApiKeyCreated> => {
    return request.post('/keys', data)
  },

  // Update API key
  update: (id: number, data: ApiKeyUpdate): Promise<ApiKey> => {
    return request.put(`/keys/${id}`, data)
  },

  // Delete API key
  delete: (id: number): Promise<void> => {
    return request.delete(`/keys/${id}`)
  }
}