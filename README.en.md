# Vestige

A modern personal blog and portfolio platform with article publishing, project showcase, and social features.

## Introduction

Vestige is a full-stack web application that provides a space for content creation and presentation. The project adopts a frontend-backend separation architecture supporting:

- **Personal Domain**: Private space for managing articles and projects
- **Public Domain**: Public showcase area for published content
- **Social Features**: Likes, comments, favorites, follows, tag subscriptions

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.13+)
- **Database**: SQLite + SQLAlchemy ORM
- **Authentication**: JWT (Users) + API Key (AI Interface)
- **Password Hashing**: Argon2

### Frontend
- **Framework**: Vue 3 + TypeScript
- **State Management**: Pinia
- **Router**: Vue Router 4
- **UI Components**: Element Plus
- **Markdown Editor**: md-editor-v3
- **Build Tool**: Vite 5

## Quick Start

### 1. Start Backend

```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

After starting:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### 2. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Access: http://localhost:3000

### 3. Build for Production

```bash
cd frontend
npm run build
```

Output in `frontend/dist/` directory.

## Features

### Core
- [x] User registration/login (JWT authentication)
- [x] User profile page
- [x] User card sharing

### Content Management
- [x] Article CRUD + Markdown editor
- [x] Project CRUD
- [x] Image upload
- [x] Personal/Public domain switching
- [x] Public plaza display

### Social Features
- [x] Likes (articles/projects)
- [x] Comments and replies
- [x] Favorites
- [x] Follow users
- [x] Tag subscriptions
- [x] Subscription feed

### Open API
- [x] API Key generation and management
- [x] AI Interface (Key-based authentication)
- [x] Permission control (read:public / write:public)

## API Overview

### Authentication (/api/auth)
- POST /register - Register
- POST /login - Login
- GET /me - Get current user info
- PUT /me - Update user info

### Articles (/api/articles)
- GET / - List user articles
- POST / - Create article
- GET /{id} - Get article detail
- PUT /{id} - Update article
- DELETE /{id} - Delete article
- POST /{id}/publish - Publish to public
- POST /{id}/unpublish - Unpublish

### Projects (/api/projects)
- GET / - List user projects
- POST / - Create project
- GET /{id} - Get project detail
- PUT /{id} - Update project
- DELETE /{id} - Delete project
- POST /{id}/publish - Publish to public

### Public (/api/public)
- GET /articles - List public articles
- GET /articles/{id} - Get public article detail
- GET /projects - List public projects
- GET /projects/{id} - Get public project detail
- GET /users/{id} - Get user public info

### Social (/api/likes, /api/comments, /api/favorites, /api/follows)
- Likes, comments, favorites, follows CRUD operations

### API Keys (/api/keys)
- GET / - List API keys
- POST / - Create API key
- PUT /{id} - Update API key
- DELETE /{id} - Delete API key

### AI Interface (/api/ai) - Requires X-API-Key header
- GET /search - Search public content
- POST/GET/PUT/DELETE /articles - Article operations
- POST/GET/PUT/DELETE /projects - Project operations

### Media (/api/media)
- POST /upload - Upload image
- GET /{id} - Get image info
- DELETE /{id} - Delete image

## Configuration

Backend configuration file: `backend/.env`

```
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///./vestige.db
UPLOAD_DIR=./uploads
```

## Database

The project uses SQLite. Database file `vestige.db` is auto-created in the backend directory.

## License

MIT