# AI舞蹈教练系统后台管理

## 项目介绍
AI舞蹈教练系统的后台管理界面，基于Vue 3和Vite构建，用于管理舞蹈课程、用户数据、健康数据等系统资源。

## 技术栈
- Vue 3 - 渐进式JavaScript框架
- Vite - 新一代前端构建工具
- Vue Router - 路由管理
- Pinia - 状态管理
- Axios - HTTP客户端

## 项目结构
```
admin/
├── src/                # 源代码目录
│   ├── api/           # API请求
│   ├── assets/        # 静态资源
│   ├── components/    # 公共组件
│   ├── layouts/       # 布局组件
│   ├── router/        # 路由配置
│   ├── stores/        # 状态管理
│   ├── styles/        # 样式文件
│   ├── utils/         # 工具函数
│   └── views/         # 页面组件
├── public/            # 公共资源
├── .env               # 环境变量
└── vite.config.js     # Vite配置
```

## 快速开始

1. 安装依赖：
```bash
npm install
```

2. 配置环境变量：
- 复制`.env.example`为`.env`
- 修改API地址等配置

3. 启动开发服务器：
```bash
npm run dev
```

4. 构建生产版本：
```bash
npm run build
```

## 功能模块
- 用户管理
- 舞蹈课程管理
- 健康数据管理
- 运动处方管理
- 系统设置

## 开发指南
1. 添加新页面：
   - 在`views/`目录创建页面组件
   - 在`router/`中添加路由配置

2. 添加新API：
   - 在`api/`目录添加API请求函数
   - 使用Axios发起请求

3. 状态管理：
   - 在`stores/`目录创建Pinia store
   - 组件中使用store管理状态

## 环境变量说明
```env
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=AI舞蹈教练系统
```
