import request from './request'
import type { FollowRequest, FollowStats, UserWithFollowStatus } from '@/types'

export const followsApi = {
  // 关注用户
  follow: (data: FollowRequest): Promise<UserWithFollowStatus> => {
    return request.post('/follows', data)
  },

  // 取消关注
  unfollow: (userId: number): Promise<void> => {
    return request.delete(`/follows/${userId}`)
  },

  // 获取我关注的人列表
  getFollowing: (): Promise<UserWithFollowStatus[]> => {
    return request.get('/follows/following')
  },

  // 获取我的粉丝列表
  getFollowers: (): Promise<UserWithFollowStatus[]> => {
    return request.get('/follows/followers')
  },

  // 获取关注统计
  getStats: (): Promise<FollowStats> => {
    return request.get('/follows/stats')
  },

  // 获取指定用户的关注信息
  getUserFollowInfo: (userId: number): Promise<UserWithFollowStatus> => {
    return request.get(`/follows/user/${userId}`)
  },

  // 检查是否关注了指定用户
  checkFollowing: (userId: number): Promise<{ is_following: boolean }> => {
    return request.get(`/follows/check/${userId}`)
  }
}