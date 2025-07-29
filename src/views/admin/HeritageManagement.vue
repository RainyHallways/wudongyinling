<template>
  <div class="heritage-management">
    <PageHeader title="非遗传承管理" subtitle="管理非物质文化遗产项目和传承人" />
    
    <!-- 功能选项卡 -->
    <el-tabs v-model="activeTab" type="card">
      <!-- 非遗项目管理 -->
      <el-tab-pane label="非遗项目" name="projects">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>非遗项目列表</span>
              <el-button type="primary" @click="showAddProject = true">
                <el-icon><Plus /></el-icon>
                添加项目
              </el-button>
            </div>
          </template>
          
          <!-- 项目筛选 -->
          <el-row :gutter="20" class="filter-row">
            <el-col :span="6">
              <el-input v-model="projectFilters.keyword" placeholder="搜索项目名称" clearable>
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </el-col>
            <el-col :span="4">
              <el-select v-model="projectFilters.category" placeholder="项目类别" clearable>
                <el-option label="舞蹈" value="dance" />
                <el-option label="音乐" value="music" />
                <el-option label="戏曲" value="opera" />
                <el-option label="技艺" value="craft" />
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-select v-model="projectFilters.level" placeholder="保护级别" clearable>
                <el-option label="国家级" value="national" />
                <el-option label="省级" value="provincial" />
                <el-option label="市级" value="municipal" />
                <el-option label="县级" value="county" />
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-select v-model="projectFilters.status" placeholder="状态" clearable>
                <el-option label="启用" value="active" />
                <el-option label="停用" value="inactive" />
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-button type="primary" @click="searchProjects">查询</el-button>
              <el-button @click="resetProjectFilters">重置</el-button>
            </el-col>
          </el-row>

          <!-- 项目表格 -->
          <el-table :data="projects" v-loading="projectLoading" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column label="项目信息" width="300">
              <template #default="{ row }">
                <div class="project-info">
                  <img v-if="row.cover_image" :src="row.cover_image" class="project-cover" />
                  <div class="project-details">
                    <div class="project-name">{{ row.name }}</div>
                    <div class="project-origin">{{ row.origin_location }}</div>
                    <el-tag :type="getCategoryTagType(row.category)" size="small">
                      {{ getCategoryText(row.category) }}
                    </el-tag>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
            <el-table-column label="保护级别" width="100">
              <template #default="{ row }">
                <el-tag :type="getLevelTagType(row.level)">
                  {{ getLevelText(row.level) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="传承人" width="120">
              <template #default="{ row }">
                {{ row.inheritor?.name || '暂无' }}
              </template>
            </el-table-column>
            <el-table-column label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'danger'">
                  {{ row.is_active ? '启用' : '停用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180" />
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button-group>
                  <el-button size="small" @click="viewProject(row)">查看</el-button>
                  <el-button size="small" type="primary" @click="editProject(row)">编辑</el-button>
                  <el-button 
                    size="small" 
                    :type="row.is_active ? 'warning' : 'success'"
                    @click="toggleProjectStatus(row)"
                  >
                    {{ row.is_active ? '停用' : '启用' }}
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteProject(row)">删除</el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="projectPagination.page"
              v-model:page-size="projectPagination.size"
              :page-sizes="[10, 20, 50]"
              :total="projectPagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleProjectSizeChange"
              @current-change="handleProjectCurrentChange"
            />
          </div>
        </el-card>
      </el-tab-pane>

      <!-- 传承人管理 -->
      <el-tab-pane label="传承人" name="inheritors">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>传承人列表</span>
              <el-button type="primary" @click="showAddInheritor = true">
                <el-icon><Plus /></el-icon>
                添加传承人
              </el-button>
            </div>
          </template>
          
          <!-- 传承人筛选 -->
          <el-row :gutter="20" class="filter-row">
            <el-col :span="6">
              <el-input v-model="inheritorFilters.keyword" placeholder="搜索传承人姓名" clearable>
                <template #prefix>
                  <el-icon><Search /></el-icon>
                </template>
              </el-input>
            </el-col>
            <el-col :span="4">
              <el-input v-model="inheritorFilters.hometown" placeholder="籍贯" clearable />
            </el-col>
            <el-col :span="4">
              <el-select v-model="inheritorFilters.gender" placeholder="性别" clearable>
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-col>
            <el-col :span="4">
              <el-select v-model="inheritorFilters.status" placeholder="状态" clearable>
                <el-option label="启用" value="active" />
                <el-option label="停用" value="inactive" />
              </el-select>
            </el-col>
            <el-col :span="6">
              <el-button type="primary" @click="searchInheritors">查询</el-button>
              <el-button @click="resetInheritorFilters">重置</el-button>
            </el-col>
          </el-row>

          <!-- 传承人表格 -->
          <el-table :data="inheritors" v-loading="inheritorLoading" style="width: 100%">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column label="基本信息" width="200">
              <template #default="{ row }">
                <div class="inheritor-info">
                  <el-avatar :src="row.avatar" :size="50">
                    {{ row.name[0] }}
                  </el-avatar>
                  <div class="inheritor-details">
                    <div class="inheritor-name">{{ row.name }}</div>
                    <div class="inheritor-meta">
                      {{ getGenderText(row.gender) }} 
                      <span v-if="row.birth_year">| {{ new Date().getFullYear() - row.birth_year }}岁</span>
                    </div>
                    <div class="inheritor-hometown">{{ row.hometown }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="specialty" label="专长" min-width="150" show-overflow-tooltip />
            <el-table-column prop="biography" label="个人简介" min-width="200" show-overflow-tooltip />
            <el-table-column label="项目数量" width="100">
              <template #default="{ row }">
                {{ row.projects?.length || 0 }}
              </template>
            </el-table-column>
            <el-table-column label="状态" width="80">
              <template #default="{ row }">
                <el-tag :type="row.is_active ? 'success' : 'danger'">
                  {{ row.is_active ? '启用' : '停用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="created_at" label="创建时间" width="180" />
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button-group>
                  <el-button size="small" @click="viewInheritor(row)">查看</el-button>
                  <el-button size="small" type="primary" @click="editInheritor(row)">编辑</el-button>
                  <el-button 
                    size="small" 
                    :type="row.is_active ? 'warning' : 'success'"
                    @click="toggleInheritorStatus(row)"
                  >
                    {{ row.is_active ? '停用' : '启用' }}
                  </el-button>
                  <el-button size="small" type="danger" @click="deleteInheritor(row)">删除</el-button>
                </el-button-group>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="inheritorPagination.page"
              v-model:page-size="inheritorPagination.size"
              :page-sizes="[10, 20, 50]"
              :total="inheritorPagination.total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleInheritorSizeChange"
              @current-change="handleInheritorCurrentChange"
            />
          </div>
        </el-card>
      </el-tab-pane>
    </el-tabs>

    <!-- 添加/编辑项目弹窗 -->
    <el-dialog 
      v-model="showAddProject" 
      :title="editingProject ? '编辑项目' : '添加项目'" 
      width="800px"
    >
      <el-form :model="projectForm" :rules="projectRules" ref="projectFormRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="项目名称" prop="name">
              <el-input v-model="projectForm.name" placeholder="请输入项目名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="发源地" prop="origin_location">
              <el-input v-model="projectForm.origin_location" placeholder="请输入发源地" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="项目类别" prop="category">
              <el-select v-model="projectForm.category" placeholder="请选择类别">
                <el-option label="舞蹈" value="dance" />
                <el-option label="音乐" value="music" />
                <el-option label="戏曲" value="opera" />
                <el-option label="技艺" value="craft" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="保护级别" prop="level">
              <el-select v-model="projectForm.level" placeholder="请选择保护级别">
                <el-option label="国家级" value="national" />
                <el-option label="省级" value="provincial" />
                <el-option label="市级" value="municipal" />
                <el-option label="县级" value="county" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="项目描述" prop="description">
          <el-input 
            v-model="projectForm.description" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入项目描述" 
          />
        </el-form-item>
        <el-form-item label="历史背景">
          <el-input 
            v-model="projectForm.history" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入历史背景" 
          />
        </el-form-item>
        <el-form-item label="特色特点">
          <el-input 
            v-model="projectForm.characteristics" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入特色特点" 
          />
        </el-form-item>
        <el-form-item label="传承人">
          <el-select v-model="projectForm.inheritor_id" placeholder="选择传承人" clearable>
            <el-option 
              v-for="inheritor in inheritors" 
              :key="inheritor.id" 
              :label="inheritor.name" 
              :value="inheritor.id" 
            />
          </el-select>
        </el-form-item>
        <el-form-item label="封面图片">
          <el-input v-model="projectForm.cover_image" placeholder="图片URL" />
        </el-form-item>
        <el-form-item label="视频链接">
          <el-input v-model="projectForm.video_url" placeholder="视频URL" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showAddProject = false">取消</el-button>
        <el-button type="primary" @click="saveProject">保存</el-button>
      </template>
    </el-dialog>

    <!-- 添加/编辑传承人弹窗 -->
    <el-dialog 
      v-model="showAddInheritor" 
      :title="editingInheritor ? '编辑传承人' : '添加传承人'" 
      width="600px"
    >
      <el-form :model="inheritorForm" :rules="inheritorRules" ref="inheritorFormRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="inheritorForm.name" placeholder="请输入姓名" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-select v-model="inheritorForm.gender" placeholder="请选择性别">
                <el-option label="男" value="male" />
                <el-option label="女" value="female" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="出生年份">
              <el-date-picker 
                v-model="inheritorForm.birth_year" 
                type="year" 
                placeholder="选择出生年份"
                value-format="YYYY"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="籍贯" prop="hometown">
              <el-input v-model="inheritorForm.hometown" placeholder="请输入籍贯" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="专长" prop="specialty">
          <el-input v-model="inheritorForm.specialty" placeholder="请输入专长" />
        </el-form-item>
        <el-form-item label="个人简介">
          <el-input 
            v-model="inheritorForm.biography" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入个人简介" 
          />
        </el-form-item>
        <el-form-item label="主要成就">
          <el-input 
            v-model="inheritorForm.achievements" 
            type="textarea" 
            :rows="3" 
            placeholder="请输入主要成就" 
          />
        </el-form-item>
        <el-form-item label="头像">
          <el-input v-model="inheritorForm.avatar" placeholder="头像URL" />
        </el-form-item>
        <el-form-item label="联系方式">
          <el-input v-model="inheritorForm.contact_info" placeholder="联系方式" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showAddInheritor = false">取消</el-button>
        <el-button type="primary" @click="saveInheritor">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import PageHeader from '@/components/common/PageHeader.vue'

// 接口定义
interface HeritageProject {
  id: number
  name: string
  description: string
  origin_location: string
  category: string
  level: string
  cover_image?: string
  video_url?: string
  history?: string
  characteristics?: string
  inheritor_id?: number
  inheritor?: HeritageInheritor
  is_active: boolean
  created_at: string
}

interface HeritageInheritor {
  id: number
  name: string
  gender: string
  birth_year?: number
  hometown: string
  specialty: string
  biography?: string
  achievements?: string
  avatar?: string
  contact_info?: string
  is_active: boolean
  projects?: HeritageProject[]
  created_at: string
}

// 响应式数据
const activeTab = ref('projects')
const projectLoading = ref(false)
const inheritorLoading = ref(false)
const projects = ref<HeritageProject[]>([])
const inheritors = ref<HeritageInheritor[]>([])
const showAddProject = ref(false)
const showAddInheritor = ref(false)
const editingProject = ref<HeritageProject | null>(null)
const editingInheritor = ref<HeritageInheritor | null>(null)

// 筛选条件
const projectFilters = reactive({
  keyword: '',
  category: '',
  level: '',
  status: ''
})

const inheritorFilters = reactive({
  keyword: '',
  hometown: '',
  gender: '',
  status: ''
})

// 分页
const projectPagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

const inheritorPagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 表单数据
const projectForm = reactive({
  name: '',
  description: '',
  origin_location: '',
  category: '',
  level: '',
  cover_image: '',
  video_url: '',
  history: '',
  characteristics: '',
  inheritor_id: null as number | null
})

const inheritorForm = reactive({
  name: '',
  gender: '',
  birth_year: null as number | null,
  hometown: '',
  specialty: '',
  biography: '',
  achievements: '',
  avatar: '',
  contact_info: ''
})

// 表单验证规则
const projectRules = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  origin_location: [{ required: true, message: '请输入发源地', trigger: 'blur' }],
  category: [{ required: true, message: '请选择项目类别', trigger: 'change' }],
  level: [{ required: true, message: '请选择保护级别', trigger: 'change' }],
  description: [{ required: true, message: '请输入项目描述', trigger: 'blur' }]
}

const inheritorRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  hometown: [{ required: true, message: '请输入籍贯', trigger: 'blur' }],
  specialty: [{ required: true, message: '请输入专长', trigger: 'blur' }]
}

// 辅助函数
const getCategoryText = (category: string) => {
  const map: Record<string, string> = {
    dance: '舞蹈',
    music: '音乐',
    opera: '戏曲',
    craft: '技艺'
  }
  return map[category] || category
}

const getCategoryTagType = (category: string) => {
  const map: Record<string, string> = {
    dance: 'success',
    music: 'primary',
    opera: 'warning',
    craft: 'info'
  }
  return map[category] || ''
}

const getLevelText = (level: string) => {
  const map: Record<string, string> = {
    national: '国家级',
    provincial: '省级',
    municipal: '市级',
    county: '县级'
  }
  return map[level] || level
}

const getLevelTagType = (level: string) => {
  const map: Record<string, string> = {
    national: 'danger',
    provincial: 'warning',
    municipal: 'primary',
    county: 'info'
  }
  return map[level] || ''
}

const getGenderText = (gender: string) => {
  return gender === 'male' ? '男' : '女'
}

// 项目相关方法
const loadProjects = async () => {
  projectLoading.value = true
  try {
    const response = await fetch(`/v1/social/heritage/projects?${new URLSearchParams({
      skip: ((projectPagination.page - 1) * projectPagination.size).toString(),
      limit: projectPagination.size.toString(),
      ...(projectFilters.keyword && { keyword: projectFilters.keyword }),
      ...(projectFilters.category && { category: projectFilters.category }),
      ...(projectFilters.level && { level: projectFilters.level }),
      ...(projectFilters.status && { is_active: projectFilters.status === 'active' ? 'true' : 'false' })
    })}`)
    
    if (!response.ok) {
      throw new Error('获取项目列表失败')
    }
    
    const data = await response.json()
    projects.value = data.data || []
    projectPagination.total = data.total || 0
  } catch (error) {
    ElMessage.error('加载项目列表失败')
    // 回退到模拟数据
    projects.value = [
      {
        id: 1,
        name: '傣族孔雀舞',
        description: '傣族孔雀舞是傣族民间舞蹈的一种，是最受群众喜爱的传统表演性舞蹈。',
        origin_location: '云南西双版纳',
        category: 'dance',
        level: 'national',
        cover_image: '/images/傣族孔雀舞图片.png',
        video_url: '',
        history: '孔雀舞历史悠久，早在一千多年前就在民间广泛流传...',
        characteristics: '舞蹈动作优美，形象生动，富有雕塑性...',
        inheritor_id: 1,
        inheritor: {
          id: 1,
          name: '杨丽萍',
          gender: 'female',
          birth_year: 1958,
          hometown: '云南大理',
          specialty: '傣族孔雀舞',
          is_active: true,
          created_at: '2024-01-01 00:00:00'
        },
        is_active: true,
        created_at: '2024-01-01 09:00:00'
      },
      {
        id: 2,
        name: '安代舞',
        description: '安代舞是蒙古族民间集体舞蹈，流传在内蒙古科尔沁草原等地区。',
        origin_location: '内蒙古通辽',
        category: 'dance',
        level: 'national',
        cover_image: '/images/安代舞图片.png',
        video_url: '',
        history: '安代舞起源于明末清初，最初是一种治病的萨满教舞蹈...',
        characteristics: '舞蹈节奏明快，动作简单易学，具有浓厚的生活气息...',
        inheritor_id: 2,
        inheritor: {
          id: 2,
          name: '包布和',
          gender: 'male',
          birth_year: 1960,
          hometown: '内蒙古通辽',
          specialty: '安代舞',
          is_active: true,
          created_at: '2024-01-01 00:00:00'
        },
        is_active: true,
        created_at: '2024-01-01 09:00:00'
      },
      {
        id: 3,
        name: '藏族锅庄舞',
        description: '锅庄舞是藏族的民间舞蹈，在节庆活动中表演，是藏族文化的重要组成部分。',
        origin_location: '西藏拉萨',
        category: 'dance',
        level: 'national',
        cover_image: '/images/藏族锅庄舞图片.png',
        video_url: '',
        history: '锅庄舞历史悠久，起源于古代藏族祭祀活动...',
        characteristics: '舞蹈队形变化丰富，男女分组对舞，动作优美大方...',
        inheritor_id: 3,
        inheritor: {
          id: 3,
          name: '次旺多吉',
          gender: 'male',
          birth_year: 1955,
          hometown: '西藏拉萨',
          specialty: '藏族锅庄舞',
          is_active: true,
          created_at: '2024-01-01 00:00:00'
        },
        is_active: true,
        created_at: '2024-01-01 09:00:00'
      }
    ]
    projectPagination.total = 3
  } finally {
    projectLoading.value = false
  }
}

const loadInheritors = async () => {
  inheritorLoading.value = true
  try {
    // TODO: 调用API
    // 模拟数据
    inheritors.value = [
      {
        id: 1,
        name: '杨丽萍',
        gender: 'female',
        birth_year: 1958,
        hometown: '云南大理',
        specialty: '傣族孔雀舞',
        biography: '中国著名舞蹈艺术家，被誉为"孔雀公主"...',
        achievements: '创作了《雀之灵》、《月光》等经典作品...',
        avatar: '',
        contact_info: '',
        is_active: true,
        projects: [],
        created_at: '2024-01-01 09:00:00'
      }
    ]
    inheritorPagination.total = 1
  } catch (error) {
    ElMessage.error('加载传承人列表失败')
  } finally {
    inheritorLoading.value = false
  }
}

const searchProjects = () => {
  projectPagination.page = 1
  loadProjects()
}

const resetProjectFilters = () => {
  Object.assign(projectFilters, {
    keyword: '',
    category: '',
    level: '',
    status: ''
  })
  searchProjects()
}

const searchInheritors = () => {
  inheritorPagination.page = 1
  loadInheritors()
}

const resetInheritorFilters = () => {
  Object.assign(inheritorFilters, {
    keyword: '',
    hometown: '',
    gender: '',
    status: ''
  })
  searchInheritors()
}

const viewProject = (project: HeritageProject) => {
  // TODO: 显示项目详情
  ElMessage.info('查看项目详情功能待开发')
}

const editProject = (project: HeritageProject) => {
  editingProject.value = project
  Object.assign(projectForm, project)
  showAddProject.value = true
}

const toggleProjectStatus = async (project: HeritageProject) => {
  try {
    // TODO: 调用API
    project.is_active = !project.is_active
    ElMessage.success(project.is_active ? '项目已启用' : '项目已停用')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const deleteProject = async (project: HeritageProject) => {
  try {
    await ElMessageBox.confirm('确定要删除这个项目吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // TODO: 调用API删除
    ElMessage.success('删除成功')
    loadProjects()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const saveProject = async () => {
  try {
    // TODO: 表单验证和API调用
    ElMessage.success(editingProject.value ? '更新成功' : '添加成功')
    showAddProject.value = false
    editingProject.value = null
    Object.assign(projectForm, {
      name: '',
      description: '',
      origin_location: '',
      category: '',
      level: '',
      cover_image: '',
      video_url: '',
      history: '',
      characteristics: '',
      inheritor_id: null
    })
    loadProjects()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 传承人相关方法
const viewInheritor = (inheritor: HeritageInheritor) => {
  // TODO: 显示传承人详情
  ElMessage.info('查看传承人详情功能待开发')
}

const editInheritor = (inheritor: HeritageInheritor) => {
  editingInheritor.value = inheritor
  Object.assign(inheritorForm, inheritor)
  showAddInheritor.value = true
}

const toggleInheritorStatus = async (inheritor: HeritageInheritor) => {
  try {
    // TODO: 调用API
    inheritor.is_active = !inheritor.is_active
    ElMessage.success(inheritor.is_active ? '传承人已启用' : '传承人已停用')
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const deleteInheritor = async (inheritor: HeritageInheritor) => {
  try {
    await ElMessageBox.confirm('确定要删除这个传承人吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // TODO: 调用API删除
    ElMessage.success('删除成功')
    loadInheritors()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const saveInheritor = async () => {
  try {
    // TODO: 表单验证和API调用
    ElMessage.success(editingInheritor.value ? '更新成功' : '添加成功')
    showAddInheritor.value = false
    editingInheritor.value = null
    Object.assign(inheritorForm, {
      name: '',
      gender: '',
      birth_year: null,
      hometown: '',
      specialty: '',
      biography: '',
      achievements: '',
      avatar: '',
      contact_info: ''
    })
    loadInheritors()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 分页处理
const handleProjectSizeChange = (size: number) => {
  projectPagination.size = size
  loadProjects()
}

const handleProjectCurrentChange = (page: number) => {
  projectPagination.page = page
  loadProjects()
}

const handleInheritorSizeChange = (size: number) => {
  inheritorPagination.size = size
  loadInheritors()
}

const handleInheritorCurrentChange = (page: number) => {
  inheritorPagination.page = page
  loadInheritors()
}

onMounted(() => {
  loadProjects()
  loadInheritors()
})
</script>

<style scoped>
.heritage-management {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-row {
  margin-bottom: 20px;
}

.project-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.project-cover {
  width: 60px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
}

.project-details {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.project-name {
  font-weight: 500;
  color: #333;
}

.project-origin {
  font-size: 12px;
  color: #666;
}

.inheritor-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.inheritor-details {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.inheritor-name {
  font-weight: 500;
  color: #333;
}

.inheritor-meta {
  font-size: 12px;
  color: #666;
}

.inheritor-hometown {
  font-size: 12px;
  color: #999;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style> 