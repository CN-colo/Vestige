<template>
  <div class="article-editor">
    <div class="editor-header">
      <h2>{{ isEdit ? '编辑文章' : '新建文章' }}</h2>
      <div class="actions">
        <el-button @click="handleSave" :loading="saving">保存</el-button>
        <el-button type="primary" @click="handleSaveAndPublish" :loading="saving">
          保存并发布
        </el-button>
      </div>
    </div>

    <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
      <el-form-item label="标题" prop="title">
        <el-input v-model="form.title" placeholder="请输入文章标题" />
      </el-form-item>

      <el-form-item label="摘要" prop="summary">
        <el-input v-model="form.summary" type="textarea" :rows="2" placeholder="请输入文章摘要" />
      </el-form-item>

      <el-form-item label="封面图片">
        <el-upload
          class="cover-uploader"
          :show-file-list="false"
          :before-upload="beforeCoverUpload"
          :http-request="handleCoverUpload"
        >
          <img v-if="form.cover_image" :src="form.cover_image" class="cover-preview" />
          <el-icon v-else class="cover-uploader-icon"><Plus /></el-icon>
        </el-upload>
      </el-form-item>

      <el-form-item label="内容" prop="content">
        <MdEditor
          v-model="form.content"
          language="zh-CN"
          style="height: 400px"
          :onUploadImg="handleEditorImageUpload"
        />
      </el-form-item>

      <el-form-item label="标签">
        <el-select v-model="form.tags" multiple filterable allow-create placeholder="请输入标签">
          <el-option v-for="tag in form.tags" :key="tag" :label="tag" :value="tag" />
        </el-select>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useArticleStore } from '@/stores/article'
import { mediaApi } from '@/api/media'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

const router = useRouter()
const route = useRoute()
const articleStore = useArticleStore()

const formRef = ref<FormInstance>()
const saving = ref(false)
const isEdit = ref(false)

const form = ref({
  title: '',
  content: '',
  cover_image: '',
  summary: '',
  tags: [] as string[]
})

const rules: FormRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const beforeCoverUpload = (file: File) => {
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

const handleCoverUpload = async (options: any) => {
  try {
    const media = await mediaApi.upload(options.file)
    form.value.cover_image = `/uploads/${media.filename}`
    ElMessage.success('图片上传成功')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '上传失败')
  }
}

// Handle image upload in markdown editor
const handleEditorImageUpload = async (files: File[], callback: (urls: string[]) => void) => {
  try {
    const urls: string[] = []
    for (const file of files) {
      const media = await mediaApi.upload(file)
      urls.push(`/uploads/${media.filename}`)
    }
    callback(urls)
    ElMessage.success('图片上传成功')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '上传失败')
  }
}

const handleSave = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      try {
        if (isEdit.value) {
          await articleStore.updateArticle(Number(route.params.id), form.value)
        } else {
          await articleStore.createArticle(form.value)
        }
        ElMessage.success('保存成功')
        router.push('/dashboard/articles')
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '保存失败')
      } finally {
        saving.value = false
      }
    }
  })
}

const handleSaveAndPublish = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (valid) {
      saving.value = true
      try {
        let article: any
        if (isEdit.value) {
          article = await articleStore.updateArticle(Number(route.params.id), form.value)
        } else {
          article = await articleStore.createArticle(form.value)
        }
        await articleStore.publishArticle(article.id)
        ElMessage.success('保存并发布成功')
        router.push('/dashboard/articles')
      } catch (error: any) {
        ElMessage.error(error.response?.data?.detail || '操作失败')
      } finally {
        saving.value = false
      }
    }
  })
}

onMounted(async () => {
  if (route.params.id) {
    isEdit.value = true
    await articleStore.loadArticle(Number(route.params.id))
    if (articleStore.currentArticle) {
      form.value = {
        title: articleStore.currentArticle.title,
        content: articleStore.currentArticle.content,
        cover_image: articleStore.currentArticle.cover_image || '',
        summary: articleStore.currentArticle.summary || '',
        tags: articleStore.currentArticle.tags || []
      }
    }
  }
})
</script>

<style scoped>
.article-editor {
  background: #fff;
  padding: 20px;
  border-radius: 8px;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.editor-header h2 {
  margin: 0;
}

.actions {
  display: flex;
  gap: 10px;
}

.cover-uploader {
  width: 200px;
  height: 150px;
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  overflow: hidden;
}

.cover-uploader:hover {
  border-color: var(--el-color-primary);
}

.cover-preview {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cover-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>