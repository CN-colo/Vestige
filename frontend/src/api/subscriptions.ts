import request from './request'
import type { TagSubscriptionCreate, TagSubscriptionList, SubscriptionFeed } from '@/types'

export const subscriptionsApi = {
  // 订阅标签
  subscribe: (data: TagSubscriptionCreate): Promise<{ id: number; tag: string; created_at: string }> => {
    return request.post('/subscriptions', data)
  },

  // 取消订阅
  unsubscribe: (tag: string): Promise<void> => {
    return request.delete(`/subscriptions/${encodeURIComponent(tag)}`)
  },

  // 获取订阅列表
  getSubscriptions: (): Promise<TagSubscriptionList> => {
    return request.get('/subscriptions')
  },

  // 获取订阅推送内容
  getFeed: (page: number = 1, pageSize: number = 10): Promise<SubscriptionFeed> => {
    return request.get('/subscriptions/feed', { params: { page, page_size: pageSize } })
  },

  // 获取热门标签
  getPopularTags: (limit: number = 20): Promise<{ tag: string; count: number }[]> => {
    return request.get('/subscriptions/popular', { params: { limit } })
  }
}