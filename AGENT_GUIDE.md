# Vestige Agent 指南

本指南用于指导 AI Agent 如何通过 API Key 调用 Vestige 平台接口，实现内容管理和搜索功能。

## 快速开始

### 1. 获取 API Key

API Key 由用户在 Vestige 平台创建，你需要用户提供以下信息：
- **API Key**: 一个 64 字符的十六进制字符串
- **Base URL**: 生产环境域名或 `http://vestige.lastday.top`

用户获取 API Key 的步骤：
1. 登录 Vestige 平台
2. 进入 Dashboard -> API Keys
3. 点击"创建新 Key"，选择所需权限
4. 保存生成的 Key（只显示一次）

### 2. 认证方式

所有请求需要在 Header 中携带 API Key：

```
X-API-Key: <your_api_key>
```

### 3. 权限说明

| 权限 | 代码 | 可执行操作 |
|------|------|-----------|
| 只读 | `read:public` | 搜索、获取文章/项目详情 |
| 写入 | `write:public` | 创建、更新、删除文章/项目 |

创建 API Key 时需至少包含 `read:public` 权限才能调用任何接口。

---

## API 接口

### 基础 URL

```
{base_url}/api/ai
```

### 接口列表

#### 搜索内容

```
GET /api/ai/search
```

**参数**:
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| query | string | 否 | 搜索关键词 |
| type | string | 否 | `article` 或 `project` |
| page | int | 否 | 页码，默认1 |
| page_size | int | 否 | 每页数量，默认10 |

**请求示例**:
```http
GET /api/ai/search?query=test&type=article
X-API-Key: <api_key>
```

**响应**:
```json
{
  "items": [
    {
      "type": "article",
      "id": 1,
      "title": "标题",
      "summary": "摘要",
      "author": {"id": 1, "username": "作者"},
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

#### 创建文章

```
POST /api/ai/articles
```

**请求体**:
```json
{
  "title": "文章标题",
  "content": "文章内容（支持Markdown）",
  "summary": "摘要",
  "cover_image": "封面图片URL（可选）",
  "tags": ["tag1", "tag2"]
}
```

**响应**:
```json
{
  "id": 3,
  "title": "文章标题",
  "is_public": true,
  "created_at": "2026-04-26T08:52:50"
}
```

---

#### 获取文章详情

```
GET /api/ai/articles/{article_id}
```

**响应**:
```json
{
  "id": 3,
  "title": "标题",
  "content": "完整内容",
  "summary": "摘要",
  "tags": ["tag1"],
  "view_count": 5,
  "created_at": "2026-04-26T08:00:00",
  "published_at": "2026-04-26T08:00:00"
}
```

---

#### 更新文章

```
PUT /api/ai/articles/{article_id}
```

**请求体**（部分字段可选）:
```json
{
  "title": "新标题",
  "content": "新内容",
  "summary": "新摘要",
  "tags": ["new_tag"]
}
```

---

#### 删除文章

```
DELETE /api/ai/articles/{article_id}
```

返回 HTTP 204 无响应体。

---

#### 创建项目

```
POST /api/ai/projects
```

**请求体**:
```json
{
  "name": "项目名称",
  "description": "项目描述",
  "url": "项目链接",
  "cover_image": "封面图片URL（可选）",
  "tags": ["tag1"],
  "tech_stack": ["Python", "Vue"]
}
```

---

#### 获取项目详情

```
GET /api/ai/projects/{project_id}
```

---

#### 更新项目

```
PUT /api/ai/projects/{project_id}
```

---

#### 删除项目

```
DELETE /api/ai/projects/{project_id}
```

返回 HTTP 204 无响应体。

---

## Skill 构建示例

### TypeScript Skill 示例

```typescript
// vestige-skill.ts

interface VestigeConfig {
  apiKey: string;
  baseUrl: string;
}

interface Article {
  title: string;
  content: string;
  summary?: string;
  cover_image?: string;
  tags?: string[];
}

interface Project {
  name: string;
  description?: string;
  url?: string;
  cover_image?: string;
  tags?: string[];
  tech_stack?: string[];
}

class VestigeClient {
  private apiKey: string;
  private baseUrl: string;

  constructor(config: VestigeConfig) {
    this.apiKey = config.apiKey;
    this.baseUrl = config.baseUrl + '/api/ai';
  }

  private async request(method: string, path: string, body?: object) {
    const url = `${this.baseUrl}${path}`;
    const headers = {
      'X-API-Key': this.apiKey,
      'Content-Type': 'application/json'
    };

    const response = await fetch(url, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Vestige API Error: ${response.status} - ${error}`);
    }

    if (response.status === 204) return null;
    return response.json();
  }

  // 搜索内容
  async search(query?: string, type?: string, page = 1, pageSize = 10) {
    const params = new URLSearchParams({
      page: page.toString(),
      page_size: pageSize.toString()
    });
    if (query) params.set('query', query);
    if (type) params.set('type', type);

    return this.request('GET', `/search?${params}`);
  }

  // 创建文章
  async createArticle(article: Article) {
    return this.request('POST', '/articles', article);
  }

  // 获取文章
  async getArticle(id: number) {
    return this.request('GET', `/articles/${id}`);
  }

  // 更新文章
  async updateArticle(id: number, data: Partial<Article>) {
    return this.request('PUT', `/articles/${id}`, data);
  }

  // 删除文章
  async deleteArticle(id: number) {
    return this.request('DELETE', `/articles/${id}`);
  }

  // 创建项目
  async createProject(project: Project) {
    return this.request('POST', '/projects', project);
  }

  // 获取项目
  async getProject(id: number) {
    return this.request('GET', `/projects/${id}`);
  }

  // 更新项目
  async updateProject(id: number, data: Partial<Project>) {
    return this.request('PUT', `/projects/${id}`, data);
  }

  // 删除项目
  async deleteProject(id: number) {
    return this.request('DELETE', `/projects/${id}`);
  }
}

export { VestigeClient, VestigeConfig, Article, Project };
```

### Python Skill 示例

```python
# vestige_skill.py

import requests
from typing import Optional, List, Dict, Any

class VestigeClient:
    """Vestige API Client for AI Agents."""
    
    def __init__(self, api_key: str, base_url: str = "http://vestige.lastday.top"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/') + '/api/ai'
        self.headers = {
            'X-API-Key': api_key,
            'Content-Type': 'application/json'
        }
    
    def _request(self, method: str, path: str, data: Optional[dict] = None) -> Optional[dict]:
        url = f"{self.base_url}{path}"
        response = requests.request(method, url, headers=self.headers, json=data)
        
        if response.status_code == 204:
            return None
        
        if not response.ok:
            raise Exception(f"Vestige API Error: {response.status_code} - {response.text}")
        
        return response.json()
    
    def search(
        self,
        query: Optional[str] = None,
        type: Optional[str] = None,
        page: int = 1,
        page_size: int = 10
    ) -> dict:
        """搜索公开内容"""
        params = {'page': page, 'page_size': page_size}
        if query:
            params['query'] = query
        if type:
            params['type'] = type
        
        param_str = '&'.join(f"{k}={v}" for k, v in params.items())
        return self._request('GET', f"/search?{param_str}")
    
    def create_article(
        self,
        title: str,
        content: str,
        summary: Optional[str] = None,
        cover_image: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> dict:
        """创建公开文章"""
        data = {'title': title, 'content': content}
        if summary:
            data['summary'] = summary
        if cover_image:
            data['cover_image'] = cover_image
        if tags:
            data['tags'] = tags
        return self._request('POST', '/articles', data)
    
    def get_article(self, article_id: int) -> dict:
        """获取文章详情"""
        return self._request('GET', f"/articles/{article_id}")
    
    def update_article(self, article_id: int, **kwargs) -> dict:
        """更新文章"""
        return self._request('PUT', f"/articles/{article_id}", kwargs)
    
    def delete_article(self, article_id: int) -> None:
        """删除文章"""
        self._request('DELETE', f"/articles/{article_id}")
    
    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        url: Optional[str] = None,
        cover_image: Optional[str] = None,
        tags: Optional[List[str]] = None,
        tech_stack: Optional[List[str]] = None
    ) -> dict:
        """创建公开项目"""
        data = {'name': name}
        if description:
            data['description'] = description
        if url:
            data['url'] = url
        if cover_image:
            data['cover_image'] = cover_image
        if tags:
            data['tags'] = tags
        if tech_stack:
            data['tech_stack'] = tech_stack
        return self._request('POST', '/projects', data)
    
    def get_project(self, project_id: int) -> dict:
        """获取项目详情"""
        return self._request('GET', f"/projects/{project_id}")
    
    def update_project(self, project_id: int, **kwargs) -> dict:
        """更新项目"""
        return self._request('PUT', f"/projects/{project_id}", kwargs)
    
    def delete_project(self, project_id: int) -> None:
        """删除项目"""
        self._request('DELETE', f"/projects/{project_id}")


# 使用示例
def example_usage():
    # 初始化客户端（需要用户提供 API Key）
    client = VestigeClient(
        api_key="your_api_key_here",
        base_url="http://vestige.lastday.top"
    )
    
    # 搜索文章
    results = client.search(query="test", type="article")
    print(f"找到 {results['total']} 条结果")
    
    # 创建文章
    article = client.create_article(
        title="AI 生成的文章",
        content="# 标题\n这是文章内容...",
        summary="文章摘要",
        tags=["ai", "automation"]
    )
    print(f"创建文章 ID: {article['id']}")
    
    # 更新文章
    updated = client.update_article(article['id'], title="更新后的标题")
    print(f"更新成功: {updated['title']}")
    
    # 创建项目
    project = client.create_project(
        name="AI 项目",
        description="项目描述",
        url="https://example.com",
        tech_stack=["Python", "FastAPI"]
    )
    print(f"创建项目 ID: {project['id']}")
```

---

## Agent 工作流程

### 标准操作流程

1. **获取配置**: 向用户请求 API Key 和 Base URL
2. **验证权限**: 通过搜索接口验证 API Key 是否有效
3. **执行任务**: 根据用户需求调用对应接口
4. **反馈结果**: 返回操作结果或错误信息

### 错误处理

| 状态码 | 含义 | 处理方式 |
|--------|------|----------|
| 401 | API Key 无效/过期/禁用 | 提示用户检查 Key 状态 |
| 403 | 权限不足 | 提示用户 Key 缺少对应权限 |
| 404 | 内容不存在 | 提示用户检查 ID 是否正确 |

### 安全建议

- 不要在代码中硬编码 API Key
- 使用环境变量或配置文件存储
- 建议用户使用 `read:public` 权限的 Key 进行只读操作
- 创建内容时才使用 `write:public` 权限的 Key

---

## 典型任务示例

### 任务1: 搜索并总结内容

```
用户: 搜索关于 "Python" 的文章并总结

Agent 步骤:
1. 调用 GET /api/ai/search?query=Python&type=article
2. 获取返回的文章列表
3. 对每篇文章调用 GET /api/ai/articles/{id} 获取完整内容
4. 总结文章内容返回给用户
```

### 任务2: 批量创建文章

```
用户: 创建以下三篇文章: [标题列表]

Agent 步骤:
1. 确认 API Key 有 write:public 权限
2. 遍历标题列表，调用 POST /api/ai/articles
3. 返回创建的文章 ID 列表
```

### 任务3: 更新项目信息

```
用户: 更新项目 ID 5 的描述为 "新描述"

Agent 步骤:
1. 调用 PUT /api/ai/projects/5 {"description": "新描述"}
2. 返回更新后的项目信息
```

---

## Skill 配置模板

创建 Vestige Skill 时，需要用户提供以下配置：

```json
{
  "name": "vestige",
  "description": "Vestige 内容管理平台操作",
  "config": {
    "api_key": {
      "type": "string",
      "required": true,
      "description": "Vestige API Key (64字符十六进制)"
    },
    "base_url": {
      "type": "string",
      "required": true,
      "default": "http://vestige.lastday.top",
      "description": "Vestige 服务地址"
    }
  },
  "capabilities": [
    "搜索公开文章和项目",
    "创建/更新/删除文章",
    "创建/更新/删除项目"
  ]
}
```

---

## 注意事项

1. **所有权限制**: 更新和删除操作只能作用于 API Key 所属用户创建的内容
2. **公开内容**: AI 接口只能操作公开内容（`is_public=true`）
3. **Markdown 支持**: 文章 `content` 字段支持 Markdown 格式
4. **分页限制**: 搜索接口 `page_size` 最大值为 100
5. **时间戳**: 创建/更新操作会自动设置 `published_at` 和时间戳