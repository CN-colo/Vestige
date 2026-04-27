<template>
  <div class="user-page">
    <el-empty v-if="!loading && !user" description="用户不存在" />
    <el-card v-loading="loading" v-if="user">
      <div class="user-header">
        <el-avatar :size="64" :src="user?.avatar">
          {{ user?.username?.charAt(0).toUpperCase() }}
        </el-avatar>
        <div class="user-info">
          <h2>{{ user?.username }}</h2>
          <div class="bio-wrapper" v-if="user?.bio">
            <MdPreview :modelValue="user.bio" class="bio-preview" />
          </div>
          <p class="bio" v-else>这个人很懒，什么都没写...</p>
          <div class="stats">
            <span>{{ user?.articles_count || 0 }} 篇文章</span>
            <span>{{ user?.projects_count || 0 }} 个作品</span>
            <span>{{ followStats.following_count }} 关注</span>
            <span>{{ followStats.followers_count }} 粉丝</span>
          </div>
        </div>
        <div class="user-actions" v-if="userStore.isLoggedIn && userStore.user?.id !== Number(route.params.id)">
          <FollowButton :userId="Number(route.params.id)" @change="onFollowChange" />
        </div>
      </div>
    </el-card>

    <el-tabs v-model="activeTab" style="margin-top: 20px" v-if="user">
      <el-tab-pane label="文章" name="articles">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" v-for="article in articles" :key="article.id">
            <el-card class="content-card" shadow="hover" @click="$router.push(`/article/${article.id}`)">
              <h3>{{ article.title }}</h3>
              <p>{{ article.summary || article.content.substring(0, 100) }}</p>
              <div class="meta">{{ article.view_count }} 次阅读</div>
            </el-card>
          </el-col>
        </el-row>
        <el-empty v-if="articles.length === 0" description="暂无公开文章" />
      </el-tab-pane>

      <el-tab-pane label="作品" name="projects">
        <el-row :gutter="20">
          <el-col :xs="24" :sm="12" :md="8" v-for="project in projects" :key="project.id">
            <el-card class="content-card" shadow="hover" @click="$router.push(`/project/${project.id}`)">
              <h3>{{ project.name }}</h3>
              <p>{{ project.description.substring(0, 100) }}</p>
              <div class="meta">{{ project.view_count }} 次查看</div>
            </el-card>
          </el-col>
        </el-row>
        <el-empty v-if="projects.length === 0" description="暂无公开作品" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/preview.css'
import { publicApi } from '@/api/articles'
import { useFollowStore } from '@/stores/follow'
import { useUserStore } from '@/stores/user'
import FollowButton from '@/components/FollowButton.vue'
import type { UserPublic, Article, Project, FollowStats } from '@/types'

const route = useRoute()
const followStore = useFollowStore()
const userStore = useUserStore()
const loading = ref(false)
const activeTab = ref('articles')
const user = ref<UserPublic | null>(null)
const articles = ref<Article[]>([])
const projects = ref<Project[]>([])
const followStats = ref<FollowStats>({ following_count: 0, followers_count: 0 })

onMounted(async () => {
  const userId = Number(route.params.id)
  
  // 检查路由参数是否有效
  if (!userId || userId <= 0 || isNaN(userId)) {
    loading.value = false
    return
  }
  
  loading.value = true
  try {
    user.value = await publicApi.getUser(userId)
    
    // Load follow stats
    if (userStore.isLoggedIn) {
      const info = await followStore.getUserFollowInfo(userId)
      followStats.value = {
        following_count: info.following_count,
        followers_count: info.followers_count
      }
    }
    
    // Load user's public articles
    const articlesRes = await publicApi.getArticles(1, 20)
    articles.value = (articlesRes as any).items?.filter(
      (a: any) => a.author?.id === userId
    ) || []
    
    // Load user's public projects  
    const projectsRes = await publicApi.getProjects(1, 20)
    projects.value = (projectsRes as any).items?.filter(
      (p: any) => p.author?.id === userId
    ) || []
  } finally {
    loading.value = false
  }
})

// 关注状态变化时更新统计
const onFollowChange = (isFollowing: boolean) => {
  followStats.value.followers_count = isFollowing 
    ? followStats.value.followers_count + 1 
    : followStats.value.followers_count - 1
}
</script>

<style scoped>
.user-page {
  max-width: var(--content-max-width-narrow);
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.el-card {
  border-radius: var(--radius-lg);
  border: none;
  box-shadow: var(--shadow-card);
}

.user-header {
  display: flex;
  gap: var(--spacing-lg);
  align-items: center;
}

.user-actions {
  margin-left: auto;
}

.user-info h2 {
  margin: 0;
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.user-info .bio {
  color: var(--text-secondary);
  margin: var(--spacing-sm) 0;
  font-size: var(--font-size-sm);
}

.user-info .bio-wrapper {
  margin: var(--spacing-sm) 0;
}

.user-info .bio-preview {
  background: transparent;
}

.user-info .stats {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.user-info .stats span {
  margin-right: var(--spacing-md);
}

.el-tabs {
  margin-top: var(--spacing-lg);
}

.content-card {
  margin-bottom: var(--spacing-lg);
  cursor: pointer;
  border-radius: var(--radius-lg);
  border: none;
  box-shadow: var(--shadow-card);
  transition: all var(--transition-normal);
}

.content-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
}

.content-card h3 {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.content-card p {
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-size-sm);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.content-card .meta {
  color: var(--text-muted);
  font-size: var(--font-size-xs);
}
</style>