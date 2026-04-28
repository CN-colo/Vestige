<template>
  <div class="subscription-manage-page">
    <el-card>
      <template #header>
        <h2>管理订阅</h2>
      </template>

      <!-- 添加订阅 -->
      <div class="add-subscription">
        <el-input
          v-model="newTag"
          placeholder="输入标签名称"
          style="width: 200px"
          @keyup.enter="handleSubscribe"
        />
        <el-button type="primary" @click="handleSubscribe" :loading="subscribeLoading">
          订阅
        </el-button>
      </div>

      <!-- 热门标签推荐 -->
      <div class="popular-tags">
        <h3>热门标签</h3>
        <div class="tag-list">
          <el-tag 
            v-for="item in popularTags" 
            :key="item.tag"
            :type="isSubscribed(item.tag) ? 'primary' : 'info'"
            :effect="isSubscribed(item.tag) ? 'dark' : 'plain'"
            class="popular-tag"
            @click="handleToggleSubscribe(item.tag)"
          >
            {{ item.tag }} ({{ item.count }}人订阅)
          </el-tag>
        </div>
      </div>

      <!-- 我的订阅 -->
      <div class="my-subscriptions">
        <h3>我的订阅 ({{ subscriptions.length }})</h3>
        <el-empty v-if="subscriptions.length === 0" description="暂无订阅标签" />
        <div class="tag-list" v-else>
          <el-tag 
            v-for="tag in subscriptions" 
            :key="tag"
            closable
            size="large"
            @close="handleUnsubscribe(tag)"
          >
            {{ tag }}
          </el-tag>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useSubscriptionStore } from '@/stores/subscription'
import { ElMessage } from 'element-plus'

const subscriptionStore = useSubscriptionStore()
const newTag = ref('')
const subscribeLoading = ref(false)

const subscriptions = computed(() => subscriptionStore.subscriptions)
const popularTags = computed(() => subscriptionStore.popularTags)

const isSubscribed = (tag: string) => subscriptionStore.isSubscribed(tag)

onMounted(async () => {
  await subscriptionStore.loadSubscriptions()
  await subscriptionStore.loadPopularTags(30)
})

const handleSubscribe = async () => {
  if (!newTag.value.trim()) {
    ElMessage.warning('请输入标签名称')
    return
  }

  subscribeLoading.value = true
  try {
    await subscriptionStore.subscribeTag(newTag.value)
    ElMessage.success(`已订阅 "${newTag.value}"`)
    newTag.value = ''
  } catch (error: any) {
    ElMessage.error(error.userMessage || error.response?.data?.detail || '订阅失败')
  } finally {
    subscribeLoading.value = false
  }
}

const handleUnsubscribe = async (tag: string) => {
  try {
    await subscriptionStore.unsubscribeTag(tag)
    ElMessage.success(`已取消订阅 "${tag}"`)
  } catch (error: any) {
    ElMessage.error(error.userMessage || error.response?.data?.detail || '操作失败')
  }
}

const handleToggleSubscribe = async (tag: string) => {
  try {
    const newState = await subscriptionStore.toggleSubscription(tag)
    ElMessage.success(newState ? `已订阅 "${tag}"` : `已取消订阅 "${tag}"`)
  } catch (error: any) {
    ElMessage.error(error.userMessage || error.response?.data?.detail || '操作失败')
  }
}
</script>

<style scoped>
.subscription-manage-page {
  max-width: var(--content-max-width-narrow);
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.el-card {
  border-radius: var(--radius-lg);
  border: none;
  box-shadow: var(--shadow-card);
}

.el-card h2 {
  margin: 0;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.add-subscription {
  display: flex;
  gap: var(--spacing-sm);
  margin-bottom: var(--spacing-xl);
}

.popular-tags,
.my-subscriptions {
  margin-top: var(--spacing-lg);
}

.popular-tags h3,
.my-subscriptions h3 {
  margin-bottom: var(--spacing-md);
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  font-weight: var(--font-weight-medium);
}

.tag-list {
  display: flex;
  gap: var(--spacing-sm);
  flex-wrap: wrap;
}

.popular-tag {
  cursor: pointer;
  transition: all var(--transition-fast);
}

.popular-tag:hover {
  transform: translateY(-1px);
}

/* 手机端适配 */
@media (max-width: 767px) {
  .subscription-manage-page {
    padding: var(--spacing-sm);
  }

  .el-card h2 {
    font-size: var(--font-size-lg);
  }

  .add-subscription {
    flex-direction: column;
  }

  .add-subscription .el-input {
    width: 100% !important;
  }

  .popular-tags h3,
  .my-subscriptions h3 {
    font-size: 13px;
  }

  .tag-list {
    gap: var(--spacing-xs);
  }

  .popular-tag {
    font-size: 12px;
  }
}
</style>