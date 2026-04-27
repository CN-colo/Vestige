# Vestige（古墟）

一个现代化的个人博客和作品展示平台，支持文章发布、作品展示、社交互动等功能。

## 项目介绍

Vestige（古墟）是一个全栈 Web 应用，为用户提供内容创作与展示的空间。项目采用前后端分离架构，支持：

- **个人域**：用户私有的文章/作品管理空间
- **公开域**：已发布内容的公共展示区域，任何人可访问
- **社交功能**：点赞、评论、收藏、关注、标签订阅

## 技术栈

### 后端
- **框架**：FastAPI (Python 3.13+)
- **数据库**：SQLite + SQLAlchemy ORM
- **认证**：JWT (用户) + API Key (AI 接口)
- **密码哈希**：Argon2

### 前端
- **框架**：Vue 3 + TypeScript
- **状态管理**：Pinia
- **路由**：Vue Router 4
- **UI 组件**：Element Plus
- **Markdown 编辑器**：md-editor-v3
- **构建工具**：Vite 5

## 项目结构

```
Vestige/
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── main.py            # 应用入口
│   │   ├── config.py          # 配置管理
│   │   ├── database.py        # 数据库配置
│   │   ├── models/            # ORM 模型
│   │   ├── schemas/           # Pydantic 模型
│   │   ├── routers/           # API 路由
│   │   ├── middleware/        # 中间件
│   │   └── utils/             # 工具函数
│   ├── uploads/               # 文件上传目录
│   ├── vestige.db             # SQLite 数据库
│   └── requirements.txt
├── frontend/                   # Vue 3 前端
│   ├── src/
│   │   ├── views/             # 页面组件
│   │   ├── components/        # 通用组件
│   │   ├── stores/            # Pinia 状态管理
│   │   ├── api/               # API 封装
│   │   ├── types/             # TypeScript 类型
│   │   └── router/            # 路由配置
│   ├── package.json
│   └── vite.config.ts
├── AGENTS.md                   # 项目开发指南
├── AI_API.md                   # AI 接口文档
└── README.md
```

## 启动步骤

### 1. 启动后端

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端启动后访问：
- API: http://localhost:8000
- API 文档: http://localhost:8000/docs

### 2. 启动前端开发服务器

```bash
cd frontend
npm install
npm run dev
```

前端启动后访问: http://localhost:3000

### 3. 构建前端生产版本

```bash
cd frontend
npm run build
```

构建输出在 `frontend/dist/` 目录。

## API 接口概览

### 用户认证 (/api/auth)
- POST /register - 注册
- POST /login - 登录
- GET /me - 获取当前用户信息
- PUT /me - 更新用户信息

### 文章管理 (/api/articles)
- GET / - 获取用户文章列表
- POST / - 创建文章
- GET /{id} - 获取文章详情
- PUT /{id} - 更新文章
- DELETE /{id} - 删除文章
- POST /{id}/publish - 发布到公开域
- POST /{id}/unpublish - 取消发布

### 作品管理 (/api/projects)
- GET / - 获取用户作品列表
- POST / - 创建作品
- GET /{id} - 获取作品详情
- PUT /{id} - 更新作品
- DELETE /{id} - 删除作品
- POST /{id}/publish - 发布到公开域

### 公开域 (/api/public)
- GET /articles - 获取公开文章列表
- GET /articles/{id} - 获取公开文章详情
- GET /projects - 获取公开作品列表
- GET /projects/{id} - 获取公开作品详情
- GET /users/{id} - 获取用户公开信息

### API Key 管理 (/api/keys)
- GET / - 获取 API Key 列表
- POST / - 创建 API Key
- PUT /{id} - 更新 API Key
- DELETE /{id} - 删除 API Key

### AI 接口 (/api/ai) - 需要 X-API-Key 请求头
- GET /search - 搜索公开域内容
- POST /articles - 创建公开文章
- GET /articles/{id} - 读取公开文章
- PUT /articles/{id} - 更新公开文章
- DELETE /articles/{id} - 删除公开文章
- POST /projects - 创建公开作品
- GET /projects/{id} - 读取公开作品
- PUT /projects/{id} - 更新公开作品
- DELETE /projects/{id} - 删除公开作品

### 媒体资源 (/api/media)
- POST /upload - 上传图片
- GET /{id} - 获取图片信息
- DELETE /{id} - 删除图片

## 数据库

项目使用 SQLite 数据库，数据库文件 `vestige.db` 在 backend 目录下自动创建。

## 环境配置

后端配置文件: `backend/.env`
- 可修改 SECRET_KEY、数据库路径、上传目录等配置

## 功能特性

### 核心功能
- [x] 用户注册/登录（JWT 认证）
- [x] 用户个人主页
- [x] 用户名片分享

### 内容管理
- [x] 文章 CRUD + Markdown 编辑器
- [x] 作品 CRUD
- [x] 图片上传
- [x] 公开域/个人域切换
- [x] 公开域广场展示

### 社交功能
- [x] 点赞（文章/作品）
- [x] 评论与回复
- [x] 收藏
- [x] 关注用户
- [x] 标签订阅
- [x] 订阅内容动态流

### 开放接口
- [x] API Key 生成与管理
- [x] AI 接口（基于 Key 认证）
- [x] 权限控制（read:public / write:public）

## 数据模型

```
User (用户)
  ├── Article (文章)
  ├── Project (作品)
  ├── Media (媒体资源)
  ├── ApiKey (API 密钥)
  ├── Favorite (收藏)
  ├── Like (点赞)
  ├── Comment (评论)
  ├── Follow (关注关系)
  └── TagSubscription (标签订阅)
```

## 访问地址

- 前端开发服务器: http://localhost:3000
- 后端 API: http://localhost:8000
- API 文档 (Swagger): http://localhost:8000/docs