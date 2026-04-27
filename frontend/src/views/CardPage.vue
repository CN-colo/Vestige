<template>
  <div class="card-page">
    <el-card class="card-container" v-loading="loading" shadow="always">
      <div class="card-wrapper">
        <!-- 头部信息 -->
        <div class="card-header">
          <div class="avatar-section">
            <el-avatar :size="100" :src="cardData?.avatar">
              {{ cardData?.username?.charAt(0).toUpperCase() }}
            </el-avatar>
          </div>
          <div class="info-section">
            <h1 class="username">{{ cardData?.username }}</h1>
            <div class="contact">
              <el-icon><Message /></el-icon>
              <span>{{ cardData?.email }}</span>
            </div>
            <div class="contact-info" v-if="cardData?.contact">
              <el-icon><Phone /></el-icon>
              <span>{{ cardData?.contact }}</span>
            </div>
          </div>
        </div>

        <!-- 个人简介 -->
        <div class="bio-section" v-if="cardData?.bio">
          <h3>个人简介</h3>
          <MdPreview :modelValue="cardData.bio" class="bio-preview" />
        </div>
        
        <!-- 统计数据 -->
        <div class="stats-section">
          <div class="stat-box">
            <span class="stat-number">{{ cardData?.articles_count || 0 }}</span>
            <span class="stat-label">文章</span>
          </div>
          <div class="stat-box">
            <span class="stat-number">{{ cardData?.projects_count || 0 }}</span>
            <span class="stat-label">作品</span>
          </div>
        </div>
        
        <!-- 文章列表 -->
        <div class="articles-section" v-if="cardData?.articles?.length">
          <h2>文章作品</h2>
          <el-row :gutter="15">
            <el-col :xs="24" :sm="12" :md="8" v-for="article in cardData.articles" :key="article.id">
              <el-card class="item-card" shadow="hover" @click="goArticle(article.id)">
                <div class="item-cover" v-if="article.cover_image">
                  <img :src="article.cover_image" alt="" />
                </div>
                <h3>{{ article.title }}</h3>
                <p class="item-summary">{{ article.summary || '暂无摘要' }}</p>
                <div class="item-meta">
                  <span>{{ article.view_count }} 阅读</span>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
        
        <!-- 作品列表 -->
        <div class="projects-section" v-if="cardData?.projects?.length">
          <h2>项目作品</h2>
          <el-row :gutter="15">
            <el-col :xs="24" :sm="12" :md="8" v-for="project in cardData.projects" :key="project.id">
              <el-card class="item-card" shadow="hover" @click="goProject(project.id)">
                <div class="item-cover" v-if="project.cover_image">
                  <img :src="project.cover_image" alt="" />
                </div>
                <h3>{{ project.name }}</h3>
                <p class="item-summary">{{ project.description?.substring(0, 100) || '暂无描述' }}</p>
                <div class="item-meta">
                  <span>{{ project.view_count }} 查看</span>
                  <el-link v-if="project.url" :href="project.url" target="_blank" type="primary">
                    访问链接
                  </el-link>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
        
        <!-- 空状态 -->
        <el-empty
          v-if="!cardData?.articles?.length && !cardData?.projects?.length"
          description="暂无公开内容"
        />
        
        <!-- 底部 -->
        <div class="card-footer">
          <p>加入时间: {{ formatDate(cardData?.created_at) }}</p>
          <el-button type="primary" @click="$router.push('/')">
            发现更多
          </el-button>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Message, Phone } from '@element-plus/icons-vue'
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/preview.css'
import request from '@/api/request'

interface CardArticle {
  id: number
  title: string
  summary?: string
  cover_image?: string
  view_count: number
  published_at?: string
}

interface CardProject {
  id: number
  name: string
  description?: string
  cover_image?: string
  url?: string
  tech_stack?: string[]
  view_count: number
  published_at?: string
}

interface CardData {
  id: number
  username: string
  email: string
  avatar?: string
  bio?: string
  contact?: string
  articles_count: number
  projects_count: number
  articles: CardArticle[]
  projects: CardProject[]
  created_at: string
}

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const cardData = ref<CardData | null>(null)

onMounted(async () => {
  await loadCard()
})

async function loadCard() {
  loading.value = true
  try {
    const response = await request.get(`/public/card/${route.params.id}`)
    cardData.value = response
  } catch (error: any) {
    if (error.response?.status === 403) {
      ElMessage.error('该用户已关闭名片分享')
    } else {
      ElMessage.error('名片不存在或无法访问')
    }
    router.push('/')
  } finally {
    loading.value = false
  }
}

function formatDate(date?: string) {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long'
  })
}

function goArticle(id: number) {
  router.push(`/article/${id}`)
}

function goProject(id: number) {
  router.push(`/project/${id}`)
}
</script>

<style scoped>
.card-page {
  min-height: calc(100vh - 100px);
  padding: var(--spacing-lg);
  background: var(--bg-page);
}

.card-container {
  max-width: var(--content-max-width-narrow);
  margin: 0 auto;
  border-radius: var(--radius-xl);
  border: none;
  box-shadow: var(--shadow-md);
}

.card-wrapper {
  padding: var(--spacing-lg);
}

.card-header {
  display: flex;
  align-items: center;
  gap: var(--spacing-xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border-light);
}

.avatar-section {
  flex-shrink: 0;
}

.info-section {
  flex: 1;
}

.username {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
}

.bio-section {
  padding: var(--spacing-lg) 0;
  border-bottom: 1px solid var(--border-light);
}

.bio-section h3 {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.bio-preview {
  background: transparent;
}

.contact {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.contact-info {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  margin-top: var(--spacing-xs);
}

.stats-section {
  display: flex;
  justify-content: center;
  gap: var(--spacing-2xl);
  padding: var(--spacing-xl) 0;
  border-bottom: 1px solid var(--border-light);
}

.stat-box {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-number {
  font-size: var(--font-size-3xl);
  font-weight: var(--font-weight-bold);
  color: var(--primary-color);
}

.stat-label {
  color: var(--text-secondary);
  margin-top: var(--spacing-xs);
  font-size: var(--font-size-sm);
}

.articles-section,
.projects-section {
  padding: var(--spacing-xl) 0;
}

.articles-section h2,
.projects-section h2 {
  margin: 0 0 var(--spacing-lg) 0;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.item-card {
  margin-bottom: var(--spacing-md);
  cursor: pointer;
  border-radius: var(--radius-lg);
  border: none;
  box-shadow: var(--shadow-card);
  transition: all var(--transition-normal);
}

.item-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
}

.item-cover {
  width: 100%;
  height: 120px;
  overflow: hidden;
  margin-bottom: var(--spacing-sm);
  border-radius: var(--radius-md);
}

.item-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-card h3 {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-summary {
  color: var(--text-secondary);
  font-size: var(--font-size-xs);
  margin: 0 0 var(--spacing-xs) 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: var(--line-height-normal);
}

.item-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--font-size-xs);
  color: var(--text-muted);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-light);
}

.card-footer p {
  color: var(--text-secondary);
  margin: 0;
  font-size: var(--font-size-sm);
}

@media (max-width: 600px) {
  .card-header {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-md);
  }

  .info-section {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  .stats-section {
    gap: var(--spacing-lg);
  }

  .stat-number {
    font-size: var(--font-size-2xl);
  }
}

/* 手机端增强适配 */
@media (max-width: 767px) {
  .card-page {
    padding: var(--spacing-sm);
    min-height: calc(100vh - 60px);
  }

  .card-container {
    border-radius: var(--radius-lg);
  }

  .card-wrapper {
    padding: var(--spacing-sm);
  }

  .username {
    font-size: var(--font-size-xl);
  }

  .avatar-section .el-avatar {
    --el-avatar-size: 80px !important;
  }

  .bio-section {
    padding: var(--spacing-md) 0;
  }

  .stats-section {
    padding: var(--spacing-md) 0;
    gap: var(--spacing-xl);
  }

  .stat-number {
    font-size: var(--font-size-xl);
  }

  .stat-label {
    font-size: var(--font-size-xs);
  }

  .articles-section,
  .projects-section {
    padding: var(--spacing-md) 0;
  }

  .articles-section h2,
  .projects-section h2 {
    font-size: var(--font-size-base);
    margin-bottom: var(--spacing-md);
  }

  .item-cover {
    height: 100px;
  }

  .item-card h3 {
    font-size: 13px;
  }

  .item-summary {
    font-size: 11px;
  }

  .item-meta {
    font-size: 10px;
  }

  .card-footer {
    flex-direction: column;
    gap: var(--spacing-sm);
    padding-top: var(--spacing-md);
    text-align: center;
  }

  .card-footer .el-button {
    width: 100%;
  }

  :deep(.md-preview) {
    font-size: 13px;
  }
}
</style>