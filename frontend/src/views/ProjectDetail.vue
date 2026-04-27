<template>
  <div class="project-detail-page">
    <el-card v-loading="loading">
      <div class="project-header">
        <h1>{{ project?.name }}</h1>
        <div class="meta">
          <span class="author" v-if="project?.author?.id != null" @click="$router.push(`/user/${project.author.id}`)">
            <el-avatar :size="24">
              {{ project?.author?.username?.charAt(0).toUpperCase() }}
            </el-avatar>
            {{ project?.author?.username }}
          </span>
          <span class="author" v-else>
            <el-avatar :size="24">?</el-avatar>
            未知作者
          </span>
          <span class="date">{{ formatDate(project?.published_at) }}</span>
          <span class="views">{{ project?.view_count }} 次查看</span>
        </div>
        <div class="tech-stack">
          <el-tag v-for="tech in project?.tech_stack" :key="tech" size="small" type="success">{{ tech }}</el-tag>
        </div>
        <div class="actions" v-if="userStore.isLoggedIn">
          <LikeButton 
            targetType="project"
            :targetId="project?.id || 0"
            :initialLikeCount="project?.like_count"
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

      <img v-if="project?.cover_image" :src="project?.cover_image" class="cover-image" />

      <div class="project-description">
        <MdPreview :modelValue="project?.description || ''" language="zh-CN" />
      </div>

      <div class="project-url" v-if="project?.url">
        <el-button type="primary" @click="openUrl(project?.url)">
          <el-icon><Link /></el-icon>
          访问项目
        </el-button>
      </div>

      <div class="tags">
        <TagSubscribeButton 
          v-for="tag in project?.tags" 
          :key="tag" 
          :tag="tag"
        />
      </div>

      <!-- Comment section -->
      <CommentSection contentType="project" :contentId="Number(route.params.id)" />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Star, StarFilled } from '@element-plus/icons-vue'
import { publicApi } from '@/api/articles'
import { projectApi } from '@/api/projects'
import { useUserStore } from '@/stores/user'
import { useFavoriteStore } from '@/stores/favorite'
import LikeButton from '@/components/LikeButton.vue'
import TagSubscribeButton from '@/components/TagSubscribeButton.vue'
import type { Project } from '@/types'
import CommentSection from '@/components/CommentSection.vue'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

const route = useRoute()
const userStore = useUserStore()
const favoriteStore = useFavoriteStore()
const loading = ref(false)
const favoriteLoading = ref(false)
const project = ref<Project | null>(null)
const isFavorited = ref(false)

const formatDate = (date?: string) => {
  if (!date) return ''
  return new Date(date).toLocaleString('zh-CN')
}

const openUrl = (url?: string) => {
  if (url) {
    window.open(url, '_blank')
  }
}

const handleFavorite = async () => {
  if (!project.value) return
  favoriteLoading.value = true
  try {
    const result = await favoriteStore.toggleFavorite('project', project.value.id)
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
    // If logged in, try to get user's own project first (including unpublished)
    if (userStore.isLoggedIn) {
      try {
        project.value = await projectApi.get(Number(route.params.id))
        // Check if favorited
        if (project.value) {
          isFavorited.value = await favoriteStore.isFavorited('project', project.value.id)
        }
      } catch {
        // Not the author, try public API
        project.value = await publicApi.getProject(Number(route.params.id))
        if (project.value) {
          isFavorited.value = await favoriteStore.isFavorited('project', project.value.id)
        }
      }
    } else {
      // Not logged in, use public API
      project.value = await publicApi.getProject(Number(route.params.id))
    }
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.project-detail-page {
  max-width: var(--content-max-width-narrow);
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.el-card {
  border-radius: var(--radius-lg);
  border: none;
  box-shadow: var(--shadow-card);
}

.project-header {
  margin-bottom: var(--spacing-lg);
}

.project-header h1 {
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

.tech-stack {
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

.project-description {
  font-size: var(--font-size-base);
  line-height: var(--line-height-relaxed);
  margin-bottom: var(--spacing-lg);
}

.project-url {
  margin-bottom: var(--spacing-lg);
}

.tags {
  margin-top: var(--spacing-md);
}

/* 手机端适配 */
@media (max-width: 767px) {
  .project-detail-page {
    padding: var(--spacing-sm);
  }

  .project-header h1 {
    font-size: var(--font-size-xl);
    line-height: 1.3;
  }

  .meta {
    flex-wrap: wrap;
    gap: var(--spacing-sm);
    font-size: var(--font-size-xs);
  }

  .tech-stack {
    margin-top: var(--spacing-xs);
  }

  .actions {
    flex-wrap: wrap;
  }

  .cover-image {
    max-height: 200px;
    margin-bottom: var(--spacing-md);
  }

  .project-description {
    margin-bottom: var(--spacing-md);
  }

  .project-url {
    margin-bottom: var(--spacing-md);
  }

  .tags {
    margin-top: var(--spacing-sm);
  }

  :deep(.md-preview) {
    font-size: 14px;
  }
}

/* 平板适配 */
@media (min-width: 768px) and (max-width: 1023px) {
  .project-detail-page {
    padding: var(--spacing-md);
  }

  .project-header h1 {
    font-size: var(--font-size-2xl);
  }
}
</style>