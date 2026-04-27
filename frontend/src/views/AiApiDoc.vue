<template>
  <div class="api-doc-page">
    <div class="doc-header">
      <h1>AI API 接口文档</h1>
      <p>通过API Key程序化管理Vestige平台内容</p>
    </div>
    <div class="doc-content">
      <MdPreview :modelValue="docContent" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { MdPreview } from 'md-editor-v3'
import 'md-editor-v3/lib/preview.css'

const docContent = `
# Vestige AI API 接口文档

本文档描述如何通过API Key调用Vestige平台的AI接口，用于程序化创建和管理内容。

## 认证方式

所有AI接口需要通过 \`X-API-Key\` 请求头进行认证：

\`\`\`
X-API-Key: your_api_key_here
\`\`\`

API Key需要先在用户后台创建，并分配相应权限：
- \`read:public\` - 读取公开内容
- \`write:public\` - 创建/更新/删除公开内容

## 基础URL

\`\`\`
http://localhost:8000/api/ai
\`\`\`

生产环境请替换为实际域名。

## 接口列表

### 1. 搜索公开内容

**GET** \`/api/ai/search\`

搜索公开的文章和作品。

**参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 否 | 搜索关键词，匹配标题 |
| type | string | 否 | 类型过滤：\`article\` 或 \`project\` |
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认10，最大100 |

**请求示例：**
\`\`\`bash
curl -X GET "http://localhost:8000/api/ai/search?query=test&type=article&page=1&page_size=10" \
  -H "X-API-Key: your_api_key"
\`\`\`

**响应示例：**
\`\`\`json
{
  "items": [
    {
      "type": "article",
      "id": 1,
      "title": "文章标题",
      "summary": "文章摘要",
      "author": {"id": 1, "username": "作者名"},
      "published_at": "2026-04-26T08:00:00",
      "view_count": 10
    }
  ],
  "total": 1,
  "page": 1,
  "page_size": 10
}
\`\`\`

---

### 2. 创建文章

**POST** \`/api/ai/articles\`

创建一篇公开文章。

**请求体：**
\`\`\`json
{
  "title": "文章标题",
  "content": "文章内容（支持Markdown）",
  "summary": "文章摘要",
  "cover_image": "封面图片URL",
  "tags": ["tag1", "tag2"]
}
\`\`\`

**请求示例：**
\`\`\`bash
curl -X POST "http://localhost:8000/api/ai/articles" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"title":"AI生成的文章","content":"# 标题\\n正文内容...","summary":"摘要","tags":["ai","test"]}'
\`\`\`

**响应示例：**
\`\`\`json
{
  "id": 3,
  "title": "AI生成的文章",
  "is_public": true,
  "created_at": "2026-04-26T08:52:50"
}
\`\`\`

---

### 3. 获取文章详情

**GET** \`/api/ai/articles/{article_id}\`

获取公开文章的完整内容。

**请求示例：**
\`\`\`bash
curl -X GET "http://localhost:8000/api/ai/articles/3" \
  -H "X-API-Key: your_api_key"
\`\`\`

**响应示例：**
\`\`\`json
{
  "id": 3,
  "title": "文章标题",
  "content": "完整内容...",
  "cover_image": "封面URL",
  "summary": "摘要",
  "tags": ["tag1"],
  "view_count": 5,
  "created_at": "2026-04-26T08:00:00",
  "published_at": "2026-04-26T08:00:00"
}
\`\`\`

---

### 4. 更新文章

**PUT** \`/api/ai/articles/{article_id}\`

更新由API Key所属用户创建的公开文章。

**请求体（部分字段可选）：**
\`\`\`json
{
  "title": "新标题",
  "content": "新内容",
  "summary": "新摘要",
  "cover_image": "新封面URL",
  "tags": ["new_tag"]
}
\`\`\`

---

### 5. 删除文章

**DELETE** \`/api/ai/articles/{article_id}\`

删除由API Key所属用户创建的公开文章。

**响应：** HTTP 204 No Content

---

### 6. 创建作品

**POST** \`/api/ai/projects\`

创建一个公开作品。

**请求体：**
\`\`\`json
{
  "name": "作品名称",
  "description": "作品描述",
  "url": "作品链接URL",
  "cover_image": "封面图片URL",
  "tags": ["tag1", "tag2"],
  "tech_stack": ["Python", "Vue"]
}
\`\`\`

---

### 7. 获取作品详情

**GET** \`/api/ai/projects/{project_id}\`

获取公开作品的完整信息。

---

### 8. 更新作品

**PUT** \`/api/ai/projects/{project_id}\`

更新由API Key所属用户创建的公开作品。

---

### 9. 删除作品

**DELETE** \`/api/ai/projects/{project_id}\`

删除由API Key所属用户创建的公开作品。

**响应：** HTTP 204 No Content

---

## 错误响应

### 401 Unauthorized
\`\`\`json
{"detail": "Invalid API key"}
\`\`\`

### 403 Forbidden
\`\`\`json
{"detail": "API key does not have write permission"}
\`\`\`

### 404 Not Found
\`\`\`json
{"detail": "Article not found or not public"}
\`\`\`

---

## Python SDK 示例

\`\`\`python
import requests

class VestigeAI:
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000/api/ai"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"X-API-Key": api_key}
    
    def search(self, query: str = None, type: str = None):
        params = {}
        if query: params["query"] = query
        if type: params["type"] = type
        return requests.get(f"{self.base_url}/search", headers=self.headers, params=params).json()
    
    def create_article(self, title: str, content: str, summary: str = None, tags: list = None):
        data = {"title": title, "content": content}
        if summary: data["summary"] = summary
        if tags: data["tags"] = tags
        return requests.post(f"{self.base_url}/articles", headers=self.headers, json=data).json()
    
    def create_project(self, name: str, description: str = None, tech_stack: list = None):
        data = {"name": name}
        if description: data["description"] = description
        if tech_stack: data["tech_stack"] = tech_stack
        return requests.post(f"{self.base_url}/projects", headers=self.headers, json=data).json()

# 使用示例
client = VestigeAI("your_api_key")
article = client.create_article("AI文章", "内容...", tags=["ai"])
\`\`\`

---

## 获取API Key

1. 登录 Vestige 平台
2. 进入 Dashboard -> API Keys
3. 点击"创建新Key"
4. 选择所需权限
5. 保存生成的Key（只显示一次）
`
</script>

<style scoped>
.api-doc-page {
  max-width: 900px;
  margin: 0 auto;
  padding: var(--spacing-lg);
}

.doc-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.doc-header h1 {
  font-size: var(--font-size-3xl);
  margin-bottom: var(--spacing-sm);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
}

.doc-header p {
  color: var(--text-secondary);
  font-size: var(--font-size-base);
}

.doc-content {
  background: var(--bg-card);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-card);
}

/* 手机端适配 */
@media (max-width: 767px) {
  .api-doc-page {
    padding: var(--spacing-sm);
  }

  .doc-header {
    margin-bottom: var(--spacing-md);
  }

  .doc-header h1 {
    font-size: var(--font-size-lg);
  }

  .doc-header p {
    font-size: var(--font-size-sm);
  }

  .doc-content {
    padding: var(--spacing-sm);
  }

  :deep(.md-preview) {
    font-size: 14px;
    overflow-x: auto;
  }

  :deep(pre) {
    font-size: 12px;
    overflow-x: auto;
  }

  :deep(table) {
    display: block;
    overflow-x: auto;
  }

  :deep(h2) {
    font-size: 16px;
  }

  :deep(h3) {
    font-size: 15px;
  }
}

/* 平板适配 */
@media (min-width: 768px) and (max-width: 1023px) {
  .api-doc-page {
    padding: var(--spacing-md);
    max-width: 100%;
  }
}
</style>