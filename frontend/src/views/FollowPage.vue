<template>
  <div class="follow-page">
    <el-tabs v-model="activeTab">
      <el-tab-pane label="我的关注" name="following">
        <el-row :gutter="20" v-loading="loading">
          <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="user in following" :key="user.id">
            <el-card class="user-card" shadow="hover" @click="$router.push(`/user/${user.id}`)">
              <el-avatar :size="50" :src="user.avatar">
                {{ user.username?.charAt(0).toUpperCase() }}
              </el-avatar>
              <div class="user-name">{{ user.username }}</div>
              <div class="user-bio">{{ user.bio || '这个人很懒，什么都没写...' }}</div>
              <div class="user-stats">
                <span>{{ user.following_count }} 关注</span>
                <span>{{ user.followers_count }} 粉丝</span>
              </div>
              <div class="user-action">
                <el-button 
                  size="small"
                  :type="user.is_following ? 'default' : 'primary'"
                  @click.stop="handleToggleFollow(user)"
                  :loading="user.loading"
                >
                  {{ user.is_following ? '已关注' : '关注' }}
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-empty v-if="following.length === 0" description="暂无关注用户" />
      </el-tab-pane>

      <el-tab-pane label="我的粉丝" name="followers">
        <el-row :gutter="20" v-loading="loading">
          <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="user in followers" :key="user.id">
            <el-card class="user-card" shadow="hover" @click="$router.push(`/user/${user.id}`)">
              <el-avatar :size="50" :src="user.avatar">
                {{ user.username?.charAt(0).toUpperCase() }}
              </el-avatar>
              <div class="user-name">{{ user.username }}</div>
              <div class="user-bio">{{ user.bio || '这个人很懒，什么都没写...' }}</div>
              <div class="user-stats">
                <span>{{ user.following_count }} 关注</span>
                <span>{{ user.followers_count }} 粉丝</span>
              </div>
              <div class="user-action">
                <el-button 
                  size="small"
                  :type="user.is_following ? 'default' : 'primary'"
                  @click.stop="handleToggleFollow(user)"
                  :loading="user.loading"
                >
                  {{ user.is_following ? '已关注' : '关注' }}
                </el-button>
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-empty v-if="followers.length === 0" description="暂无粉丝" />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useFollowStore } from '@/stores/follow'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import type { UserWithFollowStatus } from '@/types'

interface UserWithLoading extends UserWithFollowStatus {
  loading?: boolean
}

const followStore = useFollowStore()
const userStore = useUserStore()
const loading = ref(false)
const activeTab = ref('following')
const following = ref<UserWithLoading[]>([])
const followers = ref<UserWithLoading[]>([])

// 加载列表
const loadData = async () => {
  loading.value = true
  try {
    if (activeTab.value === 'following') {
    await followStore.loadFollowing()
    following.value = followStore.following.map(u => ({ ...u, loading: false }))
    } else {
      await followStore.loadFollowers()
      followers.value = followStore.followers.map(u => ({ ...u, loading: false }))
    }
  } finally {
    loading.value = false
  }
}

// 切换关注状态
const handleToggleFollow = async (user: UserWithLoading) => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    return
  }

  if (user.id === userStore.user?.id) {
    ElMessage.warning('不能关注自己')
    return
  }

  user.loading = true
  try {
    const newState = await followStore.toggleFollow(user.id)
    user.is_following = newState
    user.followers_count = newState ? user.followers_count + 1 : user.followers_count - 1
    ElMessage.success(newState ? '关注成功' : '已取消关注')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  } finally {
    user.loading = false
  }
}

// 监听 tab 变化
watch(activeTab, () => {
  loadData()
})

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.follow-page {
  max-width: var(--content-max-width);
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.user-card {
  text-align: center;
  padding: var(--spacing-lg);
  cursor: pointer;
  border-radius: var(--radius-lg);
  border: none;
  box-shadow: var(--shadow-card);
  transition: all var(--transition-normal);
}

.user-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
}

.user-card .el-avatar {
  margin-bottom: var(--spacing-sm);
}

.user-name {
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  margin-bottom: var(--spacing-xs);
  color: var(--text-primary);
}

.user-bio {
  color: var(--text-secondary);
  font-size: var(--font-size-xs);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: var(--spacing-sm);
}

.user-stats {
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  margin-bottom: var(--spacing-sm);
}

.user-stats span {
  margin: 0 var(--spacing-xs);
}

.user-action {
  margin-top: var(--spacing-sm);
}
</style>