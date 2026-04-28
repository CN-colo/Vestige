import request from './request'
import type { Article, ArticleCreate, ArticleUpdate, PaginatedResponse, Project, UserPublic } from '@/types'

export const articleApi = {
  // Get user's articles
  getList: (page = 1, pageSize = 10): Promise<Article[]> => {
    return request.get('/articles', { params: { page, page_size: pageSize } })
  },

  // Create article
  create: (data: ArticleCreate): Promise<Article> => {
    return request.post('/articles', data)
  },

  // Get article detail
  get: (id: number): Promise<Article> => {
    return request.get(`/articles/${id}`)
  },

  // Update article
  update: (id: number, data: ArticleUpdate): Promise<Article> => {
    return request.put(`/articles/${id}`, data)
  },

  // Delete article
  delete: (id: number): Promise<void> => {
    return request.delete(`/articles/${id}`)
  },

  // Publish article
  publish: (id: number): Promise<Article> => {
    return request.post(`/articles/${id}/publish`)
  },

  // Unpublish article
  unpublish: (id: number): Promise<Article> => {
    return request.post(`/articles/${id}/unpublish`)
  }
}

export const publicApi = {
  // Get public articles
  getArticles: (page = 1, pageSize = 10, search?: string, tag?: string): Promise<PaginatedResponse<Article>> => {
    return request.get('/public/articles', { params: { page, page_size: pageSize, search, tag } })
  },

  // Get public article detail
  getArticle: (id: number): Promise<Article> => {
    return request.get(`/public/articles/${id}`)
  },

  // Get public projects
  getProjects: (page = 1, pageSize = 10, search?: string, tag?: string): Promise<PaginatedResponse<Project>> => {
    return request.get('/public/projects', { params: { page, page_size: pageSize, search, tag } })
  },

  // Get public project detail
  getProject: (id: number): Promise<Project> => {
    return request.get(`/public/projects/${id}`)
  },

  // Get all public content (articles and projects combined)
  getAll: (page = 1, pageSize = 10, search?: string, tag?: string, contentType?: 'all' | 'article' | 'project'): Promise<PaginatedResponse<any>> => {
    return request.get('/public/all', { params: { page, page_size: pageSize, search, tag, content_type: contentType } })
  },

  // Get all available tags
  getTags: (): Promise<{ tags: string[] }> => {
    return request.get('/public/tags')
  },

  // Get user public profile
  getUser: (id: number): Promise<UserPublic> => {
    return request.get(`/public/users/${id}`)
  },

  // Get agent guide URL
  getAgentGuide: (): Promise<{ agent_guide_url: string; ai_api_url: string }> => {
    return request.get('/public/agent-guide')
  }
}