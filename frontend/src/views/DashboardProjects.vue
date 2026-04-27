<template>
  <div class="dashboard-projects">
    <div class="page-header">
      <h2>作品管理</h2>
      <el-button type="primary" @click="$router.push('/dashboard/projects/new')">
        <el-icon><Plus /></el-icon>
        新建作品
      </el-button>
    </div>

    <el-table :data="projects" v-loading="loading" stripe>
      <el-table-column prop="name" label="名称" min-width="150" />
      <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
      <el-table-column prop="url" label="地址" min-width="150" show-overflow-tooltip />
      <el-table-column prop="is_public" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_public ? 'success' : 'info'">
            {{ row.is_public ? '已发布' : '私有' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="view_count" label="查看量" width="100" />
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
</style>