<template>
  <div class="comment-section">
    <el-divider />
    <h3 class="comment-title">评论 ({{ commentStore.comments.length }})</h3>

    <!-- Comment form -->
    <div class="comment-form" v-if="userStore.isLoggedIn">
      <el-input
        v-model="newComment"
        type="textarea"
        :rows="3"
        placeholder="写下你的评论..."
        maxlength="2000"
        show-word-limit
      />
      <el-button type="primary" @click="handleSubmit" :loading="submitting" :disabled="!newComment.trim()">
        发表评论
      </el-button>
    </div>
    <div class="login-tip" v-else>
      <el-text type="info">登录后才能发表评论</el-text>
      <el-button type="primary" size="small" @click="$router.push('/login')">登录</el-button>
    </div>

    <!-- Comment list -->
    <div class="comment-list" v-loading="commentStore.loading">
      <div v-for="comment in commentStore.comments" :key="comment.id" class="comment-item">
        <div class="comment-avatar">
          <el-avatar :size="40">
            {{ comment.author?.username?.charAt(0).toUpperCase() }}
          </el-avatar>
        </div>
        <div class="comment-body">
          <div class="comment-header">
            <span class="username" v-if="comment.author?.id" @click="$router.push(`/user/${comment.author.id}`)">
              {{ comment.author?.username }}
            </span>
            <span class="username" v-else>
              {{ comment.author?.username || '未知用户' }}
            </span>
            <span class="date">{{ formatDate(comment.created_at) }}</span>
          </div>
          <div class="comment-content" v-if="editingId !== comment.id">
            {{ comment.content }}
          </div>
          <div class="comment-edit" v-else>
            <el-input
              v-model="editingContent"
              type="textarea"
              :rows="2"
              maxlength="2000"
              show-word-limit
            />
            <el-button type="primary" size="small" @click="handleEditSave(comment.id)" :loading="editingLoading">
              保存
            </el-button>
            <el-button size="small" @click="editingId = null">取消</el-button>
          </div>
          <div class="comment-actions">
            <el-button link size="small" @click="showReplyForm(comment.id)" v-if="userStore.isLoggedIn">
              回复
            </el-button>
            <el-button link size="small" @click="startEdit(comment)" v-if="userStore.user?.id === comment.user_id && editingId !== comment.id">
              编辑
            </el-button>
            <el-button link size="small" type="danger" @click="handleDelete(comment.id)" v-if="userStore.user?.id === comment.user_id">
              删除
            </el-button>
          </div>

          <!-- Reply form -->
          <div class="reply-form" v-if="replyingTo === comment.id">
            <el-input
              v-model="replyContent"
              type="textarea"
              :rows="2"
              placeholder="写下你的回复..."
              maxlength="2000"
              show-word-limit
            />
            <el-button type="primary" size="small" @click="handleReply(comment.id)" :loading="replyLoading" :disabled="!replyContent.trim()">
              回复
            </el-button>
            <el-button size="small" @click="replyingTo = null">取消</el-button>
          </div>

          <!-- Replies -->
          <div class="replies" v-if="comment.replies && comment.replies.length > 0">
            <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
              <div class="comment-avatar">
                <el-avatar :size="32">
                  {{ reply.author?.username?.charAt(0).toUpperCase() }}
                </el-avatar>
              </div>
              <div class="comment-body">
                <div class="comment-header">
                  <span class="username" v-if="reply.author?.id" @click="$router.push(`/user/${reply.author.id}`)">
                    {{ reply.author?.username }}
                  </span>
                  <span class="username" v-else>
                    {{ reply.author?.username || '未知用户' }}
                  </span>
                  <span class="date">{{ formatDate(reply.created_at) }}</span>
                </div>
                <div class="comment-content" v-if="editingId !== reply.id">
                  {{ reply.content }}
                </div>
                <div class="comment-edit" v-else>
                  <el-input
                    v-model="editingContent"
                    type="textarea"
                    :rows="2"
                    maxlength="2000"
                    show-word-limit
                  />
                  <el-button type="primary" size="small" @click="handleEditSave(reply.id, comment.id)" :loading="editingLoading">
                    保存
                  </el-button>
                  <el-button size="small" @click="editingId = null">取消</el-button>
                </div>
                <div class="comment-actions">
                  <el-button link size="small" @click="startEdit(reply)" v-if="userStore.user?.id === reply.user_id && editingId !== reply.id">
                    编辑
                  </el-button>
                  <el-button link size="small" type="danger" @click="handleDelete(reply.id, comment.id)" v-if="userStore.user?.id === reply.user_id">
                    删除
                  </el-button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <el-empty v-if="!commentStore.loading && commentStore.comments.length === 0" description="暂无评论" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useUserStore } from '@/stores/user'
import { useCommentStore } from '@/stores/comment'
import type { Comment } from '@/types'

const props = defineProps<{
  contentType: 'article' | 'project'
  contentId: number
}>()

const userStore = useUserStore()
const commentStore = useCommentStore()

const newComment = ref('')
const submitting = ref(false)
const replyingTo = ref<number | null>(null)
const replyContent = ref('')
const replyLoading = ref(false)
const editingId = ref<number | null>(null)
const editingContent = ref('')
const editingLoading = ref(false)

const formatDate = (date?: string) => {
  if (!date) return ''
  return new Date(date).toLocaleString('zh-CN')
}

const handleSubmit = async () => {
  if (!newComment.value.trim()) return
  submitting.value = true
  try {
    await commentStore.addComment({
      content_type: props.contentType,
      content_id: props.contentId,
      content: newComment.value.trim()
    })
    newComment.value = ''
    ElMessage.success('评论发表成功')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '发表评论失败')
  } finally {
    submitting.value = false
  }
}

const showReplyForm = (commentId: number) => {
  replyingTo.value = commentId
  replyContent.value = ''
}

const handleReply = async (parentId: number) => {
  if (!replyContent.value.trim()) return
  replyLoading.value = true
  try {
    await commentStore.addComment({
      content_type: props.contentType,
      content_id: props.contentId,
      content: replyContent.value.trim(),
      parent_id: parentId
    })
    replyingTo.value = null
    replyContent.value = ''
    ElMessage.success('回复发表成功')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '发表回复失败')
  } finally {
    replyLoading.value = false
  }
}

const startEdit = (comment: Comment) => {
  editingId.value = comment.id
  editingContent.value = comment.content
}

const handleEditSave = async (commentId: number, parentId?: number) => {
  if (!editingContent.value.trim()) return
  editingLoading.value = true
  try {
    await commentStore.editComment(commentId, { content: editingContent.value.trim() }, parentId)
    editingId.value = null
    editingContent.value = ''
    ElMessage.success('评论修改成功')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '修改评论失败')
  } finally {
    editingLoading.value = false
  }
}

const handleDelete = async (commentId: number, parentId?: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这条评论吗？', '提示', {
      type: 'warning'
    })
    await commentStore.removeComment(commentId, parentId)
    ElMessage.success('评论已删除')
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error(error.response?.data?.detail || '删除评论失败')
    }
  }
}

onMounted(() => {
  commentStore.loadComments(props.contentType, props.contentId)
})

onUnmounted(() => {
  commentStore.clearComments()
})
</script>

<style scoped>
.comment-section {
  margin-top: 20px;
}

.comment-title {
  margin: 20px 0 15px 0;
}

.comment-form {
  margin-bottom: 20px;
}

.comment-form .el-button {
  margin-top: 10px;
}

.login-tip {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.comment-list {
  margin-top: 20px;
}

.comment-item {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.comment-avatar {
  flex-shrink: 0;
}

.comment-body {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.username {
  font-weight: 500;
  cursor: pointer;
}

.username:hover {
  color: var(--el-color-primary);
}

.date {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

.comment-content {
  margin: 8px 0;
  line-height: 1.6;
}

.comment-edit {
  margin: 8px 0;
}

.comment-edit .el-button {
  margin-top: 5px;
  margin-right: 5px;
}

.comment-actions {
  display: flex;
  gap: 5px;
}

.reply-form {
  margin: 10px 0;
  padding-left: 10px;
}

.reply-form .el-button {
  margin-top: 5px;
  margin-right: 5px;
}

.replies {
  margin-top: 15px;
  padding-left: 20px;
  border-left: 2px solid var(--el-border-color-light);
}

.reply-item {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

/* 手机端适配 */
@media (max-width: 767px) {
  .comment-section {
    margin-top: 10px;
  }

  .comment-title {
    margin: 10px 0 10px 0;
    font-size: var(--font-size-base);
  }

  .comment-form {
    margin-bottom: 15px;
  }

  .comment-item {
    gap: 8px;
    margin-bottom: 15px;
  }

  .comment-avatar .el-avatar {
    --el-avatar-size: 32px !important;
  }

  .comment-header {
    flex-wrap: wrap;
    gap: 5px;
  }

  .username {
    font-size: 14px;
  }

  .date {
    font-size: 11px;
  }

  .comment-content {
    margin: 5px 0;
    font-size: 14px;
    line-height: 1.5;
  }

  .comment-actions {
    flex-wrap: wrap;
  }

  .reply-form {
    margin: 8px 0;
    padding-left: 5px;
  }

  .replies {
    margin-top: 10px;
    padding-left: 10px;
  }

  .reply-item {
    gap: 8px;
    margin-bottom: 10px;
  }

  .reply-item .comment-avatar .el-avatar {
    --el-avatar-size: 24px !important;
  }
}
</style>