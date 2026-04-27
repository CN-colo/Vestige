<template>
  <div class="api-keys-page">
    <div class="page-header">
      <h2>API Keys 管理</h2>
      <el-button type="primary" @click="showCreateDialog">
        <el-icon><Plus /></el-icon>
        创建 Key
      </el-button>
    </div>

    <el-alert type="info" :closable="false" style="margin-bottom: 20px">
      API Keys 允许外部应用（如 AI）访问您的公开域数据。请妥善保管您的 Key。
    </el-alert>

    <el-table :data="keys" v-loading="loading" stripe>
      <el-table-column prop="name" label="名称" min-width="150" />
      <el-table-column prop="permissions" label="权限" min-width="150">
        <template #default="{ row }">
          <el-tag v-for="perm in row.permissions" :key="perm" size="small">
            {{ perm }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'">
            {{ row.is_active ? '活跃' : '已禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="last_used_at" label="最后使用" width="180">
        <template #default="{ row }">
          {{ row.last_used_at ? formatDate(row.last_used_at) : '从未使用' }}
        </template>
      </el-table-column>
      <el-table-column prop="expires_at" label="过期时间" width="180">
        <template #default="{ row }">
          {{ row.expires_at ? formatDate(row.expires_at) : '永不过期' }}
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="handleToggleActive(row)">
            {{ row.is_active ? '禁用' : '启用' }}
          </el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- Create Dialog -->
    <el-dialog v-model="createDialogVisible" title="创建 API Key" width="400px">
      <el-form ref="createFormRef" :model="createForm" label-position="top">
        <el-form-item label="名称">
          <el-input v-model="createForm.name" placeholder="如：My AI Assistant" />
        </el-form-item>

        <el-form-item label="权限">
          <el-checkbox-group v-model="createForm.permissions">
            <el-checkbox label="read:public">读取公开域</el-checkbox>
            <el-checkbox label="write:public">写入公开域</el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item label="过期时间">
          <el-date-picker
            v-model="createForm.expires_at"
            type="datetime"
            placeholder="可选，不设置则永不过期"
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleCreate" :loading="creating">创建</el-button>
      </template>
    </el-dialog>

    <!-- Show Key Dialog -->
    <el-dialog v-model="showKeyDialogVisible" title="API Key 已创建" width="500px">
      <el-alert type="warning" :closable="false" style="margin-bottom: 20px">
        请立即保存此 Key，关闭后将无法再次查看完整 Key！
      </el-alert>

      <el-input v-model="newKey" readonly>
        <template #append>
          <el-button @click="copyKey">复制</el-button>
        </template>
      </el-input>

      <template #footer>
        <el-button type="primary" @click="showKeyDialogVisible = false">我已保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { apiKeyApi } from '@/api/keys'
import type { ApiKey } from '@/types'

const keys = ref<ApiKey[]>([])
const loading = ref(false)
const creating = ref(false)
const createDialogVisible = ref(false)
const showKeyDialogVisible = ref(false)
const newKey = ref('')

const createForm = ref({
  name: '',
  permissions: ['read:public'] as string[],
  expires_at: null as Date | null
})

const formatDate = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

const loadKeys = async () => {
  loading.value = true
  try {
    keys.value = await apiKeyApi.getList()
  } finally {
    loading.value = false
  }
}

const showCreateDialog = () => {
  createForm.value = {
    name: '',
    permissions: ['read:public'],
    expires_at: null
  }
  createDialogVisible.value = true
}

const handleCreate = async () => {
  creating.value = true
  try {
    const result = await apiKeyApi.create({
      name: createForm.value.name,
      permissions: createForm.value.permissions,
      expires_at: createForm.value.expires_at?.toISOString()
    })
    newKey.value = result.key
    createDialogVisible.value = false
    showKeyDialogVisible.value = true
    loadKeys()
    ElMessage.success('API Key 创建成功')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '创建失败')
  } finally {
    creating.value = false
  }
}

const copyKey = () => {
  navigator.clipboard.writeText(newKey.value)
  ElMessage.success('已复制到剪贴板')
}

const handleToggleActive = async (key: ApiKey) => {
  try {
    await apiKeyApi.update(key.id, { is_active: !key.is_active })
    ElMessage.success(key.is_active ? '已禁用' : '已启用')
    loadKeys()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '操作失败')
  }
}

const handleDelete = async (key: ApiKey) => {
  try {
    await ElMessageBox.confirm('确定要删除此 API Key 吗？', '删除确认', { type: 'warning' })
    await apiKeyApi.delete(key.id)
    ElMessage.success('删除成功')
    loadKeys()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }
}

onMounted(() => {
  loadKeys()
})
</script>

<style scoped>
.api-keys-page {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}
</style>