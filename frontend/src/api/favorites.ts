import request from './request'
import type { FavoriteWithItem, FavoriteCreate } from '@/types'

export const favoritesApi = {
  // Add favorite
  add(data: FavoriteCreate): Promise<FavoriteWithItem> {
    return request.post('/favorites', data)
  },

  // Remove favorite
  remove(targetType: 'article' | 'project', targetId: number): Promise<void> {
    return request.delete('/favorites', {
      params: {
        target_type: targetType,
        target_id: targetId
      }
    })
  },

  // Get favorites list
  list(targetType?: 'article' | 'project', page = 1, pageSize = 10): Promise<FavoriteWithItem[]> {
    return request.get('/favorites', {
      params: {
        target_type: targetType,
        page,
        page_size: pageSize
      }
    })
  },

  // Check if favorited
  check(targetType: 'article' | 'project', targetId: number): Promise<{ is_favorited: boolean }> {
    return request.get('/favorites/check', {
      params: {
        target_type: targetType,
        target_id: targetId
      }
    })
  }
}