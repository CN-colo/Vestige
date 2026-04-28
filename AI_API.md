# Vestige AI API 接口文档

本文档描述如何通过API Key调用Vestige平台的AI接口，用于程序化创建和管理内容。

## 认证方式

所有AI接口需要通过 `X-API-Key` 请求头进行认证：

```
X-API-Key: your_api_key_here
```

API Key需要先在用户后台创建，并分配相应权限：
- `read:public` - 读取公开内容
- `write:public` - 创建/更新/删除公开内容

## 基础URL

```
http://vestige.lastday.top/api/ai
```

生产环境请替换为实际域名。

## 接口列表

### 1. 搜索公开内容

**GET** `/api/ai/search`

搜索公开的文章和作品。

**参数：**
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 否 | 搜索关键词，匹配标题 |
| type | string | 否 | 类型过滤：`article` 或 `project` |
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认10，最大100 |

**请求示例：**
```bash
curl -X GET "http://vestige.lastday.top/api/ai/search?query=test&type=article&page=1&page_size=10" \
  -H "X-API-Key: your_api_key"
```

**响应示例：**
```json
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
```

---

### 2. 创建文章

**POST** `/api/ai/articles`

创建一篇公开文章。

**请求体：**
```json
{
  "title": "文章标题",
  "content": "文章内容（支持Markdown）",
  "summary": "文章摘要",
  "cover_image": "封面图片URL",
  "tags": ["tag1", "tag2"]
}
```

**请求示例：**
```bash
curl -X POST "http://vestige.lastday.top/api/ai/articles" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"title":"AI生成的文章","content":"# 标题\n正文内容...","summary":"摘要","tags":["ai","test"]}'
```

**响应示例：**
```json
{
  "id": 3,
  "title": "AI生成的文章",
  "is_public": true,
  "created_at": "2026-04-26T08:52:50"
}
```

---

### 3. 获取文章详情

**GET** `/api/ai/articles/{article_id}`

获取公开文章的完整内容。

**请求示例：**
```bash
curl -X GET "http://vestige.lastday.top/api/ai/articles/3" \
  -H "X-API-Key: your_api_key"
```

**响应示例：**
```json
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
```

---

### 4. 更新文章

**PUT** `/api/ai/articles/{article_id}`

更新由API Key所属用户创建的公开文章。

**请求体（部分字段可选）：**
```json
{
  "title": "新标题",
  "content": "新内容",
  "summary": "新摘要",
  "cover_image": "新封面URL",
  "tags": ["new_tag"]
}
```

**请求示例：**
```bash
curl -X PUT "http://vestige.lastday.top/api/ai/articles/3" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"title":"更新后的标题"}'
```

**响应示例：**
```json
{
  "id": 3,
  "title": "更新后的标题",
  "updated_at": "2026-04-26T09:00:00"
}
```

---

### 5. 删除文章

**DELETE** `/api/ai/articles/{article_id}`

删除由API Key所属用户创建的公开文章。

**请求示例：**
```bash
curl -X DELETE "http://vestige.lastday.top/api/ai/articles/3" \
  -H "X-API-Key: your_api_key"
```

**响应：** HTTP 204 No Content（无响应体）

---

### 6. 创建作品

**POST** `/api/ai/projects`

创建一个公开作品。

**请求体：**
```json
{
  "name": "作品名称",
  "description": "作品描述",
  "url": "作品链接URL",
  "cover_image": "封面图片URL",
  "tags": ["tag1", "tag2"],
  "tech_stack": ["Python", "Vue"]
}
```

**请求示例：**
```bash
curl -X POST "http://vestige.lastday.top/api/ai/projects" \
  -H "X-API-Key: your_api_key" \
  -H "Content-Type: application/json" \
  -d '{"name":"AI项目","description":"项目描述","url":"https://example.com","tech_stack":["Python","FastAPI"]}'
```

**响应示例：**
```json
{
  "id": 2,
  "name": "AI项目",
  "is_public": true,
  "created_at": "2026-04-26T08:52:52"
}
```

---

### 7. 获取作品详情

**GET** `/api/ai/projects/{project_id}`

获取公开作品的完整信息。

**请求示例：**
```bash
curl -X GET "http://vestige.lastday.top/api/ai/projects/2" \
  -H "X-API-Key: your_api_key"
```

**响应示例：**
```json
{
  "id": 2,
  "name": "作品名称",
  "description": "描述内容",
  "url": "https://example.com",
  "cover_image": "封面URL",
  "tags": ["tag1"],
  "tech_stack": ["Python"],
  "view_count": 5,
  "created_at": "2026-04-26T08:00:00",
  "published_at": "2026-04-26T08:00:00"
}
```

---

### 8. 更新作品

**PUT** `/api/ai/projects/{project_id}`

更新由API Key所属用户创建的公开作品。

**请求体（部分字段可选）：**
```json
{
  "name": "新名称",
  "description": "新描述",
  "url": "新链接",
  "cover_image": "新封面",
  "tags": ["new_tag"],
  "tech_stack": ["新技术"]
}
```

---

### 9. 删除作品

**DELETE** `/api/ai/projects/{project_id}`

删除由API Key所属用户创建的公开作品。

**响应：** HTTP 204 No Content

---

## 错误响应

### 401 Unauthorized
```json
{
  "detail": "Invalid API key"
}
```
或
```json
{
  "detail": "API key is deactivated"
}
```
或
```json
{
  "detail": "API key has expired"
}
```

### 403 Forbidden
```json
{
  "detail": "API key does not have read permission"
}
```
或
```json
{
  "detail": "API key does not have write permission"
}
```

### 404 Not Found
```json
{
  "detail": "Article not found or not public"
}
```
或
```json
{
  "detail": "Article not found or not owned by API key owner"
}
```

---

## 最佳实践

### 1. 安全存储API Key
不要在代码中硬编码API Key，建议使用环境变量：
```python
import os
API_KEY = os.environ.get("VESTIGE_API_KEY")
```

### 2. 内容格式
- `content` 字段支持Markdown格式
- `tags` 和 `tech_stack` 是字符串数组
- `cover_image` 需要提供完整的URL地址

### 3. 权限检查
调用接口前确认API Key有对应权限：
- 搜索、获取详情需要 `read:public`
- 创建、更新、删除需要 `write:public`

### 4. 错误处理
建议对所有API调用进行错误处理：
```python
import requests

response = requests.get(url, headers={"X-API-Key": api_key})
if response.status_code == 401:
    print("API Key无效或已过期")
elif response.status_code == 403:
    print("权限不足")
elif response.status_code == 404:
    print("内容不存在")
else:
    data = response.json()
```

---

## Python SDK 示例

```python
import requests

class VestigeAI:
    def __init__(self, api_key: str, base_url: str = "http://vestige.lastday.top/api/ai"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"X-API-Key": api_key}
    
    def search(self, query: str = None, type: str = None, page: int = 1, page_size: int = 10):
        params = {"page": page, "page_size": page_size}
        if query:
            params["query"] = query
        if type:
            params["type"] = type
        return requests.get(f"{self.base_url}/search", headers=self.headers, params=params).json()
    
    def create_article(self, title: str, content: str, summary: str = None, tags: list = None):
        data = {"title": title, "content": content}
        if summary:
            data["summary"] = summary
        if tags:
            data["tags"] = tags
        return requests.post(f"{self.base_url}/articles", headers=self.headers, json=data).json()
    
    def get_article(self, article_id: int):
        return requests.get(f"{self.base_url}/articles/{article_id}", headers=self.headers).json()
    
    def update_article(self, article_id: int, **kwargs):
        return requests.put(f"{self.base_url}/articles/{article_id}", headers=self.headers, json=kwargs).json()
    
    def delete_article(self, article_id: int):
        requests.delete(f"{self.base_url}/articles/{article_id}", headers=self.headers)
    
    def create_project(self, name: str, description: str = None, url: str = None, tech_stack: list = None):
        data = {"name": name}
        if description:
            data["description"] = description
        if url:
            data["url"] = url
        if tech_stack:
            data["tech_stack"] = tech_stack
        return requests.post(f"{self.base_url}/projects", headers=self.headers, json=data).json()
    
    def get_project(self, project_id: int):
        return requests.get(f"{self.base_url}/projects/{project_id}", headers=self.headers).json()
    
    def update_project(self, project_id: int, **kwargs):
        return requests.put(f"{self.base_url}/projects/{project_id}", headers=self.headers, json=kwargs).json()
    
    def delete_project(self, project_id: int):
        requests.delete(f"{self.base_url}/projects/{project_id}", headers=self.headers)

# 使用示例
client = VestigeAI("your_api_key")

# 搜索内容
results = client.search(query="test")

# 创建文章
article = client.create_article(
    title="AI自动生成的文章",
    content="这是文章正文内容...",
    summary="文章摘要",
    tags=["ai", "automation"]
)

# 获取文章
article = client.get_article(article["id"])

# 更新文章
client.update_article(article["id"], title="更新后的标题")

# 创建项目
project = client.create_project(
    name="AI项目",
    description="项目描述",
    url="https://example.com",
    tech_stack=["Python", "FastAPI"]
)
```

---

## 获取API Key

1. 登录 Vestige 平台
2. 进入 Dashboard -> API Keys
3. 点击"创建新Key"
4. 选择所需权限
5. 保存生成的Key（只显示一次）