# 舞动银龄——基于多模态AI的舞蹈教学与反馈系统

<p align="center">
  <img src="public/fonticon.png" alt="舞动银龄" width="200">
</p>

<p align="center">
  <b>基于多模态AI的舞蹈教学与反馈系统，专为老年人设计的智能舞蹈学习平台</b>
</p>

## 项目简介

"舞动银龄"是一个专为中国老年人打造的舞蹈教学平台，基于多模态AI技术，结合了智能教学、实时反馈、社交互动与健康管理功能。平台充分考虑老年人的使用习惯和学习需求，提供简洁直观的界面和个性化的学习体验，帮助老年人通过舞蹈活动提升身心健康，同时传承和弘扬中国传统舞蹈文化。

## 技术栈

| 层级 | 前端 | 后端 |
|------|------|------|
| 核心框架 | Vue 3 (Composition API) | FastAPI |
| 构建工具 | Vite | - |
| 语言 | TypeScript | Python 3.8+ |
| 路由 | Vue Router 4 | - |
| 状态管理 | Pinia | - |
| UI组件 | Element Plus | - |
| CSS方案 | UnoCSS | - |
| HTTP客户端 | Axios | - |
| 数据库 | - | SQLAlchemy 2.0 ORM |
| 数据迁移 | - | Alembic |
| 数据验证 | - | Pydantic V2 |
| 测试 | Vitest, Cypress | Pytest |
| 代码质量 | ESLint, Prettier | Flake8, Black |
| 部署 | Docker | Docker |

## 项目结构

```
舞动银龄平台/
├── new-frontend/            # 统一前端项目
│   ├── src/                # 源代码目录
│   │   ├── api/           # API服务层
│   │   ├── assets/        # 静态资源
│   │   ├── components/    # 组件
│   │   │   ├── common/    # 通用组件
│   │   │   └── specific/  # 业务组件
│   │   ├── layouts/       # 布局组件
│   │   │   ├── PublicLayout.vue  # 公共页面布局
│   │   │   └── AdminLayout.vue   # 后台页面布局
│   │   ├── router/        # 路由配置
│   │   │   ├── index.ts   # 路由入口
│   │   │   ├── routes-public.ts  # 公共路由
│   │   │   └── routes-admin.ts   # 后台路由
│   │   ├── stores/        # Pinia状态管理
│   │   ├── style/         # 样式文件
│   │   ├── utils/         # 工具函数
│   │   ├── views/         # 页面组件
│   │   │   ├── public/    # 公共页面
│   │   │   └── admin/     # 后台页面
│   │   ├── App.vue        # 根组件
│   │   └── main.ts        # 入口文件
│   ├── public/            # 公共资源
│   └── vite.config.ts     # Vite配置
│
├── backend/               # 后端服务
│   ├── app/              # 应用主目录
│   │   ├── api/         # API路由
│   │   │   └── v1/      # API v1版本
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据模型 (SQLAlchemy ORM)
│   │   ├── repositories/ # 数据访问层
│   │   ├── schemas/     # 数据验证 (Pydantic)
│   │   └── services/    # 业务逻辑层
│   ├── alembic/          # 数据库迁移
│   ├── uploads/          # 文件上传目录
│   └── main.py           # 应用入口
│
└── docker-compose.yml    # Docker Compose配置
```

## 功能亮点

### 1. AI智能教练
- **实时动作评估**: 基于计算机视觉技术，分析用户舞蹈动作，提供即时反馈
- **个性化指导**: 根据用户水平和身体状况，调整教学难度和进度
- **虚拟示范**: 3D虚拟教练展示标准动作，多角度观看学习

### 2. 健康管理系统
- **健康数据追踪**: 记录运动量、心率、消耗热量等健康指标
- **个性化运动处方**: 基于用户身体状况，生成适合的舞蹈训练计划
- **风险评估**: 智能识别不适合的动作，预防运动伤害

### 3. 社交平台
- **舞蹈社区**: 用户可分享舞蹈视频、交流心得
- **挑战活动**: 定期举办线上舞蹈挑战，激励持续参与
- **成就系统**: 通过徽章、等级等方式，肯定用户进步

### 4. 非遗舞蹈传承
- **传统舞蹈库**: 收录各地区非物质文化遗产舞蹈
- **传承人讲解**: 非遗传承人视频讲解舞蹈文化背景和技巧
- **互动学习**: 通过简化版教学，让用户轻松学习传统舞蹈

## 快速开始

使用Docker Compose一键启动整个应用：

```bash
# 克隆仓库
git clone https://github.com/your-org/dance-platform.git
cd dance-platform

# 启动服务
docker-compose up -d
```

启动后访问:
- 前台网站: http://localhost:5173
- 后台管理: http://localhost:5173/admin
- API文档: http://localhost:8000/docs

## 许可证

本项目采用 MIT 许可证
