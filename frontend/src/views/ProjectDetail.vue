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
  max-width: 800px;
  margin: 0 auto;
}

.project-header {
  margin-bottom: 20px;
}

.project-header h1 {
  margin: 0 0 15px 0;
  font-size: 28px;
}

.meta {
  display: flex;
  align-items: center;
  gap: 15px;
  color: var(--el-text-color-secondary);
}

.author {
  display: flex;
  align-items: center;
  gap: 5px;
  cursor: pointer;
}

.tech-stack {
  margin-top: 10px;
}

.actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  align-items: center;
}

.cover-image {
  width: 100%;
  max-height: 400px;
  object-fit: cover;
  margin-bottom: 20px;
}

.project-description {
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.project-url {
  margin-bottom: 20px;
}

.tags {
  margin-top: 15px;
}
</style>