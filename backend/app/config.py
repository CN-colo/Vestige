from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    APP_NAME: str = "Vestige"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 生产环境 URL，用于生成 Agent 指南链接
    # 本地调试时可设置为 http://localhost:8000
    BASE_URL: str = "http://vestige.lastday.top"
    
    DATABASE_URL: str = "sqlite:///./vestige.db"
    
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    @property
    def effective_base_url(self) -> str:
        """获取实际使用的 BASE_URL，DEBUG 模式下使用本地地址"""
        if self.DEBUG:
            return f"http://localhost:{self.PORT}"
        return self.BASE_URL
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()