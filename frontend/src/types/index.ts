// User types
export interface User {
  id: number
  username: string
  email: string
  avatar?: string
  bio?: string
  contact?: string
  card_enabled?: boolean
  is_active: boolean
  created_at: string
}

export interface UserPublic {
  id: number
  username: string
  avatar?: string
  bio?: string
  contact?: string
  articles_count?: number
  projects_count?: number
  created_at?: string
}

// Auth types
export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface TokenResponse {
  access_token: string
  token_type: string
}

// Article types
export interface Article {
  id: number
  user_id: number
  title: string
  content: string
  cover_image?: string
  summary?: string
  tags?: string[]
  is_public: boolean
  published_at?: string
  view_count: number
  like_count: number
  created_at: string
  updated_at?: string
  author?: { id: number; username: string; avatar?: string }
}

export interface ArticleCreate {
  title: string
  content: string
  cover_image?: string
  summary?: string
  tags?: string[]
}

export interface ArticleUpdate {
  title?: string
  content?: string
  cover_image?: string
  summary?: string
  tags?: string[]
}

export interface ArticlePublic {
  id: number
  title: string
  content: string
  cover_image?: string
  summary?: string
  tags?: string[]
  published_at?: string
  created_at?: string
  view_count: number
  author?: { id: number; username: string }
}

// Project types
export interface Project {
  id: number
  user_id: number
  name: string
  description: string
  content: string
  url?: string
  cover_image?: string
  tags?: string[]
  tech_stack?: string[]
  is_public: boolean
  published_at?: string
  view_count: number
  like_count: number
  created_at: string
  updated_at?: string
  author?: { id: number; username: string; avatar?: string }
}

export interface ProjectCreate {
  name: string
  description: string
  content?: string
  url?: string
  cover_image?: string
  tags?: string[]
  tech_stack?: string[]
}

export interface ProjectUpdate {
  name?: string
  description?: string
  content?: string
  url?: string
  cover_image?: string
  tags?: string[]
  tech_stack?: string[]
}

export interface ProjectPublic {
  id: number
  name: string
  description: string
  url?: string
  cover_image?: string
  tags?: string[]
  tech_stack?: string[]
  published_at?: string
  created_at?: string
  view_count: number
  author?: { id: number; username: string }
}

// API Key types
export interface ApiKey {
  id: number
  name?: string
  permissions?: string[]
  is_active: boolean
  last_used_at?: string
  expires_at?: string
  created_at: string
}

export interface ApiKeyCreate {
  name?: string
  permissions?: string[]
  expires_at?: string
}

export interface ApiKeyCreated {
  id: number
  key: string
  name?: string
  permissions?: string[]
  expires_at?: string
  created_at: string
}

export interface ApiKeyUpdate {
  name?: string
  permissions?: string[]
  is_active?: boolean
}

// Pagination types
export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

// Media types
export interface Media {
  id: number
  filename: string
  original_name: string
  file_path: string
  file_size: number
  mime_type: string
  url?: string
  created_at: string
}

// Favorite types
export interface Favorite {
  id: number
  user_id: number
  target_type: 'article' | 'project'
  target_id: number
  created_at: string
}

export interface FavoriteWithItem extends Favorite {
  item?: {
    id: number
    title?: string  // for articles
    name?: string   // for projects
    summary?: string
    description?: string
    cover_image?: string
    view_count: number
    author: {
      id: number
      username: string
      avatar?: string
    }
  }
}

export interface FavoriteCreate {
  target_type: 'article' | 'project'
  target_id: number
}

// Comment types
export interface CommentAuthor {
  id: number
  username: string
  avatar?: string
}

export interface Comment {
  id: number
  user_id: number
  content_type: 'article' | 'project'
  content_id: number
  content: string
  parent_id?: number
  created_at: string
  updated_at?: string
  author?: CommentAuthor
  replies?: Comment[]
}

export interface CommentCreate {
  content_type: 'article' | 'project'
  content_id: number
  content: string
  parent_id?: number
}

export interface CommentUpdate {
  content: string
}

// Follow types
export interface FollowRequest {
  user_id: number
}

export interface FollowStats {
  following_count: number
  followers_count: number
}

export interface UserWithFollowStatus {
  id: number
  username: string
  avatar?: string
  bio?: string
  is_following: boolean
  followers_count: number
  following_count: number
}

// Tag Subscription types
export interface TagSubscriptionCreate {
  tag: string
}

export interface TagSubscriptionList {
  tags: string[]
  total: number
}

export interface SubscriptionFeedItem {
  id: number
  title?: string
  name?: string
  summary?: string
  description?: string
  cover_image?: string
  tags?: string[]
  tech_stack?: string[]
  view_count: number
  like_count: number
  published_at?: string
  author: {
    id: number
    username: string
    avatar?: string
  }
}

export interface SubscriptionFeed {
  articles: SubscriptionFeedItem[]
  projects: SubscriptionFeedItem[]
  total_articles: number
  total_projects: number
  page: number
  page_size: number
  subscribed_tags?: string[]
}

// Like types
export interface LikeRequest {
  target_type: 'article' | 'project'
  target_id: number
}

export interface LikeStatus {
  is_liked: boolean
  like_count: number
}

export interface Like {
  id: number
  user_id: number
  target_type: 'article' | 'project'
  target_id: number
  created_at: string
}