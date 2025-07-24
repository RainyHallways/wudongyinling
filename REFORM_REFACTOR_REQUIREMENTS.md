# 舞蹈艺术平台 2025 统一版本需求清单

> 本文档作为 **唯一权威** 的项目需求与技术实现依据，删除了历史上“主网站 + 后台管理”两套前端的分离描述，仅保留后端 API 及**已合并的统一前端**相关内容。

---

## 1. 项目总体概述

本项目定位为面向舞蹈学习者、舞蹈教育机构与健康管理服务提供者的综合性平台，核心目标包括：

1. 提供系统化、可视化的舞蹈课程与 AI 互动教学体验。
2. 基于健康数据的个性化训练与康复建议，帮助用户科学练舞、降低受伤风险。
3. 构建舞蹈社交与作品展示空间，促进舞蹈文化的传播与交流。
4. 为运营人员提供高效的内容、用户与数据管理工具，支持业务快速迭代。

**目标用户**：舞蹈学习者、舞蹈机构/工作室、康复教练、平台运营人员。

---

## 2. 技术栈概览（最终版）

| 层级 | 技术 | 采用理由 |
|------|------|---------|
| 后端 | **Python 3** / **FastAPI** / **SQLAlchemy** / **Alembic** / **Pydantic** | 性能优异、异步友好、生态丰富；ORM + 迁移保证数据一致性 |
| 前端 | **Vue 3 (Composition API)** / **Vite** / **Vue Router 4** / **Pinia** / **Axios** | 最新官方栈，开发体验佳，易于类型化与模块化 |
| UI 库 | **Element Plus** | 中文社区活跃、组件齐全、后台与 B 端场景契合 |
| CSS | **UnoCSS** *(或 TailwindCSS)* | 原子化 CSS、方便主题定制与响应式 |
| 质量保障 | **ESLint + Prettier + Commitlint + Husky** | 代码规范、提交钩子、统一格式 |
| 测试 | **Vitest + Cypress** | 单元 & 端到端测试 |

---

## 3. 后端 API 功能清单

| 模块 | 文件 | 主要职责 |
|------|------|---------|
| 用户认证 | `auth.py` | 登录/注册、JWT 签发、权限校验 |
| 用户管理 | `users.py` | 个人资料 CRUD、角色 & 状态管理 |
| 课程管理 | `courses.py` | 课程 CRUD、分类、进度、收藏 |
| 挑战活动 | `challenges.py` | 挑战发起、参与、排行统计 |
| AI 分析 | `ai_analysis.py` | 视频动作检测、评分、反馈 |
| 聊天服务 | `chat.py` | 用户与 AI/客服/教师实时或离线聊天 |
| 健康数据 | `health.py` | 体测数据、健康指标、风险评估 |
| 处方管理 | `prescriptions.py` | 个性化训练/康复处方创建与跟踪 |
| 统计报表 | `stats.py` | 活跃度、完成率、业务 KPI 汇总 |

> **接口契约**：所有接口遵循 RESTful 规范，统一返回 `{ code, message, data }` 结构，错误码详见《后端错误码手册》。

---

## 4. 统一前端项目需求

### 4.1 目录结构

```text
src/
├─ api/                    # 业务域 API 调用封装
├─ assets/                 # 静态资源
├─ components/
│   ├─ common/             # 通用组件
│   └─ specific/           # 业务专用组件
├─ layouts/                # 公共布局
│   ├─ PublicLayout.vue
│   └─ AdminLayout.vue
├─ router/
│   ├─ index.ts            # 路由注册入口
│   ├─ routes-public.ts    # 公共路由
│   └─ routes-admin.ts     # 后台路由
├─ stores/                 # Pinia modules
│   ├─ user.ts
│   ├─ dance.ts
│   ├─ health.ts
│   ├─ social.ts
│   └─ ...
├─ utils/
│   ├─ request.ts          # Axios 封装
│   └─ helpers.ts
├─ views/
│   ├─ public/             # 面向公众的页面
│   │   ├─ Home.vue
│   │   ├─ About.vue
│   │   ├─ DanceCourses.vue
│   │   ├─ AICoach.vue
│   │   ├─ HealthManagement.vue
│   │   ├─ SocialPlatform.vue
│   │   ├─ Contact.vue
│   │   ├─ FAQ.vue
│   │   ├─ Login.vue
│   │   └─ policy/
│   │       ├─ OriginalLicenseAgreement.vue
│   │       ├─ UserAgreement.vue
│   │       ├─ UserOriginalityGuarantee.vue
│   │       └─ PrivacyPolicy.vue
│   └─ admin/              # 后台页面
│       ├─ Dashboard.vue
│       ├─ UserManagement.vue
│       ├─ CourseManagement.vue
│       ├─ ChallengeManagement.vue
│       ├─ HealthRecords.vue
│       ├─ PrescriptionManagement.vue
│       └─ Login.vue
├─ style/
│   ├─ index.css
│   └─ variables.scss
├─ App.vue
└─ main.ts
```

### 4.2 路由设计

* **公共路由**（`routes-public.ts`）：根路径 `/`，统一使用 `PublicLayout`。
* **后台路由**（`routes-admin.ts`）：前缀 `/admin`，统一使用 `AdminLayout`，并携带 `meta: { requiresAuth: true, role: 'admin' }`。
* **路由守卫**：在 `router/index.ts` 中实现 `beforeEach`，验证 `token` 和 `roles`，无权限时重定向到 `/login` 或首页。

### 4.3 状态管理（Pinia）

| Store | State | Actions | 说明 |
|-------|-------|---------|------|
| `user` | `token`, `userInfo`, `roles` | `login`, `logout`, `getUserInfo` | 同时支持普通用户与管理员登录场景 |
| `dance` | 课程列表、收藏、进度 | `fetchCourses`, `updateProgress` | |
| `health` | 健康指标、图表数据 | `fetchHealthData` | |
| `social` | 动态、评论、点赞 | `fetchFeeds`, `postComment` | |
| 其他 | 依业务增长按领域拆分 | | |

### 4.4 API 服务层

* **`utils/request.ts`**：封装 Axios，自动注入 `Bearer token`，统一处理 `401`、业务错误码。
* **`api/`**：按后端模块拆分（`user.ts`, `course.ts`, `health.ts`, `challenge.ts`, `prescription.ts` 等），每个文件暴露函数与后端路径一一对应。

### 4.5 组件与页面迁移

* **可复用组件**：`AppFooter`, `MainNav`, `PageHeader` 等迁移至 `components/common/`，适配 Element Plus。
* **页面映射**：详见下表。

| 原始路径 | 新路径 | 模块 | 备注 |
|---|---|---|---|
| `admin/src/views/dashboard/index.vue` | `src/views/admin/Dashboard.vue` | Admin | 适配新布局 |
| `src/views/Home.vue` | `src/views/public/Home.vue` | Public | |
| *...其余同类映射省略，遵循目录结构即可* |  |  |  |

---

## 5. 开发流程与里程碑

| 阶段 | 主要任务 | 预估时长 |
|------|----------|---------|
| 初始化 | Vite + Element Plus + Pinia + Router 脚手架；CI/CD；代码规范 | 1 周 |
| 基础功能 | 实现公共/后台布局、路由守卫、`user` store、登录/注册 | 1–2 周 |
| 核心模块 | 课程、AI 教练、健康、挑战等主要页面与 API 对接 | 3–4 周 |
| 后台功能 | Dashboard、用户/课程/处方管理、数据可视化 | 3 周 |
| 测试与优化 | 单元测试、E2E、性能优化、可访问性检查 | 1–2 周 |
| 发布 | 容器化部署、灰度发布、监控告警 | 1 周 |

> **交付标准**：所有 PR 通过 CI，测试覆盖率 ≥ 80%，主要页面 Lighthouse 分数 ≥ 90。

---

## 6. 风险与注意事项

1. **角色权限**：需与后端统一角色枚举与权限点，避免前后端不一致。
2. **SEO vs SPA**：若对 SEO 有硬需求，可考虑 SSR / SSG；当前方案默认 CSR。
3. **多端适配**：移动端适配采用 `rem` 或 `viewport` + 原子化 CSS；后台可优先保证桌面端体验。
4. **AI 分析性能**：前端需异步轮询/Socket 获取 AI 评估结果，避免长时间阻塞。

---

> **后续行动**：确认本需求清单后，立即开设 Git 仓、创建看板、冻结技术栈，进入迭代开发。 