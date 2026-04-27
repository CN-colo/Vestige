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
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.el-card {
  border-radius: var(--radius-lg);
  border: none;
  box-shadow: var(--shadow-card);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.page-header h2 {
  margin: 0;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.subscribed-tags {
  margin-bottom: var(--spacing-lg);
}

.subscribed-tags .label {
  color: var(--text-secondary);
  margin-right: var(--spacing-sm);
  font-size: var(--font-size-sm);
}

.subscribed-tags .el-tag {
  margin-right: var(--spacing-xs);
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

.card-cover {
  width: 100%;
  height: 150px;
  object-fit: cover;
  margin-bottom: var(--spacing-sm);
  border-radius: var(--radius-md);
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

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  margin-bottom: var(--spacing-sm);
}

.card-meta .author {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.card-tags {
  display: flex;
  gap: var(--spacing-xs);
  flex-wrap: wrap;
}

/* 手机端适配 */
@media (max-width: 767px) {
  .subscription-feed-page {
    padding: var(--spacing-sm);
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
  }

  .page-header h2 {
    font-size: var(--font-size-lg);
  }

  .subscribed-tags {
    margin-bottom: var(--spacing-md);
  }

  .subscribed-tags .label {
    display: block;
    margin-bottom: var(--spacing-xs);
  }

  .content-card {
    margin-bottom: var(--spacing-sm);
  }

  .card-cover {
    height: 120px;
  }

  .content-card h3 {
    font-size: 15px;
  }

  .content-card p {
    font-size: 13px;
  }

  .card-meta {
    font-size: 11px;
  }

  .card-tags .el-tag {
    font-size: 11px;
  }
}
</style>