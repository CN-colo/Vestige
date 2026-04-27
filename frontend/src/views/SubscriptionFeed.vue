<template>
  <div class="subscription-feed-page">
    <el-card>
      <template #header>
        <div class="page-header">
          <h2>订阅推送</h2>
          <el-button @click="$router.push('/subscriptions/manage')">
            管理订阅
          </el-button>
        </div>
      </template>

      <!-- 显示订阅的标签 -->
      <div class="subscribed-tags" v-if="feed?.subscribed_tags?.length">
        <span class="label">已订阅标签：</span>
        <el-tag 
          v-for="tag in feed.subscribed_tags" 
          :key="tag"
          closable
          @close="handleUnsubscribe(tag)"
        >
          {{ tag }}
        </el-tag>
      </div>

      <el-empty v-if="!feed?.subscribed_tags?.length" description="暂无订阅标签，去订阅一些感兴趣的标签吧">
        <el-button type="primary" @click="$router.push('/subscriptions/manage')">
          管理订阅
        </el-button>
      </el-empty>
    </el-card>

    <!-- 推送内容 -->
    <div v-if="feed?.subscribed_tags?.length" v-loading="loading">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="文章" name="articles">
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" v-for="article in feed?.articles" :key="article.id">
              <el-card class="content-card" shadow="hover" @click="$router.push(`/article/${article.id}`)">
                <img v-if="article.cover_image" :src="article.cover_image" class="card-cover" />
                <h3>{{ article.title }}</h3>
                <p>{{ article.summary }}</p>
                <div class="card-meta">
                  <span class="author">
                    <el-avatar :size="20" :src="article.author?.avatar">
                      {{ article.author?.username?.charAt(0) }}
                    </el-avatar>
                    {{ article.author?.username }}
                  </span>
                  <span>{{ article.like_count }} 赞</span>
                </div>
                <div class="card-tags">
                  <el-tag v-for="tag in article.tags" :key="tag" size="small" type="info">{{ tag }}</el-tag>
                </div>
              </el-card>
            </el-col>
          </el-row>
          <el-empty v-if="!feed?.articles?.length" description="暂无相关文章推送" />
        </el-tab-pane>

        <el-tab-pane label="作品" name="projects">
          <el-row :gutter="20">
            <el-col :xs="24" :sm="12" :md="8" v-for="project in feed?.projects" :key="project.id">
              <el-card class="content-card" shadow="hover" @click="$router.push(`/project/${project.id}`)">
                <img v-if="project.cover_image" :src="project.cover_image" class="card-cover" />
                <h3>{{ project.name }}</h3>
                <p>{{ project.description }}</p>
                <div class="card-meta">
                  <span class="author">
                    <el-avatar :size="20" :src="project.author?.avatar">
                      {{ project.author?.username?.charAt(0) }}
                    </el-avatar>
                    {{ project.author?.username }}
                  </span>
                  <span>{{ project.like_count }} 赞</span>
                </div>
                <div class="card-tags">
                  <el-tag v-for="tag in project.tags" :key="tag" size="small" type="info">{{ tag }}</el-tag>
                </div>
              </el-card>
            </el-col>
          </el-row>
          <el-empty v-if="!feed?.projects?.length" description="暂无相关作品推送" />
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSubscriptionStore } from '@/stores/subscription'
import { ElMessage } from 'element-plus'
import type { SubscriptionFeed } from '@/types'

const subscriptionStore = useSubscriptionStore()
const loading = ref(false)
const activeTab = ref('articles')
const feed = ref<SubscriptionFeed | null>(null)

onMounted(async () => {
  loading.value = true
  try {
    await subscriptionStore.loadFeed(1, 20)
    feed.value = subscriptionStore.feed
  } finally {
    loading.value = false
  }
})

const handleUnsubscribe = async (tag: string) => {
  try {
    await subscriptionStore.unsubscribeTag(tag)
    ElMessage.success(`已取消订阅 "${tag}"`)
    // 重新加载推送
    await subscriptionStore.loadFeed(1, 20)
    feed.value = subscriptionStore.feed
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}
</script>

<style scoped>
.subscription-feed-page {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  margin: 0;
}

.subscribed-tags {
  margin-bottom: 20px;
}

.subscribed-tags .label {
  color: var(--el-text-color-secondary);
  margin-right: 10px;
}

.subscribed-tags .el-tag {
  margin-right: 8px;
}

.content-card {
  margin-bottom: 20px;
  cursor: pointer;
}

.card-cover {
  width: 100%;
  height: 150px;
  object-fit: cover;
  margin-bottom: 10px;
}

.content-card h3 {
  margin: 0 0 10px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.content-card p {
  color: var(--el-text-color-secondary);
  margin: 0 0 10px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--el-text-color-secondary);
  font-size: 12px;
  margin-bottom: 10px;
}

.card-meta .author {
  display: flex;
  align-items: center;
  gap: 5px;
}

.card-tags {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}
</style>