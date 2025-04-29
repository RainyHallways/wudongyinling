# 舞动银龄 - 老年人舞蹈教学平台

<p align="center">
  <img src="public/fonticon.png" alt="舞动银龄" width="200">
</p>

<p align="center">
  <b>一个专为老年人设计的智能舞蹈教学平台</b>
</p>

## 项目简介

"舞动银龄"是一个专为中国老年人打造的舞蹈教学平台，结合了AI智能教学、社交互动与健康管理功能。平台充分考虑老年人的使用习惯和学习需求，提供简洁直观的界面和个性化的学习体验，帮助老年人通过舞蹈活动提升身心健康。

## 关键功能

- **智能AI教练**：采用AI视频分析技术，实时评估用户舞蹈动作，提供个性化指导和改进建议
- **多样化舞蹈课程**：提供广场舞、太极、民族舞、交谊舞、健身操等多种适合老年人的舞蹈课程
- **社交激励系统**：用户可以分享舞蹈视频、参与打卡挑战、加入社区活动，增强社交互动
- **健康数据管理**：记录运动数据，根据身体状况生成个性化运动处方和训练计划
- **非遗舞蹈传承**：收录非物质文化遗产舞蹈内容，帮助传统文化传承与弘扬

## 无障碍设计特点

平台特别关注老年用户的无障碍需求，具有以下特色：

- 最小字体设置为18px，确保文字清晰可读
- 高对比度色彩方案，方便视力减退的老年人识别
- 简化的导航结构和大尺寸交互元素，提高操作便捷性
- 圆角按钮设计，减少视觉压力
- 响应式布局，适配各种设备屏幕大小
- 直观的图标设计，配合文字说明，降低学习门槛

## 技术栈

### 前端
- **前端框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **UI组件库**: Element Plus
- **路由管理**: Vue Router
- **状态管理**: Pinia
- **图表可视化**: ECharts
- **HTTP请求**: Axios
- **样式处理**: SCSS

### 后端
- **开发语言**: Python 3.8+
- **Web框架**: FastAPI
- **数据库**: MySQL 8.0+
- **ORM**: SQLAlchemy
- **数据迁移**: Alembic
- **缓存**: Redis
- **API文档**: Swagger/ReDoc

### 后台管理系统
- **框架**: Vue 3
- **构建工具**: Vite
- **UI组件库**: Element Plus
- **状态管理**: Pinia
- **HTTP客户端**: Axios

## 项目结构

```
├── admin/                  # 后台管理系统
│   ├── src/               # 源代码目录
│   │   ├── api/          # API请求
│   │   ├── components/   # 公共组件
│   │   ├── layouts/      # 布局组件
│   │   ├── router/       # 路由配置
│   │   ├── stores/       # 状态管理
│   │   ├── styles/       # 样式文件
│   │   └── views/        # 页面组件
│   └── vite.config.js     # Vite配置
├── backend/               # 后端服务
│   ├── app/              # 应用主目录
│   │   ├── api/         # API路由
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据模型
│   │   └── schemas/     # 数据验证
│   ├── alembic/          # 数据库迁移
│   └── main.py           # 应用入口
├── public/                # 静态资源
│   └── images/           # 图片资源
├── src/                   # 前端源代码
│   ├── components/       # 通用组件
│   │   ├── AppFooter.vue # 页脚组件
│   │   ├── MainNav.vue   # 主导航
│   │   └── PageHeader.vue # 页头组件
│   ├── router/           # 路由配置
│   ├── stores/           # Pinia状态管理
│   ├── styles/           # 样式文件
│   │   └── main.css      # 主样式表
│   ├── utils/            # 工具函数
│   ├── views/            # 页面组件
│   │   ├── AICoach.vue   # AI教练页面
│   │   ├── About.vue     # 关于我们
│   │   ├── DanceCourses.vue # 舞蹈课程
│   │   ├── HealthManagement.vue # 健康管理
│   │   ├── Home.vue      # 首页
│   │   ├── Login.vue     # 登录页
│   │   ├── NotFound.vue  # 404页面
│   │   └── SocialPlatform.vue # 社交平台
│   ├── App.vue           # 根组件
│   ├── main.js           # 入口文件
│   └── style.css         # 全局样式
└── package.json          # 项目配置
```

## 开发环境设置

### 前端
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

### 后端
```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env

# 初始化数据库
python reset_db.py
alembic upgrade head

# 启动服务
uvicorn main:app --reload
```

### 后台管理系统
```bash
cd admin

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

## Docker 镜像管理

### 构建镜像 (wdyl_app)

确保你的 Docker 环境已启动。在项目根目录下（包含 `Dockerfile` 的目录），运行以下命令来构建名为 `wdyl_app` 的 Docker 镜像：

```bash
docker build -t wdyl_app .
```
这个命令会根据 `Dockerfile` 的指令构建镜像，并将其标记为 `wdyl_app:latest`。

**(可选) 使用 Docker Compose 构建:**

你也可以使用 `docker-compose` 来构建镜像。默认情况下，这会构建 `app` 服务的镜像，但名称可能不是 `wdyl_app` (例如，可能是 `websites_app`，取决于你的项目目录名)。

```bash
docker-compose build app
```
若想让 `docker-compose build` 也生成名为 `wdyl_app` 的镜像，你需要在 `docker-compose.yml` 文件中为 `app` 服务添加 `image: wdyl_app` 指令。

### 导出镜像

将已构建的 `wdyl_app` 镜像导出为 tar 文件：

```bash
docker save -o wdyl_app.tar wdyl_app:latest
```
这将创建一个名为 `wdyl_app.tar` 的文件，其中包含你的 Docker 镜像。

### 导入镜像

在另一台机器或环境中，你可以使用以下命令从 tar 文件加载镜像：

```bash
docker load -i wdyl_app.tar
```
导入成功后，你可以通过 `docker images | grep wdyl_app` 来查看已导入的镜像。

### 运行容器

使用以下命令以后台模式运行名为 `wdyl_website` 的容器，并将宿主机的 5173 端口映射到容器的 80 端口：

```bash
docker run -d --name wdyl_website -p 5173:80 wdyl_app:latest
```

运行成功后，你可以通过访问 `http://localhost:5173` 来访问前端应用，API 则通过 `http://localhost:5173/api` 访问。

**(注意)** 如果你使用 `docker-compose up -d` 来启动服务，它会根据 `docker-compose.yml` 中的配置来运行容器（包括端口映射），而不是使用上面的 `docker run` 命令。

## 浏览器兼容性

- Chrome (最新版本)
- Firefox (最新版本)
- Safari (最新版本)
- Edge (最新版本)
- IE 不支持

## 贡献指南

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request
