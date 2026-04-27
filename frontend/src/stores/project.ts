import { defineStore } from 'pinia'
import { ref } from 'vue'
import { projectApi } from '@/api/projects'
import type { Project, ProjectCreate, ProjectUpdate } from '@/types'

export const useProjectStore = defineStore('project', () => {
  const projects = ref<Project[]>([])
  const currentProject = ref<Project | null>(null)
  const loading = ref(false)

  // Load user's projects
  const loadProjects = async (page = 1) => {
    loading.value = true
    try {
      projects.value = await projectApi.getList(page)
    } finally {
      loading.value = false
    }
  }

  // Load single project
  const loadProject = async (id: number) => {
    loading.value = true
    try {
      currentProject.value = await projectApi.get(id)
    } finally {
      loading.value = false
    }
  }

  // Create project
  const createProject = async (data: ProjectCreate) => {
    const project = await projectApi.create(data)
    projects.value.unshift(project)
    return project
  }

  // Update project
  const updateProject = async (id: number, data: ProjectUpdate) => {
    const project = await projectApi.update(id, data)
    const index = projects.value.findIndex(p => p.id === id)
    if (index !== -1) {
      projects.value[index] = project
    }
    currentProject.value = project
    return project
  }

  // Delete project
  const deleteProject = async (id: number) => {
    await projectApi.delete(id)
    projects.value = projects.value.filter(p => p.id !== id)
  }

  // Publish project
  const publishProject = async (id: number) => {
    const project = await projectApi.publish(id)
    const index = projects.value.findIndex(p => p.id === id)
    if (index !== -1) {
      projects.value[index] = project
    }
    return project
  }

  // Unpublish project
  const unpublishProject = async (id: number) => {
    const project = await projectApi.unpublish(id)
    const index = projects.value.findIndex(p => p.id === id)
    if (index !== -1) {
      projects.value[index] = project
    }
    return project
  }

  return {
    projects,
    currentProject,
    loading,
    loadProjects,
    loadProject,
    createProject,
    updateProject,
    deleteProject,
    publishProject,
    unpublishProject
  }
})