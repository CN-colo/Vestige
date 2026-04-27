<template>
  <div class="article-editor">
    <div class="editor-header">
      <h2>{{ isEdit ? '编辑文章' : '新建文章' }}</h2>
      <div class="editor-actions">
        <el-button @click="handleSaveDraft" :loading="saving">
          <el-icon><DocumentChecked /></el-icon>
          <span class="btn-text">保存草稿</span>
        </el-button>
        <el-button type="primary" @click="handlePublish" :loading="publishing">
          <el-icon><Promotion /></el-icon>
          <span class="btn-text">{{ article.is_public ? '更新发布' : '发布' }}</span>
        </el-button>
      </div>
    </div>

    <div class="editor-form">
      <el-form :model="article" label-position="top">
        <el-form-item label="标题">
          <el-input v-model="article.title" placeholder="请输入文章标题" />
        </el-form-item>

        <el-form-item label="摘要">
          <el-input
            v-model="article.summary"
            type="textarea"
            :rows="3"
            placeholder="请输入文章摘要（可选）"
          />
        </el-form-item>

        <el-form-item label="标签（用逗号分隔）">
          <el-input v-model="article.tags" placeholder="例如：技术, Vue, 前端" />
        </el-form-item>

        <el-form-item label="封面图片">
          <div class="cover-upload">
            <el-upload
              :action="uploadUrl"
              :headers="uploadHeaders"
              :show-file-list="false"
              :on-success="handleCoverSuccess"
              :before-upload="beforeCoverUpload"
              accept="image/*"
            >
              <div v-if="article.cover_image" class="cover-preview">
                <img :src="article.cover_image" alt="封面预览" />
                <div class="cover-actions">
                  <el-button size="small" @click.stop="removeCover">移除</el-button>
                </div>
              </div>
              <div v-else class="cover-placeholder">
                <el-icon><Plus /></el-icon>
                <span>上传封面</span>
              </div>
            </el-upload>
          </div>
        </el-form-item>

        <el-form-item label="正文">
          <MdEditor
            v-model="article.content"
            :style="{ height: editorHeight }"
            :preview="true"
            :toolbars="editorToolbars"
            placeholder="请使用 Markdown 格式编写文章内容..."
          />
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { DocumentChecked, Promotion } from '@element-plus/icons-vue'
import { MdEditor, ToolbarNames } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'
import { useArticleStore } from '@/stores/article'
import { useUserStore } from '@/stores/user'
import request from '@/api/request'

const route = useRoute()
const router = useRouter()
const articleStore = useArticleStore()
const userStore = useUserStore()

const isEdit = computed(() => !!route.params.id)
const articleId = computed(() => route.params.id as string)

const article = ref({
  title: '',
  summary: '',
  content: '',
  tags: '',
  cover_image: '',
  is_public: false
})

const saving = ref(false)
const publishing = ref(false)

// 编辑器高度响应式
const editorHeight = ref('500px')

const updateEditorHeight = () => {
  const windowHeight = window.innerHeight
  if (windowHeight < 768) {
    editorHeight.value = '350px'
  } else if (windowHeight < 1024) {
    editorHeight.value = '400px'
  } else {
    editorHeight.value = '500px'
  }
}

onMounted(() => {
  updateEditorHeight()
  window.addEventListener('resize', updateEditorHeight)
  
  if (isEdit.value && articleId.value) {
    loadArticle()
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', updateEditorHeight)
})

// 上传配置
const uploadUrl = computed(() => `${request.defaults.baseURL}/media/upload`)
const uploadHeaders = computed(() => ({
  Authorization: `Bearer ${userStore.token}`
}))

const editorToolbars: ToolbarNames[] = [
  'bold', 'underline', 'italic', '-',
  'title', 'strikeThrough', 'sub', 'sup', 'quote', 'unorderedList', 'orderedList', '-',
  'codeRow', 'code', 'link', 'image', 'table', '-',
  'revoke', 'next', 'save', '=', 'preview', 'fullscreen'
]

const loadArticle = async () => {
  try {
    const data = await articleStore.loadArticle(articleId.value)
    article.value = {
      title: data.title || '',
      summary: data.summary || '',
      content: data.content || '',
      tags: (data.tags || []).join(', '),
      cover_image: data.cover_image || '',
      is_public: data.is_public ?? false
    }
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '加载文章失败')
    router.push('/dashboard/articles')
  }
}

const beforeCoverUpload = (file: File) => {
  const isImage = file.type.startsWith('image/')
  const isLt5M = file.size / 1024 / 1024 < 5

  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
    return false
  }
  if (!isLt5M) {
    ElMessage.error('图片大小不能超过 5MB!')
    return false
  }
  return true
}

const handleCoverSuccess = (response: any) => {
  if (response.url) {
    article.value.cover_image = response.url
    ElMessage.success('封面上传成功')
  }
}

const removeCover = () => {
  article.value.cover_image = ''
}

const handleSaveDraft = async () => {
  if (!article.value.title) {
    ElMessage.warning('请输入文章标题')
    return
  }

  saving.value = true
  try {
    const data = {
      title: article.value.title,
      summary: article.value.summary,
      content: article.value.content,
      tags: article.value.tags.split(',').map(t => t.trim()).filter(Boolean),
      cover_image: article.value.cover_image,
      is_public: false
    }

    if (isEdit.value) {
      await articleStore.updateArticle(articleId.value, data)
    } else {
      await articleStore.createArticle(data)
    }
    ElMessage.success('草稿保存成功')
    router.push('/dashboard/articles')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

const handlePublish = async () => {
  if (!article.value.title) {
    ElMessage.warning('请输入文章标题')
    return
  }
  if (!article.value.content) {
    ElMessage.warning('请输入文章内容')
    return
  }

  publishing.value = true
  try {
    const data = {
      title: article.value.title,
      summary: article.value.summary,
      content: article.value.content,
      tags: article.value.tags.split(',').map(t => t.trim()).filter(Boolean),
      cover_image: article.value.cover_image,
      is_public: true
    }

    if (isEdit.value) {
      await articleStore.updateArticle(articleId.value, data)
    } else {
      await articleStore.createArticle(data)
    }
    ElMessage.success('发布成功')
    router.push('/dashboard/articles')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '发布失败')
  } finally {
    publishing.value = false
  }
}
</script>

<style scoped>
.article-editor {
  background: var(--bg-card);
  padding: var(--spacing-lg);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-light);
}

.editor-header h2 {
  margin: 0;
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.editor-actions {
  display: flex;
  gap: var(--spacing-sm);
}

.editor-form {
  max-width: 100%;
}

.cover-upload {
  width: 100%;
}

.cover-preview {
  position: relative;
  width: 100%;
  max-width: 300px;
  border-radius: var(--radius-md);
  overflow: hidden;
}

.cover-preview img {
  width: 100%;
  display: block;
}

.cover-actions {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: var(--spacing-xs);
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
}

.cover-placeholder {
  width: 100%;
  max-width: 300px;
  height: 150px;
  border: 2px dashed var(--border-color);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: var(--text-muted);
  cursor: pointer;
  transition: border-color var(--transition-fast);
}

.cover-placeholder:hover {
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.cover-placeholder .el-icon {
  font-size: 24px;
  margin-bottom: var(--spacing-xs);
}

/* 手机端适配 */
@media (max-width: 767px) {
  .article-editor {
    padding: var(--spacing-sm);
  }

  .editor-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-md);
    padding-bottom: var(--spacing-sm);
  }

  .editor-header h2 {
    font-size: var(--font-size-lg);
  }

  .editor-actions {
    width: 100%;
    justify-content: flex-end;
  }

  .btn-text {
    display: none;
  }

  .cover-preview,
  .cover-placeholder {
    max-width: 100%;
  }

  .cover-placeholder {
    height: 120px;
  }

  :deep(.md-editor) {
    font-size: 14px;
  }
}

/* 平板适配 */
@media (min-width: 768px) and (max-width: 1023px) {
  .article-editor {
    padding: var(--spacing-md);
  }
}
</style>