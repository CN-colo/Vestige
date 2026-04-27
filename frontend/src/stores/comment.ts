import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getComments, createComment, updateComment, deleteComment } from '@/api/comments'
import type { Comment, CommentCreate, CommentUpdate } from '@/types'

export const useCommentStore = defineStore('comment', () => {
  const comments = ref<Comment[]>([])
  const loading = ref(false)

  const loadComments = async (contentType: 'article' | 'project', contentId: number) => {
    loading.value = true
    try {
      comments.value = await getComments(contentType, contentId)
    } finally {
      loading.value = false
    }
  }

  const addComment = async (data: CommentCreate) => {
    const comment = await createComment(data)
    if (data.parent_id) {
      // Add as reply to parent comment
      const parentIndex = comments.value.findIndex(c => c.id === data.parent_id)
      if (parentIndex !== -1) {
        if (!comments.value[parentIndex].replies) {
          comments.value[parentIndex].replies = []
        }
        comments.value[parentIndex].replies!.push(comment)
      }
    } else {
      // Add as top-level comment
      comments.value.unshift(comment)
    }
    return comment
  }

  const editComment = async (commentId: number, data: CommentUpdate, parentId?: number) => {
    const comment = await updateComment(commentId, data)
    if (parentId) {
      const parentIndex = comments.value.findIndex(c => c.id === parentId)
      if (parentIndex !== -1 && comments.value[parentIndex].replies) {
        const replyIndex = comments.value[parentIndex].replies!.findIndex(r => r.id === commentId)
        if (replyIndex !== -1) {
          comments.value[parentIndex].replies![replyIndex] = comment
        }
      }
    } else {
      const index = comments.value.findIndex(c => c.id === commentId)
      if (index !== -1) {
        comments.value[index] = comment
      }
    }
    return comment
  }

  const removeComment = async (commentId: number, parentId?: number) => {
    await deleteComment(commentId)
    if (parentId) {
      const parentIndex = comments.value.findIndex(c => c.id === parentId)
      if (parentIndex !== -1 && comments.value[parentIndex].replies) {
        comments.value[parentIndex].replies = comments.value[parentIndex].replies!.filter(r => r.id !== commentId)
      }
    } else {
      comments.value = comments.value.filter(c => c.id !== commentId)
    }
  }

  const clearComments = () => {
    comments.value = []
  }

  return {
    comments,
    loading,
    loadComments,
    addComment,
    editComment,
    removeComment,
    clearComments
  }
})