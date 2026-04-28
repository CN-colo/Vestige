import axios from 'axios'
import type { AxiosInstance, AxiosRequestConfig } from 'axios'
import { useUserStore } from '@/stores/user'
import router from '@/router'

// 自定义请求接口，返回类型是 T 而不是 AxiosResponse<T>
interface CustomAxiosInstance {
  get<T>(url: string, config?: AxiosRequestConfig): Promise<T>
  post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
  put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T>
  delete<T>(url: string, config?: AxiosRequestConfig): Promise<T>
  defaults: AxiosInstance['defaults']
}

const request: AxiosInstance = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
request.interceptors.request.use(
  (config) => {
    // Get token directly from localStorage to avoid Pinia timing issues
    const token = localStorage.getItem('token')
    console.log('Request interceptor - token:', token ? 'exists' : 'null')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Helper function to extract error message from various error formats
function extractErrorMessage(errorData: any): string {
  if (!errorData) return '请求失败'

  const detail = errorData.detail

  // Handle Pydantic validation errors (array of error objects)
  if (Array.isArray(detail) && detail.length > 0) {
    const firstError = detail[0]
    // Extract field name from loc array (e.g., ["body", "password"] -> "password")
    const field = firstError.loc?.slice(-1)[0] || '字段'
    const message = firstError.msg || '验证失败'
    // Translate field names
    const fieldNames: Record<string, string> = {
      username: '用户名',
      password: '密码',
      email: '邮箱'
    }
    const fieldName = fieldNames[field] || field
    return `${fieldName}${message.replace('String should have at least', '长度至少为').replace('characters', '个字符')}`
  }

  // Handle simple string detail
  if (typeof detail === 'string') {
    return detail
  }

  // Handle message field
  if (errorData.message) {
    return errorData.message
  }

  return '请求失败'
}

// Response interceptor
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
      // Extract and attach a user-friendly error message
      error.userMessage = extractErrorMessage(error.response.data)

      if (error.response.status === 401) {
        const userStore = useUserStore()
        userStore.logout()
        router.push('/login')
      }
    }
    return Promise.reject(error)
  }
)

// 导出为 CustomAxiosInstance 类型以获得正确的返回类型
export default request as CustomAxiosInstance