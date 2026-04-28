# Vestige API Reference

## Authentication

All requests require the `X-API-Key` header with a valid 64-character hex API key.

```http
X-API-Key: <your_api_key>
```

## Base URL

```
{base_url}/api/ai
```

Default base URL: `http://vestige.lastday.top`

## Permissions

| Permission | Code | Operations |
|------------|------|------------|
| Read-only | `read:public` | Search, get article/project details |
| Write | `write:public` | Create, update, delete articles/projects |

## Error Handling

| Status Code | Meaning | Action |
|-------------|---------|--------|
| 401 | Invalid/expired/disabled API Key | Ask user to check key status |
| 403 | Insufficient permissions | Ask user to check key permissions |
| 404 | Content not found | Ask user to verify ID |

## Endpoints

### Search Content

```
GET /api/ai/search
```

**Parameters:**
- `query` (string, optional): Search keywords
- `type` (string, optional): `article` or `project`
- `page` (int, optional): Page number, default 1
- `page_size` (int, optional): Results per page, default 10, max 100

**Response:**
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "page_size": 10
}
```

### Articles

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/articles` | Create article |
| GET | `/api/ai/articles/{id}` | Get article details |
| PUT | `/api/ai/articles/{id}` | Update article |
| DELETE | `/api/ai/articles/{id}` | Delete article |

**Article Fields:**
- `title` (string, required): Article title
- `content` (string, required): Article content (Markdown supported)
- `summary` (string, optional): Article summary
- `cover_image` (string, optional): Cover image URL
- `tags` (array, optional): List of tags

### Projects

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/ai/projects` | Create project |
| GET | `/api/ai/projects/{id}` | Get project details |
| PUT | `/api/ai/projects/{id}` | Update project |
| DELETE | `/api/ai/projects/{id}` | Delete project |

**Project Fields:**
- `name` (string, required): Project name
- `description` (string, optional): Project description
- `url` (string, optional): Project URL
- `cover_image` (string, optional): Cover image URL
- `tags` (array, optional): List of tags
- `tech_stack` (array, optional): List of technologies

## Important Notes

1. **Ownership**: Update/delete operations only work on content owned by the API key's user
2. **Public content**: All AI endpoints only access public content (`is_public=true`)
3. **Markdown support**: Article `content` field supports Markdown formatting
4. **Pagination limit**: Maximum `page_size` is 100