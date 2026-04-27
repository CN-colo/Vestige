<template>
  <div class="home-page">
    <div class="page-header">
      <div class="header-left">
        <h2>公开广场</h2>
      </div>
      <div class="header-right">
        <el-button type="primary" @click="$router.push('/ai-api')">
          <el-icon><Document /></el-icon>
          AI API 文档
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选区域 -->
    <div class="filter-section">
      <div class="search-row">
        <el-input
          v-model="searchQuery"
          placeholder="搜索内容..."
          clearable
          @input="handleSearch"
          class="search-input"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>

      <!-- 类型筛选 -->
      <div class="type-filter">
        <el-radio-group v-model="contentType" @change="loadContent">
          <el-radio-button value="all">全部</el-radio-button>
          <el-radio-button value="article">文章</el-radio-button>
          <el-radio-button value="project">作品</el-radio-button>
        </el-radio-group>
      </div>

      <!-- 标签筛选 -->
      <div class="tag-filter" v-if="allTags.length > 0">
        <span class="tag-label">标签筛选：</span>
        <el-tag
          v-for="tag in allTags.slice(0, 20)"
          :key="tag"
          :type="selectedTag === tag ? 'primary' : 'info'"
          :effect="selectedTag === tag ? 'dark' : 'plain'"
          class="tag-item"
          @click="handleTagClick(tag)"
        >
          {{ tag }}
        </el-tag>
        <el-tag v-if="selectedTag" type="danger" class="tag-item clear-tag" @click="clearTag">
          清除
        </el-tag>
      </div>
    </div>

    <!-- 内容列表 -->
    <el-row :gutter="20" v-loading="loading">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="item in contentList" :key="`${item.type}-${item.id}`">
        <el-card class="content-card" shadow="hover" @click="handleItemClick(item)">
          <img v-if="item.cover_image" :src="item.cover_image" class="cover-image" />
          <div class="card-content">
            <!-- 类型标签 -->
            <el-tag :type="item.type === 'article' ? 'primary' : 'success'" size="small" class="type-tag">
              {{ item.type === 'article' ? '文章' : '作品' }}
            </el-tag>
            <h3 class="title">{{ item.title }}</h3>
            <p class="summary">{{ item.summary || item.content?.substring(0, 100) }}</p>
            <div class="meta">
              <el-tag v-for="tag in getDisplayTags(item).slice(0, 3)" :key="tag" size="small" class="content-tag">
                {{ tag }}
              </el-tag>
              <span class="author">{{ item.author?.username }}</span>
              <span class="views">{{ item.view_count }} 次查看</span>
              <span class="date">{{ formatDate(item.created_at) }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-empty v-if="!loading && contentList.length === 0" description="暂无公开内容" />

    <!-- 分页 -->
    <div class="pagination-section" v-if="totalPages > 1">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="loadContent"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { publicApi } from '@/api/articles'
import { Document } from '@element-plus/icons-vue'

const router = useRouter()

const searchQuery = ref('')
const contentType = ref<'all' | 'article' | 'project'>('all')
const selectedTag = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const loading = ref(false)
const contentList = ref<any[]>([])
const allTags = ref<string[]>([])
const total = ref(0)
const totalPages = ref(0)

// 加载所有标签
const loadTags = async () => {
  try {
    const response = await publicApi.getTags()
    allTags.value = response.tags
  } catch (error) {
    console.error('Failed to load tags:', error)
  }
}

// 加载内容列表
const loadContent = async () => {
  loading.value = true
  try {
    const response = await publicApi.getAll(
      currentPage.value,
      pageSize.value,
      searchQuery.value,
      selectedTag.value,
      contentType.value
    )
    contentList.value = response.items
    total.value = response.total
    totalPages.value = response.total_pages
  } finally {
    loading.value = false
  }
}

// 搜索处理（使用防抖）
let searchTimer: ReturnType<typeof setTimeout> | null = null
const handleSearch = () => {
  if (searchTimer) clearTimeout(searchTimer)
  searchTimer = setTimeout(() => {
    currentPage.value = 1
    loadContent()
  }, 300)
}

// 标签点击处理
const handleTagClick = (tag: string) => {
  if (selectedTag.value === tag) {
    selectedTag.value = ''
  } else {
    selectedTag.value = tag
  }
  currentPage.value = 1
  loadContent()
}

// 清除标签筛选
const clearTag = () => {
  selectedTag.value = ''
  currentPage.value = 1
  loadContent()
}

// 点击内容卡片
const handleItemClick = (item: any) => {
  if (item.type === 'article') {
    router.push(`/article/${item.id}`)
  } else {
    router.push(`/project/${item.id}`)
  }
}

// 获取显示的标签（作品显示tech_stack，文章显示tags）
const getDisplayTags = (item: any) => {
  if (item.type === 'project') {
    return item.tech_stack || item.tags || []
  }
  return item.tags || []
}

// 格式化日期
const formatDate = (date?: string) => {
  if (!date) return ''
  const d = new Date(date)
  const now = new Date()
  const diff = now.getTime() - d.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) {
    return '今天'
  } else if (days === 1) {
    return '昨天'
  } else if (days < 7) {
    return `${days}天前`
  } else if (days < 30) {
    return `${Math.floor(days / 7)}周前`
  } else if (days < 365) {
    return `${Math.floor(days / 30)}个月前`
  } else {
    return `${Math.floor(days / 365)}年前`
  }
}

onMounted(() => {
  loadTags()
  loadContent()
})
</script>

<style scoped>
.home-page {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.header-left h2 {
  margin: 0;
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.filter-section {
  margin-bottom: var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
}

.search-row {
  margin-bottom: var(--spacing-md);
}

.search-input {
  max-width: 400px;
}

.type-filter {
  margin-bottom: var(--spacing-md);
}

.tag-filter {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
  align-items: center;
}

.tag-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  font-weight: var(--font-weight-medium);
}

.tag-item {
  cursor: pointer;
  transition: all var(--transition-fast);
}

.tag-item:hover {
  transform: translateY(-1px);
}

.clear-tag {
  margin-left: var(--spacing-sm);
}

.content-card {
  margin-bottom: var(--spacing-lg);
  cursor: pointer;
  border-radius: var(--radius-lg);
  border: none;
  box-shadow: var(--shadow-card);
  transition: all var(--transition-normal);
  overflow: hidden;
}

.content-card:hover {
  box-shadow: var(--shadow-hover);
  transform: translateY(-4px);
}

.cover-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.card-content {
  padding: var(--spacing-md);
}

.type-tag {
  margin-bottom: var(--spacing-xs);
}

.title {
  font-size: var(--font-size-base);
  margin: 0 0 var(--spacing-sm) 0;
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.summary {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  margin: 0 0 var(--spacing-sm) 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: var(--line-height-normal);
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: var(--spacing-xs);
  align-items: center;
}

.content-tag {
  margin-right: var(--spacing-xs);
}

.author {
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  margin-left: var(--spacing-sm);
}

.views {
  color: var(--text-muted);
  font-size: var(--font-size-xs);
}

.date {
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  margin-left: var(--spacing-sm);
}

.pagination-section {
  display: flex;
  justify-content: center;
  margin: var(--spacing-xl) 0;
}
</style>