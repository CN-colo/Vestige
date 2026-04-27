<template>
  <div class="article-detail-page">
    <el-card v-loading="loading">
      <div class="article-header">
        <h1>{{ article?.title }}</h1>
        <div class="meta">
          <span class="author" v-if="article?.author?.id != null" @click="$router.push(`/user/${article.author.id}`)">
            <el-avatar :size="24">
              {{ article?.author?.username?.charAt(0).toUpperCase() }}
            </el-avatar>
            {{ article?.author?.username }}
          </span>
          <span class="author" v-else>
            <el-avatar :size="24">?</el-avatar>
            未知作者
          </span>
          <span class="date">{{ formatDate(article?.published_at) }}</span>
          <span class="views">{{ article?.view_count }} 次阅读</span>
        </div>
        <div class="tags">
          <TagSubscribeButton 
            v-for="tag in article?.tags" 
            :key="tag" 
            :tag="tag"
          />
        </div>
        <div class="actions" v-if="userStore.isLoggedIn">
          <LikeButton 
            targetType="article"
            :targetId="article?.id || 0"
            :initialLikeCount="article?.like_count"
            :showCount="true"
          />
          <el-button 
            :type="isFavorited ? 'danger' : 'default'" 
            :icon="isFavorited ? StarFilled : Star"
            @click="handleFavorite"
            :loading="favoriteLoading"
          >
            {{ isFavorited ? '已收藏' : '收藏' }}
          </el-button>
        </div>
      </div>

      <img v-if="article?.cover_image" :src="article?.cover_image" class="cover-image" />

      <div class="article-content">
        <MdPreview :modelValue="article?.content || ''" language="zh-CN" />
      </div>

      <!-- Comment section -->
      <CommentSection contentType="article" :contentId="Number(route.params.id)" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Star, StarFilled } from '@element-plus/icons-vue'
import { publicApi, articleApi } from '@/api/articles'
import { useUserStore } from '@/stores/user'
import { useFavoriteStore } from '@/stores/favorite'
import LikeButton from '@/components/LikeButton.vue'
import TagSubscribeButton from '@/components/TagSubscribeButton.vue'
import type { Article } from '@/types'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import CommentSection from '@/components/CommentSection.vue'

const route = useRoute()
const userStore = useUserStore()
const favoriteStore = useFavoriteStore()
const loading = ref(false)
const favoriteLoading = ref(false)
const article = ref<Article | null>(null)
const isFavorited = ref(false)

const formatDate = (date?: string) => {
  if (!date) return ''
  return new Date(date).toLocaleString('zh-CN')
}

const handleFavorite = async () => {
  if (!article.value) return
  favoriteLoading.value = true
  try {
    const result = await favoriteStore.toggleFavorite('article', article.value.id)
    isFavorited.value = result
    ElMessage.success(result ? '已添加到收藏' : '已取消收藏')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    favoriteLoading.value = false
  }
}

onMounted(async () => {
  loading.value = true
  try {
    // If logged in, try to get user's own article first (including unpublished)
    if (userStore.isLoggedIn) {
      try {
        article.value = await articleApi.get(Number(route.params.id))
        // Check if favorited
        if (article.value) {
          isFavorited.value = await favoriteStore.isFavorited('article', article.value.id)
        }
      } catch {
        // Not the author, try public API
        article.value = await publicApi.getArticle(Number(route.params.id))
        if (article.value) {
          isFavorited.value = await favoriteStore.isFavorited('article', article.value.id)
        }
      }
    } else {
      // Not logged in, use public API
      article.value = await publicApi.getArticle(Number(route.params.id))
    }
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.article-detail-page {
  max-width: var(--content-max-width-narrow);
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.el-card {
  border-radius: var(--radius-lg);
  border: none;
  box-shadow: var(--shadow-card);
}

.article-header {
  margin-bottom: var(--spacing-lg);
}

.article-header h1 {
  margin: 0 0 var(--spacing-md) 0;
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  line-height: var(--line-height-tight);
}

.meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.author {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  cursor: pointer;
  transition: color var(--transition-fast);
}

.author:hover {
  color: var(--primary-color);
}

.tags {
  margin-top: var(--spacing-sm);
}

.actions {
  margin-top: var(--spacing-md);
  display: flex;
  gap: var(--spacing-sm);
  align-items: center;
}

.cover-image {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  margin-bottom: var(--spacing-lg);
  border-radius: var(--radius-lg);
}

.article-content {
  margin-top: var(--spacing-lg);
}
</style>