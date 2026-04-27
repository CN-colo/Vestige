import request from './request'
import type { Project, ProjectCreate, ProjectUpdate } from '@/types'

export const projectApi = {
  // Get user's projects
  getList: (page = 1, pageSize = 10): Promise<Project[]> => {
    return request.get('/projects', { params: { page, page_size: pageSize } })
  },

  // Create project
  create: (data: ProjectCreate): Promise<Project> => {
    return request.post('/projects', data)
  },

  // Get project detail
  get: (id: number): Promise<Project> => {
    return request.get(`/projects/${id}`)
  },

  // Update project
  update: (id: number, data: ProjectUpdate): Promise<Project> => {
    return request.put(`/projects/${id}`, data)
  },

  // Delete project
  delete: (id: number): Promise<void> => {
    return request.delete(`/projects/${id}`)
  },

  // Publish project
  publish: (id: number): Promise<Project> => {
    return request.post(`/projects/${id}/publish`)
  },

  // Unpublish project
  unpublish: (id: number): Promise<Project> => {
    return request.post(`/projects/${id}/unpublish`)
  }
}