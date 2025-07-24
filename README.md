# 舞动银龄——基于多模态AI的舞蹈教学与反馈系统

<p align="center">
  <img src="/public/fonticon.png" alt="舞动银龄" width="120">
</p>

<p align="center">
  <b>基于多模态AI的舞蹈教学与反馈系统，专为老年人设计的智能舞蹈学习平台</b>
</p>

## 项目简介

这是"舞动银龄"平台的统一前端项目，采用最新的Vue 3 + TypeScript技术栈构建。本项目整合了原有的公共前台和管理后台，提供了一致的用户体验和开发模式。通过多模态AI技术，为老年用户提供智能化的舞蹈教学与实时反馈，让舞蹈学习更加高效、有趣。

## 技术栈

- **核心框架**: Vue 3 (Composition API)
- **开发语言**: TypeScript
- **构建工具**: Vite
- **路由管理**: Vue Router 4
- **状态管理**: Pinia
- **UI组件库**: Element Plus
- **图标**: @element-plus/icons-vue
- **HTTP请求**: Axios
- **CSS方案**: UnoCSS (原子化CSS)
- **代码规范**: ESLint + Prettier
- **Git钩子**: Husky + Commitlint
- **测试工具**: Vitest + Cypress

## 项目结构

```
src/
├─ api/                    # API服务层
│   ├─ user.ts            # 用户相关API
│   ├─ course.ts          # 课程相关API
│   ├─ health.ts          # 健康相关API
│   └─ ...                # 其他API模块
├─ assets/                 # 静态资源
├─ components/             # 组件
│   ├─ common/            # 通用组件
│   │   ├─ MainNav.vue    # 主导航
│   │   ├─ AppFooter.vue  # 页脚
│   │   └─ ...            # 其他通用组件
│   └─ specific/          # 业务专用组件
├─ layouts/                # 布局组件
│   ├─ PublicLayout.vue   # 公共页面布局
│   └─ AdminLayout.vue    # 后台页面布局
├─ router/                 # 路由配置
│   ├─ index.ts           # 路由入口
│   ├─ routes-public.ts   # 公共路由
│   └─ routes-admin.ts    # 后台路由
├─ stores/                 # Pinia状态管理
│   ├─ user.ts            # 用户状态
│   ├─ dance.ts           # 舞蹈相关状态
│   ├─ health.ts          # 健康相关状态
│   └─ social.ts          # 社交相关状态
├─ style/                  # 样式文件
│   └─ index.css          # 全局样式
├─ utils/                  # 工具函数
│   ├─ request.ts         # Axios封装
│   └─ ...                # 其他工具
├─ views/                  # 页面组件
│   ├─ public/            # 公共页面
│   │   ├─ Home.vue       # 首页
│   │   ├─ DanceCourses.vue # 舞蹈课程
│   │   └─ ...            # 其他公共页面
│   └─ admin/             # 后台页面
│       ├─ Dashboard.vue  # 仪表盘
│       ├─ UserManagement.vue # 用户管理
│       └─ ...            # 其他后台页面
├─ App.vue                 # 根组件
└─ main.ts                 # 入口文件
```

## 开发指南

### 安装依赖

```bash
npm install
```

### 启动开发服务器

```bash
npm run dev
```

### 构建生产版本

```bash
npm run build
```

### 代码格式化

```bash
npm run format
```

### 代码检查

```bash
npm run lint
```

### 运行测试

```bash
# 单元测试
npm run test

# 端到端测试
npm run test:e2e
```

## 开发规范

- **组件命名**: 使用 PascalCase (如 `MainNav.vue`)
- **API函数命名**: 使用 camelCase (如 `getUserInfo`)
- **组件编写**: 使用 Composition API 和 `<script setup lang="ts">` 语法
- **状态管理**: 按业务域划分 Pinia store
- **样式编写**: 优先使用原子化 CSS 类，必要时使用 scoped CSS
- **路由权限**: 通过 meta 属性控制路由访问权限
- **类型定义**: 为所有 API 请求/响应创建 TypeScript 接口

## 路由说明

- **公共路由**: 路径以 `/` 开头，使用 `PublicLayout`
- **后台路由**: 路径以 `/admin` 开头，使用 `AdminLayout`，需要管理员权限
- **认证路由**: 在 meta 中设置 `requiresAuth: true`
- **角色控制**: 在 meta 中设置 `role: 'admin'` 或其他角色

## 环境变量

```env
# .env.development
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=舞动银龄 (开发)

# .env.production
VITE_API_BASE_URL=/api
VITE_APP_TITLE=舞动银龄
``` 