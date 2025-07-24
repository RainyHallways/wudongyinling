# 舞蹈艺术平台 2025 重构需求清单

## 1. 项目总体概述

本项目旨在构建一个面向舞蹈学习者、舞蹈教育机构以及健康管理服务提供者的综合性平台，核心价值包括：

1. 为大众用户提供系统化、可视化的舞蹈课程与 AI 互动教学体验。
2. 提供基于健康数据的个性化训练与康复建议，帮助用户科学练舞、降低受伤风险。
3. 构建舞蹈社交与作品展示空间，促进舞蹈文化的传播与交流。
4. 为后台运营人员提供高效便捷的内容与用户管理工具，支持业务快速迭代。

目标用户：舞蹈学习者、舞蹈工作室/机构、康复教练、平台运营人员。

---

## 2. 技术栈分析

| 模块 | 主要技术 | 说明 |
|------|----------|------|
| 后端 API | **Python 3**, **FastAPI**, **SQLAlchemy**, **Alembic**, **Pydantic**, **Uvicorn/Gunicorn** | 提供 RESTful 接口与业务逻辑，使用 SQLAlchemy + Alembic 进行 ORM 与迁移管理。 |
| 主网站前端 (public) | **Vue 3**, **Vite**, **Vue-Router**, **Pinia**, **CSS/SCSS** | 面向公众的营销与功能页，静态资源位于根目录 `src`。 |
| 后台管理前端 (admin) | **Vue 3**, **Vite**, **Vue-Router**, **Pinia**, **CSS/SCSS** | 面向运营人员的后台管理系统，代码位于 `admin/src`。 |

> 两个前端项目技术栈基本一致，后端服务独立，对外暴露统一 API。

---

## 3. 功能模块分析

### 3.1 后端 API (`backend/app/api/v1/`)

| 文件 | 推断功能 | 说明 |
|------|----------|------|
| `auth.py` | 用户注册、登录、权限验证 | JWT/Token 管理、权限装饰器等 |
| `users.py` | 用户资料增删改查 | 个人信息、角色、状态管理 |
| `courses.py` | 课程管理 | 课程 CRUD、分类、进度、收藏 |
| `challenges.py` | 挑战/打卡模块 | 发起挑战、参与、排行 |
| `ai_analysis.py` | AI 动作分析 | 上传视频/动作检测、评分与反馈 |
| `chat.py` | 实时/离线聊天 | 用户与 AI/客服/教师沟通接口 |
| `health.py` | 健康数据接口 | 体测数据、活动记录、风险评估 |
| `prescriptions.py` | 训练/康复处方 | 生成与跟踪个性处方计划 |
| `stats.py` | 统计与报表 | 用户活跃度、课程完成率等汇总 |

### 3.2 主网站前端 (`src/views`)

| 页面 | 作用 |
|-------|------|
| `Home.vue` | 首页、品牌与平台介绍 |
| `DanceCourses.vue` | 舞蹈课程目录与详情 |
| `AICoach.vue` | AI 教练互动页面 |
| `HealthManagement.vue` | 健康管理与数据看板 |
| `SocialPlatform.vue` | 社交广场/作品分享 |
| `About.vue` | 关于我们 |
| `Contact.vue` | 联系方式 |
| `FAQ.vue` | 常见问题 |
| `Login.vue` | 用户登录/注册 |
| `OriginalLicenseAgreement.vue`, `UserAgreement.vue`, `UserOriginalityGuarantee.vue`, `PrivacyPolicy.vue` | 法律与合规相关页面 |
| `NotFound.vue` | 404 页面 |

### 3.3 后台管理前端 (`admin/src/views`)

| 页面 | 作用 |
|-------|------|
| `dashboard/index.vue` | 后台仪表盘，总览关键指标 |
| `users/index.vue` | 用户管理：查询、编辑、禁用 |
| `courses/index.vue` | 课程管理：新建、编辑、发布 |
| `challenges/index.vue` | 挑战管理：配置、审核、统计 |
| `health-records/index.vue` | 健康记录审查与干预 |
| `prescriptions/index.vue` | 处方管理：创建、分配、跟进 |
| `login/index.vue` | 后台登录 |

---

## 4. 重构目标

1. **统一前端代码基线**：将现有的 *主网站* 与 *后台管理* 两套 Vue 项目合并为 **单一 Vue 3 Mono-Repo**，共享构建、依赖与复用组件。
2. **隔离业务领域**：通过命名空间路由（如 `/admin/**` 与 `/`）或子应用模式清晰区分 **Admin** 与 **Public** 视图。
3. **保持与后端解耦**：统一 `utils/request.ts` (Axios 封装) 与 API 调用层，保证前端替换部署不影响 FastAPI 服务。
4. **组件与状态复用**：提取通用 UI 组件与 Pinia Store（如 `user`, `notification`），减少重复实现。
5. **优化 CI/CD**：单一前端产物更易于持续集成与容器化部署，减少 DevOps 复杂度。

---

## 5. 统一前端项目设计建议

### 5.1 推荐目录结构

```text
src/
├─ assets/                # 静态资源
├─ components/            # 通用组件库
├─ layouts/               # 公共布局 (AdminLayout / PublicLayout)
├─ router/
│   ├─ index.ts           # 路由入口
│   ├─ routes-public.ts   # 公网路由表
│   └─ routes-admin.ts    # 后台路由表
├─ stores/                # Pinia modules
│   ├─ index.ts           # store 注册入口
│   ├─ user.ts            # 统一用户状态
│   └─ ...
├─ views/
│   ├─ public/            # 面向公众的页面
│   │   ├─ Home.vue
│   │   ├─ DanceCourses.vue
│   │   └─ ...
│   └─ admin/             # 后台页面
│       ├─ Dashboard.vue
│       ├─ Users.vue
│       └─ ...
├─ utils/
│   ├─ request.ts         # Axios 封装
│   └─ ...
├─ style/                 # 全局样式/设计系统
├─ App.vue
└─ main.ts
```

**设计要点：**

1. 使用 **布局组件** (`PublicLayout`, `AdminLayout`) 统一导航与外观，同时通过 `defineAsyncComponent` 懒加载非活跃模块。
2. 路由分层：顶层 `index.ts` 只负责注入公共守卫与全局配置，实际路由细节拆分至 `routes-public.ts` 与 `routes-admin.ts`，互不影响。
3. Pinia `stores/` 采用 **领域分包** (user / course / health / misc)，保持业务聚合与可维护性。
4. 统一 `utils/request.ts` + `env` 配置，实现 **后端 API Base URL** 按环境注入。
5. 将通用 CSS/变量放在 `style/`，结合 PostCSS 或 Tailwind 配置保证风格统一。

### 5.2 关键待整合模块

| 模块 | 现状 | 合并策略 |
|------|------|---------|
| `router/index.js` | 两套前端各自维护 | 合并为单一路由入口，使用子路由或命名空间区分 Admin/Public |
| `stores/user.js` | 两套前端重复 | 抽象公共用户状态，加入角色与权限字段以便前端鉴权 |
| `utils/request.js` | Axios 封装重复 | 提取到根级统一实现，支持拦截器注入 Token 与错误处理 |
| 主题样式 / 组件库 | 风格不一 | 建议引入设计系统 (如 UnoCSS/Tailwind + 自定义主题) 并使用 Storybook 维护组件资产 |
| 登录 / 权限逻辑 | 代码分散于各项目 | 统一权限中间件：路由守卫 + 组件指令 + API Error 处理 |

---

> **下一步**：基于上述需求清单，拟定详细的任务拆分（Roadmap）、时程与人员分工；确定技术选型（如 UI 库、组件规范）后开始重构实施。 