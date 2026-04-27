<template>
  <div class="dashboard-favorites">
    <div class="page-header">
      <h2>我的收藏</h2>
      <el-radio-group v-model="filterType" @change="handleFilterChange">
        <el-radio-button label="">全部</el-radio-button>
        <el-radio-button label="article">文章</el-radio-button>
        <el-radio-button label="project">作品</el-radio-button>
      </el-radio-group>
    </div>

    <div v-loading="loading" class="favorites-list">
      <el-empty v-if="favorites.length === 0" description="暂无收藏" />
      
      <div v-for="favorite in favorites" :key="favorite.id" class="favorite-item">
        <div class="favorite-content" @click="navigateTo(favorite)">
          <img 
            v-if="favorite.item?.cover_image" 
            :src="favorite.item?.cover_image" 
            class="cover-image"
          />
          <div class="favorite-info">
            <div class="favorite-type">
              <el-tag size="small" :type="favorite.target_type === 'article' ? '' : 'success'">
                {{ favorite.target_type === 'article' ? '文章' : '作品' }}
              </el-tag>
            </div>
            <h3 class="favorite-title">
              {{ favorite.target_type === 'article' ? favorite.item?.title : favorite.item?.name }}
            </h3>
            <p class="favorite-desc" v-if="favorite.item?.summary || favorite.item?.description">
              {{ favorite.target_type === 'article' ? favorite.item?.summary : favorite.item?.description }}
            </p>
            <div class="favorite-meta">
              <span class="author">
                <el-avatar :size="16">
                  {{ favorite.item?.author?.username?.charAt(0).toUpperCase() }}
                </el-avatar>
                {{ favorite.item?.author?.username }}
              </span>
              <span class="views">{{ favorite.item?.view_count }} 次查看</span>
              <span class="date">{{ formatDate(favorite.created_at) }} 收藏</span>
            </div>
          </div>
        </div>
        <el-button 
          type="danger" 
          size="small" 
          :icon="StarFilled"
          @click="handleRemove(favorite)"
        >
          取消收藏
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { StarFilled } from '@element-plus/icons-vue'
import { useFavoriteStore } from '@/stores/favorite'
import type { FavoriteWithItem } from '@/types'

const router = useRouter()
const favoriteStore = useFavoriteStore()

const favorites = computed(() => favoriteStore.favorites)
const loading = computed(() => favoriteStore.loading)
const filterType = ref<'article' | 'project' | ''>('')

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

const handleFilterChange = () => {
  favoriteStore.loadFavorites(filterType.value || undefined)
}

const navigateTo = (favorite: FavoriteWithItem) => {
  if (favorite.target_type === 'article') {
    router.push(`/article/${favorite.target_id}`)
  } else {
    router.push(`/project/${favorite.target_id}`)
  }
}

const handleRemove = async (favorite: FavoriteWithItem) => {
  try {
    await ElMessageBox.confirm('确定要取消收藏吗？', '取消收藏', {
      type: 'warning'
    })
    await favoriteStore.removeFavorite(favorite.target_type, favorite.target_id)
    ElMessage.success('已取消收藏')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '操作失败')
    }
  }
}

onMounted(() => {
  favoriteStore.loadFavorites()
})
</script>

<style scoped>
.dashboard-favorites {
  background: var(--bg-card);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-light);
}

.page-header h2 {
  margin: 0;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.favorites-list {
  min-height: 200px;
}

.favorite-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-sm);
  transition: all var(--transition-fast);
  background: var(--bg-card);
}

.favorite-item:hover {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-sm);
  transform: translateY(-2px);
}

.favorite-content {
  display: flex;
  gap: var(--spacing-md);
  flex: 1;
  cursor: pointer;
}

.cover-image {
  width: 100px;
  height: 80px;
  object-fit: cover;
  border-radius: var(--radius-md);
}

.favorite-info {
  flex: 1;
}

.favorite-type {
  margin-bottom: var(--spacing-xs);
}

.favorite-title {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

.favorite-desc {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.favorite-meta {
  display: flex;
  align-items: center;
  gap: var(--spacing-md);
  font-size: var(--font-size-xs);
  color: var(--text-muted);
}

.author {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

/* 手机端适配 */
@media (max-width: 767px) {
  .dashboard-favorites {
    padding: var(--spacing-sm);
  }

  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-md);
    padding-bottom: var(--spacing-sm);
  }

  .page-header h2 {
    font-size: var(--font-size-lg);
  }

  .favorite-item {
    flex-direction: column;
    gap: var(--spacing-sm);
    padding: var(--spacing-sm);
  }

  .favorite-content {
    flex-direction: column;
    gap: var(--spacing-sm);
  }

  .cover-image {
    width: 100%;
    height: 120px;
  }

  .favorite-title {
    font-size: 15px;
  }

  .favorite-desc {
    font-size: 13px;
  }

  .favorite-meta {
    flex-wrap: wrap;
    gap: var(--spacing-sm);
    font-size: 11px;
  }
}
</style>