<template>
  <div class="settings-page">
    <div class="page-header">
      <h2>个人设置</h2>
    </div>

    <el-tabs v-model="activeTab">
      <el-tab-pane label="基本信息" name="profile">
        <el-form ref="profileFormRef" :model="profileForm" :rules="profileRules" label-position="top">
          <el-form-item label="用户名">
            <el-input v-model="profileForm.username" />
          </el-form-item>

          <el-form-item label="邮箱">
            <el-input v-model="profileForm.email" />
          </el-form-item>

          <el-form-item label="头像">
            <el-upload
              class="avatar-uploader"
              :show-file-list="false"
              :before-upload="beforeAvatarUpload"
              :http-request="handleAvatarUpload"
            >
              <img v-if="profileForm.avatar" :src="profileForm.avatar" class="avatar-preview" />
              <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
            </el-upload>
          </el-form-item>

          <el-form-item label="个人简介">
            <MdEditor
              v-model="profileForm.bio"
              language="zh-CN"
              style="height: 300px"
              :previewOnly="false"
            />
          </el-form-item>

          <el-form-item label="联系方式">
            <el-input v-model="profileForm.contact" placeholder="手机/微信/QQ等（可选）" />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="handleUpdateProfile" :loading="saving">
              保存修改
            </el-button>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <el-tab-pane label="账号信息" name="account">
        <el-descriptions :column="1" border>
          <el-descriptions-item label="用户 ID">{{ user?.id }}</el-descriptions-item>
          <el-descriptions-item label="注册时间">{{ formatDate(user?.created_at) }}</el-descriptions-item>
          <el-descriptions-item label="账号状态">
            <el-tag :type="user?.is_active ? 'success' : 'danger'">
              {{ user?.is_active ? '正常' : '已禁用' }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { useUserStore } from '@/stores/user'
import { mediaApi } from '@/api/media'

const userStore = useUserStore()
const user = computed(() => userStore.user)

const activeTab = ref('profile')
const profileFormRef = ref<FormInstance>()
const saving = ref(false)

const profileForm = ref({
  username: '',
  email: '',
  avatar: '',
  bio: '',
  contact: ''
})

const profileRules: FormRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度在 3-50 个字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ]
}

const formatDate = (date?: string) => {
  if (!date) return ''
  return new Date(date).toLocaleString('zh-CN')
}

const beforeAvatarUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt10M = file.size / 1024 / 1024 < 10

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt10M) {
    ElMessage.error('图片大小不能超过 10MB!')
    return false
  }
  return true
}

const handleAvatarUpload = async (options: any) => {
  try {
    const media = await mediaApi.upload(options.file)
    profileForm.value.avatar = `/uploads/${media.filename}`
    ElMessage.success('头像上传成功')
  } catch (error: any) {
    ElMessage.error(error.userMessage || error.response?.data?.detail || '上传失败')
  }
}

const handleUpdateProfile = async () => {
  if (!profileFormRef.value) return

  await profileFormRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      try {
        await userStore.updateUser(profileForm.value)
        ElMessage.success('修改成功')
      } catch (error: any) {
        ElMessage.error(error.userMessage || error.response?.data?.detail || '修改失败')
      } finally {
        saving.value = false
      }
    }
  })
}

onMounted(() => {
  if (user.value) {
    profileForm.value = {
      username: user.value.username,
      email: user.value.email,
      avatar: user.value.avatar || '',
      bio: user.value.bio || '',
      contact: user.value.contact || ''
    }
  }
})
</script>

<style scoped>
.settings-page {
  background: var(--bg-card);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  max-width: var(--content-max-width-small);
}

.page-header {
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

.avatar-uploader .el-upload {
  width: 100px;
  height: 100px;
  border: 2px dashed var(--border-base);
  border-radius: 50%;
  cursor: pointer;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all var(--transition-fast);
  background: var(--gray-50);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--primary-color);
  background: var(--primary-lighter);
}

.avatar-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-uploader-icon {
  font-size: var(--font-size-2xl);
  color: var(--text-placeholder);
  transition: color var(--transition-fast);
}

.avatar-uploader .el-upload:hover .avatar-uploader-icon {
  color: var(--primary-color);
}

/* 手机端适配 */
@media (max-width: 767px) {
  .settings-page {
    padding: var(--spacing-sm);
    max-width: 100%;
  }

  .page-header {
    margin-bottom: var(--spacing-md);
    padding-bottom: var(--spacing-sm);
  }

  .page-header h2 {
    font-size: var(--font-size-lg);
  }

  .avatar-uploader .el-upload {
    width: 80px;
    height: 80px;
  }

  .avatar-uploader-icon {
    font-size: var(--font-size-xl);
  }

  :deep(.md-editor) {
    height: 200px !important;
    font-size: 14px;
  }
}
</style>