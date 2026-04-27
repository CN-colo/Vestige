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

// Response interceptor
request.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    if (error.response) {
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