<template>
  <div class="project-editor">
    <div class="editor-header">
      <h2>{{ isEdit ? '编辑作品' : '新建作品' }}</h2>
      <div class="actions">
        <el-button @click="handleSave" :loading="saving">保存</el-button>
        <el-button type="primary" @click="handleSaveAndPublish" :loading="saving">
          保存并发布
        </el-button>
      </div>
    </div>

    <el-form ref="formRef" :model="form" :rules="rules" label-position="top">
      <el-form-item label="项目名称" prop="name">
        <el-input v-model="form.name" placeholder="请输入项目名称" />
      </el-form-item>

      <el-form-item label="项目描述" prop="description">
        <MdEditor
          v-model="form.description"
          language="zh-CN"
          style="height: 300px"
          :onUploadImg="handleEditorImageUpload"
        />
      </el-form-item>

      <el-form-item label="项目地址">
        <el-input v-model="form.url" placeholder="请输入项目地址 URL" />
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

      <el-form-item label="标签">
        <el-select v-model="form.tags" multiple filterable allow-create placeholder="请输入标签">
          <el-option v-for="tag in form.tags" :key="tag" :label="tag" :value="tag" />
        </el-select>
      </el-form-item>

      <el-form-item label="技术栈">
        <el-select v-model="form.tech_stack" multiple filterable allow-create placeholder="请输入技术栈">
          <el-option v-for="tech in form.tech_stack" :key="tech" :label="tech" :value="tech" />
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
import { useProjectStore } from '@/stores/project'
import { mediaApi } from '@/api/media'
import { MdEditor } from 'md-editor-v3'
import 'md-editor-v3/lib/style.css'

const router = useRouter()
const route = useRoute()
const projectStore = useProjectStore()

const formRef = ref<FormInstance>()
const saving = ref(false)
const isEdit = ref(false)

const form = ref({
  name: '',
  description: '',
  url: '',
  cover_image: '',
  tags: [] as string[],
  tech_stack: [] as string[]
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入项目描述', trigger: 'blur' }]
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
          await projectStore.updateProject(Number(route.params.id), form.value)
        } else {
          await projectStore.createProject(form.value)
        }
        ElMessage.success('保存成功')
        router.push('/dashboard/projects')
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
        let project: any
        if (isEdit.value) {
          project = await projectStore.updateProject(Number(route.params.id), form.value)
        } else {
          project = await projectStore.createProject(form.value)
        }
        await projectStore.publishProject(project.id)
        ElMessage.success('保存并发布成功')
        router.push('/dashboard/projects')
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
    await projectStore.loadProject(Number(route.params.id))
    if (projectStore.currentProject) {
      form.value = {
        name: projectStore.currentProject.name,
        description: projectStore.currentProject.description,
        url: projectStore.currentProject.url || '',
        cover_image: projectStore.currentProject.cover_image || '',
        tags: projectStore.currentProject.tags || [],
        tech_stack: projectStore.currentProject.tech_stack || []
      }
    }
  }
})
</script>

<style scoped>
.project-editor {
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