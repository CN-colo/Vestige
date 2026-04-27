import { defineStore } from 'pinia'
import { ref } from 'vue'
import { articleApi, publicApi } from '@/api/articles'
import type { Article, ArticleCreate, ArticleUpdate } from '@/types'

export const useArticleStore = defineStore('article', () => {
  const articles = ref<Article[]>([])
  const currentArticle = ref<Article | null>(null)
  const publicArticles = ref<Article[]>([])
  const loading = ref(false)

  // Load user's articles
  const loadArticles = async (page = 1) => {
    loading.value = true
    try {
      articles.value = await articleApi.getList(page)
    } finally {
      loading.value = false
    }
  }

  // Load single article
  const loadArticle = async (id: number | string) => {
    loading.value = true
    try {
      const numericId = typeof id === 'string' ? parseInt(id, 10) : id
      currentArticle.value = await articleApi.get(numericId)
      return currentArticle.value
    } finally {
      loading.value = false
    }
  }

  // Create article
  const createArticle = async (data: ArticleCreate) => {
    const article = await articleApi.create(data)
    articles.value.unshift(article)
    return article
  }

  // Update article
  const updateArticle = async (id: number | string, data: ArticleUpdate) => {
    const numericId = typeof id === 'string' ? parseInt(id, 10) : id
    const article = await articleApi.update(numericId, data)
    const index = articles.value.findIndex(a => a.id === numericId)
    if (index !== -1) {
      articles.value[index] = article
    }
    currentArticle.value = article
    return article
  }

  // Delete article
  const deleteArticle = async (id: number) => {
    await articleApi.delete(id)
    articles.value = articles.value.filter(a => a.id !== id)
  }

  // Publish article
  const publishArticle = async (id: number) => {
    const article = await articleApi.publish(id)
    const index = articles.value.findIndex(a => a.id === id)
    if (index !== -1) {
      articles.value[index] = article
    }
    return article
  }

  // Unpublish article
  const unpublishArticle = async (id: number) => {
    const article = await articleApi.unpublish(id)
    const index = articles.value.findIndex(a => a.id === id)
    if (index !== -1) {
      articles.value[index] = article
    }
    return article
  }

  // Load public articles
  const loadPublicArticles = async (page = 1, search?: string) => {
    loading.value = true
    try {
      const response = await publicApi.getArticles(page, 10, search)
      publicArticles.value = response.items
      return response
    } finally {
      loading.value = false
    }
  }

  return {
    articles,
    currentArticle,
    publicArticles,
    loading,
    loadArticles,
    loadArticle,
    createArticle,
    updateArticle,
    deleteArticle,
    publishArticle,
    unpublishArticle,
    loadPublicArticles
  }
})