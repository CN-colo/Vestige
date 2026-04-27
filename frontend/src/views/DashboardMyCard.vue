<template>
  <div class="my-card-page">
    <el-card class="card-preview" v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>我的名片</span>
          <el-switch
            v-model="cardEnabled"
            active-text="允许分享"
            inactive-text="禁止分享"
            @change="handleCardEnabledChange"
          />
        </div>
      </template>
      
      <!-- 名片预览 -->
      <div class="card-content">
        <div class="card-avatar">
          <el-avatar :size="100" :src="user?.avatar">
            {{ user?.username?.charAt(0).toUpperCase() }}
          </el-avatar>
          <el-upload
            :show-file-list="false"
            :before-upload="beforeAvatarUpload"
            :http-request="handleAvatarUpload"
            class="avatar-upload"
          >
            <el-button size="small" type="primary" link>更换头像</el-button>
          </el-upload>
        </div>
        
        <div class="card-info">
          <h2>{{ user?.username }}</h2>
          <p class="email">{{ user?.email }}</p>
          <div class="bio-section">
            <MdPreview
              v-if="!editingBio && user?.bio"
              :modelValue="user.bio"
              class="bio-preview"
            />
            <p class="bio-placeholder" v-if="!editingBio && !user?.bio">点击编辑个人简介...</p>
            <MdEditor
              v-if="editingBio"
              v-model="bioText"
              language="zh-CN"
              style="height: 200px"
            />
            <div class="bio-actions" v-if="editingBio">
              <el-button size="small" type="primary" @click="saveBio">保存</el-button>
              <el-button size="small" @click="cancelEditBio">取消</el-button>
            </div>
            <el-button
              v-if="!editingBio"
              size="small"
              type="primary"
              link
              @click="startEditBio"
            >
              编辑简介
            </el-button>
          </div>
          
          <div class="contact-section">
            <p class="contact" v-if="!editingContact">{{ user?.contact || '点击编辑联系方式...' }}</p>
            <el-input
              v-else
              v-model="contactText"
              placeholder="手机/微信/QQ等"
              @blur="saveContact"
            />
            <el-button
              v-if="!editingContact"
              size="small"
              type="primary"
              link
              @click="startEditContact"
            >
              编辑联系方式
            </el-button>
          </div>
          
          <div class="stats">
            <div class="stat-item">
              <span class="stat-value">{{ articlesCount }}</span>
              <span class="stat-label">篇文章</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ projectsCount }}</span>
              <span class="stat-label">个作品</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 分享链接 -->
      <div class="share-section" v-if="cardEnabled">
        <el-divider />
        <h3>分享链接</h3>
        <div class="share-link">
          <el-input
            v-model="shareLink"
            readonly
            class="link-input"
          >
            <template #append>
              <el-button @click="copyLink" type="primary">
                复制链接
              </el-button>
            </template>
          </el-input>
        </div>
        <p class="share-tip">复制链接分享给朋友，让他们查看你的名片</p>
      </div>
      
      <div class="share-disabled" v-else>
        <el-divider />
        <el-alert
          type="warning"
          title="名片分享已关闭"
          description="开启分享后，其他人可以通过链接查看你的名片"
          :closable="false"
          show-icon
        />
      </div>
    </el-card>
    
    <!-- 预览按钮 -->
    <el-button
      type="primary"
      class="preview-btn"
      @click="previewCard"
      :disabled="!cardEnabled"
    >
      预览名片
    </el-button>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { MdEditor, MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import 'md-editor-v3/lib/preview.css'
import { useUserStore } from '@/stores/user'
import { authApi } from '@/api/auth'
import { mediaApi } from '@/api/media'
import { publicApi } from '@/api/articles'
import type { User } from '@/types'

const router = useRouter()
const userStore = useUserStore()
const loading = ref(false)
const user = ref<User | null>(null)
const cardEnabled = ref(true)
const editingBio = ref(false)
const editingContact = ref(false)
const bioText = ref('')
const contactText = ref('')
const articlesCount = ref(0)
const projectsCount = ref(0)

const shareLink = computed(() => {
  if (!user.value) return ''
  return `${window.location.origin}/card/${user.value.id}`
})

onMounted(async () => {
  await loadUserInfo()
})

async function loadUserInfo() {
  loading.value = true
  try {
    user.value = await authApi.getMe()
    cardEnabled.value = user.value.card_enabled ?? true
    bioText.value = user.value.bio || ''
    contactText.value = user.value.contact || ''
    
    // 获取文章和作品统计
    const userInfo = await publicApi.getUser(user.value.id)
    articlesCount.value = userInfo.articles_count || 0
    projectsCount.value = userInfo.projects_count || 0
  } catch (error) {
    ElMessage.error('加载用户信息失败')
  } finally {
    loading.value = false
  }
}

async function handleCardEnabledChange(value: boolean) {
  try {
    await authApi.updateMe({ card_enabled: value })
    ElMessage.success(value ? '名片分享已开启' : '名片分享已关闭')
  } catch (error) {
    ElMessage.error('更新失败')
    cardEnabled.value = !value
  }
}

function startEditBio() {
  editingBio.value = true
  bioText.value = user.value?.bio || ''
}

function cancelEditBio() {
  editingBio.value = false
  bioText.value = user.value?.bio || ''
}

async function saveBio() {
  editingBio.value = false
  if (bioText.value === user.value?.bio) return
  
  try {
    const updated = await authApi.updateMe({ bio: bioText.value })
    user.value = updated
    ElMessage.success('简介已更新')
  } catch (error) {
    ElMessage.error('更新简介失败')
  }
}

function startEditContact() {
  editingContact.value = true
  contactText.value = user.value?.contact || ''
}

async function saveContact() {
  editingContact.value = false
  if (contactText.value === user.value?.contact) return
  
  try {
    const updated = await authApi.updateMe({ contact: contactText.value })
    user.value = updated
    ElMessage.success('联系方式已更新')
  } catch (error) {
    ElMessage.error('更新联系方式失败')
  }
}

function beforeAvatarUpload(file: File) {
  const isImage = file.type.startsWith('image/')
  const isLt2M = file.size / 1024 / 1024 < 2
  
  if (!isImage) {
    ElMessage.error('只能上传图片文件')
    return false
  }
  if (!isLt2M) {
    ElMessage.error('图片大小不能超过 2MB')
    return false
  }
  return true
}

async function handleAvatarUpload(options: any) {
  try {
    const result = await mediaApi.upload(options.file)
    const avatarUrl = result.url
    const updated = await authApi.updateMe({ avatar: avatarUrl })
    user.value = updated
    userStore.user = updated
    ElMessage.success('头像已更新')
  } catch (error) {
    ElMessage.error('上传头像失败')
  }
}

function copyLink() {
  navigator.clipboard.writeText(shareLink.value)
  ElMessage.success('链接已复制到剪贴板')
}

function previewCard() {
  router.push(`/card/${user.value?.id}`)
}
</script>

<style scoped>
.my-card-page {
  width: 100%;
}

.card-preview {
  border-radius: var(--radius-lg);
  border: none;
  box-shadow: var(--shadow-card);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.card-content {
  display: flex;
  gap: var(--spacing-xl);
  padding: var(--spacing-lg) 0;
}

.card-avatar {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
}

.card-info {
  flex: 1;
}

.card-info h2 {
  margin: 0 0 var(--spacing-sm) 0;
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
}

.card-info .email {
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-md) 0;
  font-size: var(--font-size-sm);
}

.bio-section {
  margin-bottom: var(--spacing-lg);
}

.bio-section .bio-placeholder {
  color: var(--text-placeholder);
  margin: 0 0 var(--spacing-xs) 0;
  font-size: var(--font-size-sm);
}

.bio-section .bio-preview {
  background: transparent;
}

.bio-actions {
  margin-top: var(--spacing-sm);
}

.contact-section {
  margin-bottom: var(--spacing-lg);
}

.contact-section .contact {
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-xs) 0;
  cursor: pointer;
  font-size: var(--font-size-sm);
}

.stats {
  display: flex;
  gap: var(--spacing-xl);
}

.stat-item {
  display: flex;
  align-items: baseline;
  gap: var(--spacing-xs);
}

.stat-value {
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
  color: var(--primary-color);
}

.stat-label {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.share-section h3 {
  margin: 0 0 var(--spacing-md) 0;
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.share-link {
  margin-bottom: var(--spacing-sm);
}

.share-tip {
  color: var(--text-muted);
  font-size: var(--font-size-xs);
  margin: 0;
}

.share-disabled {
  margin-top: var(--spacing-lg);
}

.preview-btn {
  margin-top: var(--spacing-lg);
  transition: all var(--transition-fast);
}

.preview-btn:hover {
  transform: translateY(-2px);
}
</style>