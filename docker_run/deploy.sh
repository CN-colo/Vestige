#!/bin/bash

# Vestige 部署脚本
# 用法: ./deploy.sh [选项]
#   ./deploy.sh        - 拉取镜像并重启服务
#   ./deploy.sh logs   - 查看日志
#   ./deploy.sh stop   - 停止服务

set -e

# 配置 - 根据实际情况修改
IMAGE_OWNER="cn-colo"
BACKEND_IMAGE="ghcr.io/${IMAGE_OWNER}/vestige-backend:latest"
FRONTEND_IMAGE="ghcr.io/${IMAGE_OWNER}/vestige-frontend:latest"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 docker 命令是否可用
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装"
        exit 1
    fi
}

# 拉取镜像
pull_images() {
    log_info "拉取后端镜像: ${BACKEND_IMAGE}"
    docker pull ${BACKEND_IMAGE}
    
    log_info "拉取前端镜像: ${FRONTEND_IMAGE}"
    docker pull ${FRONTEND_IMAGE}
}

# 启动服务
start_services() {
    log_info "启动服务..."
    docker compose up -d
    
    log_info "等待服务健康检查..."
    sleep 5
    
    # 检查服务状态
    if docker ps | grep -q vestige-backend; then
        log_info "后端容器运行中"
    else
        log_error "后端容器启动失败"
        log_info "查看日志: docker logs vestige-backend"
        exit 1
    fi
    
    if docker ps | grep -q vestige-frontend; then
        log_info "前端容器运行中"
    else
        log_error "前端容器启动失败"
        log_info "查看日志: docker logs vestige-frontend"
        exit 1
    fi
    
    log_info "部署完成! 访问 http://localhost:3000"
}

# 停止服务
stop_services() {
    log_info "停止服务..."
    docker compose down
    log_info "服务已停止"
}

# 查看日志
view_logs() {
    docker compose logs -f
}

# 主逻辑
case "${1:-}" in
    stop)
        check_docker
        stop_services
        ;;
    logs)
        check_docker
        view_logs
        ;;
    *)
        check_docker
        log_info "开始部署 Vestige..."
        
        # 停止旧服务
        if docker ps | grep -q vestige; then
            log_info "停止现有服务..."
            docker compose down
        fi
        
        pull_images
        start_services
        ;;
esac