# 舞蹈艺术平台 2025 统一版本

这是舞蹈艺术平台2025年统一版本的前端项目，采用最新的Vue 3 + Vite技术栈构建。

## 技术栈

- **核心框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **UI框架**: Element Plus
- **HTTP请求**: Axios
- **CSS**: UnoCSS / 原子化CSS
- **代码规范**: ESLint + Prettier + Commitlint + Husky
- **测试工具**: Vitest + Cypress

## 项目结构

```
src/
├─ api/                    # 业务域 API 调用封装
├─ assets/                 # 静态资源
├─ components/
│   ├─ common/             # 通用组件
│   └─ specific/           # 业务专用组件
├─ layouts/                # 公共布局
├─ router/                 # 路由配置
├─ stores/                 # Pinia 状态管理
├─ utils/                  # 工具函数
├─ views/                  # 页面组件
│   ├─ public/             # 面向公众的页面
│   └─ admin/              # 后台管理页面
├─ style/                  # 全局样式
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

## 项目规范

- 组件文件使用 PascalCase 命名（如 `MainNav.vue`）
- API 函数使用 camelCase 命名（如 `getUserInfo`）
- 使用 Composition API 和 `<script setup>` 语法
- 统一使用 Element Plus 组件库
- 遵循 ESLint 和 Prettier 规范

## 目标用户

- 舞蹈学习者
- 舞蹈机构/工作室
- 康复教练
- 平台运营人员 