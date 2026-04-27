import request from './request'
import type { Comment, CommentCreate, CommentUpdate } from '@/types'

export const getComments = (contentType: 'article' | 'project', contentId: number) => {
  return request.get<Comment[]>('/comments', {
    params: {
      content_type: contentType,
      content_id: contentId
    }
  })
}

export const createComment = (data: CommentCreate) => {
  return request.post<Comment>('/comments', data)
}

export const updateComment = (commentId: number, data: CommentUpdate) => {
  return request.put<Comment>(`/comments/${commentId}`, data)
}

export const deleteComment = (commentId: number) => {
  return request.delete(`/comments/${commentId}`)
}