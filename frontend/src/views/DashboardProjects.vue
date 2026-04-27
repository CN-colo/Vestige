<template>
  <div class="dashboard-projects">
    <div class="page-header">
      <h2>作品管理</h2>
      <el-button type="primary" @click="$router.push('/dashboard/projects/new')">
        <el-icon><Plus /></el-icon>
        <span class="btn-text">新建作品</span>
      </el-button>
    </div>

    <!-- 桌面端表格 -->
    <el-table :data="projects" v-loading="loading" stripe class="desktop-table" table-layout="fixed">
      <el-table-column prop="name" label="名称" min-width="180" />
      <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
      <el-table-column prop="is_public" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_public ? 'success' : 'info'">
            {{ row.is_public ? '已发布' : '私有' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="view_count" label="阅读量" width="100" />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="260" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="$router.push(`/dashboard/projects/${row.id}`)">
            编辑
          </el-button>
          <el-button size="small" @click="$router.push(`/project/${row.id}`)">
            预览
          </el-button>
          <el-button
            size="small"
            :type="row.is_public ? 'warning' : 'success'"
            @click="handlePublish(row)"
          >
            {{ row.is_public ? '取消发布' : '发布' }}
          </el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 移动端卡片列表 -->
    <div class="mobile-card-list" v-loading="loading">
      <div v-for="project in projects" :key="project.id" class="project-card">
        <div class="card-header">
          <el-tag :type="project.is_public ? 'success' : 'info'" size="small">
            {{ project.is_public ? '已发布' : '私有' }}
          </el-tag>
          <span class="view-count">{{ project.view_count }} 阅读</span>
        </div>
        <h3 class="card-title">{{ project.name }}</h3>
        <p class="card-description" v-if="project.description">{{ project.description }}</p>
        <div class="card-meta">
          <span>{{ formatDate(project.created_at) }}</span>
        </div>
        <div class="card-actions">
          <el-button size="small" @click="$router.push(`/dashboard/projects/${project.id}`)">
            编辑
          </el-button>
          <el-button size="small" @click="$router.push(`/project/${project.id}`)">
            预览
          </el-button>
          <el-button
            size="small"
            :type="project.is_public ? 'warning' : 'success'"
            @click="handlePublish(project)"
          >
            {{ project.is_public ? '取消发布' : '发布' }}
          </el-button>
          <el-button size="small" type="danger" @click="handleDelete(project)">
            删除
          </el-button>
        </div>
      </div>
      <el-empty v-if="!loading && projects.length === 0" description="暂无作品" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useProjectStore } from '@/stores/project'

const projectStore = useProjectStore()

const projects = computed(() => projectStore.projects)
const loading = computed(() => projectStore.loading)

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

const handlePublish = async (project: any) => {
  try {
    if (project.is_public) {
      await projectStore.unpublishProject(project.id)
      ElMessage.success('已取消发布')
    } else {
      await projectStore.publishProject(project.id)
      ElMessage.success('已发布到公开域')
    }
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

const handleDelete = async (project: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这个作品吗？', '删除确认', {
      type: 'warning'
    })
    await projectStore.deleteProject(project.id)
    ElMessage.success('删除成功')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

onMounted(() => {
  projectStore.loadProjects()
})
</script>

<style scoped>
.dashboard-projects {
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

/* 移动端卡片列表默认隐藏 */
.mobile-card-list {
  display: none;
}

.project-card {
  padding: var(--spacing-md);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  margin-bottom: var(--spacing-sm);
  background: var(--bg-card);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-xs);
}

.view-count {
  color: var(--text-muted);
  font-size: var(--font-size-xs);
}

.card-title {
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-description {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  margin: 0 0 var(--spacing-xs) 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.card-meta {
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  margin-bottom: var(--spacing-sm);
}

.card-actions {
  display: flex;
  gap: var(--spacing-xs);
  flex-wrap: wrap;
}

/* 手机端适配 */
@media (max-width: 767px) {
  .dashboard-projects {
    padding: var(--spacing-sm);
  }

  .page-header {
    margin-bottom: var(--spacing-md);
    padding-bottom: var(--spacing-sm);
  }

  .page-header h2 {
    font-size: var(--font-size-lg);
  }

  .btn-text {
    display: none;
  }

  /* 隐藏表格，显示卡片 */
  .desktop-table {
    display: none;
  }

  .mobile-card-list {
    display: block;
  }
}
</style>