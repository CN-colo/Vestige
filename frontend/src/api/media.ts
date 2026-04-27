import request from './request'
import type { Media } from '@/types'

export const mediaApi = {
  // Upload media
  upload: async (file: File): Promise<Media> => {
    const formData = new FormData()
    formData.append('file', file)
    return request.post('/media/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }) as Promise<Media>
  },

  // Get media info
  get: (id: number): Promise<Media> => {
    return request.get(`/media/${id}`) as Promise<Media>
  },

  // Delete media
  delete: (id: number): Promise<void> => {
    return request.delete(`/media/${id}`) as Promise<void>
  }
}