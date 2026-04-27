import request from './request'
import type { LikeRequest, LikeStatus, Like } from '@/types'

export const likesApi = {
  // 点赞
  like: (data: LikeRequest): Promise<Like> => {
    return request.post('/likes', data)
  },

  // 取消点赞
  unlike: (targetType: 'article' | 'project', targetId: number): Promise<void> => {
    return request.delete(`/likes/${targetType}/${targetId}`)
  },

  // 获取点赞状态
  getStatus: (targetType: 'article' | 'project', targetId: number): Promise<LikeStatus> => {
    return request.get(`/likes/status/${targetType}/${targetId}`)
  },

  // 获取我的点赞列表
  getMyLikes: (targetType?: 'article' | 'project'): Promise<Like[]> => {
    const params = targetType ? { target_type: targetType } : {}
    return request.get('/likes/my', { params })
  },

  // 获取点赞用户列表
  getLikeUsers: (targetType: 'article' | 'project', targetId: number, limit: number = 20): Promise<{ users: { id: number; username: string; avatar?: string }[]; total: number }> => {
    return request.get(`/likes/users/${targetType}/${targetId}`, { params: { limit } })
  }
}