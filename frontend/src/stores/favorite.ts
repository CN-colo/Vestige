import { defineStore } from 'pinia'
import { ref } from 'vue'
import { favoritesApi } from '@/api/favorites'
import type { FavoriteWithItem } from '@/types'

export const useFavoriteStore = defineStore('favorite', () => {
  const favorites = ref<FavoriteWithItem[]>([])
  const loading = ref(false)

  // Load favorites
  const loadFavorites = async (targetType?: 'article' | 'project', page = 1) => {
    loading.value = true
    try {
      favorites.value = await favoritesApi.list(targetType, page, 20)
    } finally {
      loading.value = false
    }
  }

  // Add favorite
  const addFavorite = async (targetType: 'article' | 'project', targetId: number) => {
    const favorite = await favoritesApi.add({ target_type: targetType, target_id: targetId })
    favorites.value.unshift(favorite)
    return favorite
  }

  // Remove favorite
  const removeFavorite = async (targetType: 'article' | 'project', targetId: number) => {
    await favoritesApi.remove(targetType, targetId)
    favorites.value = favorites.value.filter(
      f => f.target_type !== targetType || f.target_id !== targetId
    )
  }

  // Check if favorited (returns boolean)
  const isFavorited = async (targetType: 'article' | 'project', targetId: number): Promise<boolean> => {
    try {
      const result = await favoritesApi.check(targetType, targetId)
      return result.is_favorited
    } catch {
      return false
    }
  }

  // Toggle favorite
  const toggleFavorite = async (targetType: 'article' | 'project', targetId: number): Promise<boolean> => {
    const isCurrentlyFavorited = await isFavorited(targetType, targetId)
    if (isCurrentlyFavorited) {
      await removeFavorite(targetType, targetId)
      return false
    } else {
      await addFavorite(targetType, targetId)
      return true
    }
  }

  return {
    favorites,
    loading,
    loadFavorites,
    addFavorite,
    removeFavorite,
    isFavorited,
    toggleFavorite
  }
})