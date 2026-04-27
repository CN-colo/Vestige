# Vestige（古墟）项目指南

## 常用命令

### 后端 (FastAPI)
```bash
cd backend
pip install -r requirements.txt                          # 安装依赖
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000  # 启动开发服务器
```

### 前端 (Vue 3 + TypeScript)
```bash
cd frontend
npm install                                              # 安装依赖
npm run dev                                              # 启动开发服务器 (端口 3000)
npm run build                                            # 构建生产版本
```

### 访问地址
- 前端开发服务器: http://localhost:3000
- 后端 API: http://localhost:8000
- API 文档 (Swagger): http://localhost:8000/docs

## 架构概览

### 后端架构 (backend/app/)
```
backend/app/
├── main.py              # FastAPI 应用入口，注册路由和中间件
├── config.py            # 配置管理 (pydantic-settings)，支持 .env 文件
├── database.py          # SQLAlchemy 配置，Session 工厂
├── models/              # SQLAlchemy ORM 模型
├── schemas/             # Pydantic 请求/响应模型
├── routers/             # API 路由端点
├── middleware/auth.py   # 认证中间件 (JWT + API Key)
└── utils/security.py    # 密码哈希、JWT 生成/验证、API Key 生成
```

**数据模型**: User → Article, Project, ApiKey, Media (级联删除)

**认证方式**:
- 用户认证: JWT Bearer Token (通过 `get_current_user` 依赖)
- AI 接口认证: X-API-Key 请求头 (通过 `verify_api_key_auth` 依赖)

**权限系统**: API Key 支持 `read:public` 和 `write:public` 权限

### 前端架构 (frontend/src/)
```
frontend/src/
├── main.ts              # Vue 应用入口
├── App.vue              # 根组件
├── router/index.ts      # Vue Router 配置，含认证守卫
├── stores/              # Pinia 状态管理
│   ├── user.ts          # 用户认证状态
│   ├── article.ts       # 文章状态
│   └── project.ts       # 作品状态
├── api/                 # API 请求封装
│   ├── request.ts       # Axios 实例，含请求/响应拦截器
│   ├── auth.ts          # 认证 API
│   ├── articles.ts      # 文章 API
│   └── projects.ts      # 作品 API
├── types/index.ts       # TypeScript 类型定义
└── views/               # 页面组件
```

**认证流程**: 登录成功后将 token 存储到 localStorage，Pinia user store 管理用户状态，路由守卫检查 `meta.requiresAuth`

**API 代理**: Vite 开发服务器将 `/api` 和 `/uploads` 请求代理到后端 8000 端口

## 核心概念

### 内容域
- **个人域**: 用户私有的文章/作品，需登录访问 (`/dashboard`)
- **公开域**: 已发布的内容，任何人可访问 (`/` 首页广场)

### 发布机制
- Article/Project 有 `is_public` 字段
- 发布操作设置 `is_public=True` 和 `published_at` 时间戳
- 公开内容通过 `/api/public` 路由访问

### API 接口分组
| 路由前缀 | 认证方式 | 用途 |
|---------|---------|------|
| `/api/auth` | JWT | 用户注册/登录/个人信息 |
| `/api/articles` | JWT | 用户私有文章管理 |
| `/api/projects` | JWT | 用户私有作品管理 |
| `/api/media` | JWT | 图片上传 |
| `/api/keys` | JWT | API Key 管理 |
| `/api/public` | 无 | 公开内容访问 |
| `/api/ai` | X-API-Key | AI 程序调用接口 |

## 开发注意事项

### 后端
- 数据库使用 SQLite，文件 `backend/vestige.db` 自动创建
- 配置可通过 `backend/.env` 文件覆盖 (SECRET_KEY, DATABASE_URL 等)
- 路由文件按资源划分，每个路由导入对应的 schema 和 model
- 密码哈希使用 argon2 (非 bcrypt)，兼容 Python 3.13

### 前端
- Element Plus 组件通过 unplugin 自动导入，无需手动注册
- 使用 `md-editor-v3` 作为 Markdown 编辑器
- API 模块统一使用 `request.ts` 中的 axios 实例
- 类型定义集中在 `types/index.ts`

### 环境配置
后端 `.env` 可配置项:
```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./vestige.db
UPLOAD_DIR=./uploads
```