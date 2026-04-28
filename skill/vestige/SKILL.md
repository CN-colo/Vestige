---
name: vestige
description: Interact with Vestige content management platform for searching, creating, updating, and deleting articles and projects. Use when the user wants to: (1) Search or browse public articles/projects, (2) Create new articles or projects with Markdown content, (3) Update or delete existing content, (4) Manage their Vestige publications. Requires API key from user - always ask for API key and base URL before making API calls.
---

# Vestige

## Overview

This skill enables interaction with the Vestige content management platform through its AI API. Supports searching public content, creating/updating/deleting articles and projects.

## Prerequisites

Before using any Vestige operations, obtain these from the user:

1. **API Key**: 64-character hex string from Vestige Dashboard → API Keys
2. **Base URL**: Default is `http://vestige.lastday.top` (ask if using different server)

Validate the API key by performing a simple search before other operations.

## Quick Start

```python
from scripts.vestige_client import VestigeClient

client = VestigeClient(
    api_key="user_provided_api_key",
    base_url="http://vestige.lastday.top"
)

# Test connection with search
results = client.search(page=1, page_size=1)
```

## Core Capabilities

### 1. Search Content

Search public articles and projects:

```python
# Search all content
results = client.search(query="Python")

# Filter by type
articles = client.search(query="tutorial", type="article")
projects = client.search(query="web", type="project")

# Pagination
results = client.search(page=2, page_size=20)
```

Returns: `{"items": [...], "total": 100, "page": 1, "page_size": 10}`

### 2. Manage Articles

Create, read, update, delete articles:

```python
# Create article
article = client.create_article(
    title="My Article",
    content="# Heading\n\nArticle content in **Markdown**.",
    summary="Brief summary",
    tags=["python", "tutorial"]
)

# Get article
article = client.get_article(article_id=123)

# Update article
client.update_article(article_id=123, title="New Title")

# Delete article
client.delete_article(article_id=123)
```

### 3. Manage Projects

Create, read, update, delete projects:

```python
# Create project
project = client.create_project(
    name="My Project",
    description="Project description",
    url="https://github.com/user/repo",
    tech_stack=["Python", "FastAPI", "Vue"]
)

# Get project
project = client.get_project(project_id=456)

# Update project
client.update_project(project_id=456, description="Updated description")

# Delete project
client.delete_project(project_id=456)
```

## Common Workflows

### Search and Summarize

1. Search for content matching user query
2. For each result, get full details if needed
3. Summarize findings for user

### Batch Create Content

1. Confirm API key has `write:public` permission
2. Iterate through content list
3. Create each item and collect IDs
4. Report results to user

### Update Existing Content

1. Search to find the content ID
2. Get current details to show user
3. Apply requested changes
4. Confirm update success

## Error Handling

| Status | Meaning | User Action |
|--------|---------|-------------|
| 401 | Invalid/expired key | Check API key in Dashboard |
| 403 | Permission denied | Verify key has required permission |
| 404 | Not found | Check if ID is correct and content is public |

## API Reference

See [references/api_reference.md](references/api_reference.md) for complete API documentation including all endpoints, parameters, and response formats.

## Security Notes

- Never hardcode API keys in code
- Use environment variables or ask user for key at runtime
- Recommend `read:public` key for read-only operations
- Only use `write:public` key when creating/updating content
- Users can only modify content they own