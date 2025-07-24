<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

// 这里应该导入挑战相关的API，但目前还没有创建，先注释掉
// import { getChallenges, createChallenge, updateChallenge, deleteChallenge, getRecords } from '@/api/challenge'

const loading = ref(false)
const challenges = ref<Challenge[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formMode = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()

const recordsDialogVisible = ref(false)
const recordsDialogTitle = ref('')
const challengeRecords = ref<ChallengeRecord[]>([])

interface Challenge {
  id: string | number
  title: string
  description: string
  startDate: string | Date
  endDate: string | Date
  targetDays: number
  reward: number
  status: 'pending' | 'active' | 'completed'
}

interface ChallengeRecord {
  id: string | number
  userId: string | number
  checkInDate: string | Date
  duration: number
  content: string
  status: 'valid' | 'invalid'
}

const form = ref<Challenge>({
  id: '',
  title: '',
  description: '',
  startDate: '',
  endDate: '',
  targetDays: 7,
  reward: 100,
  status: 'pending'
})

const rules = reactive<FormRules>({
  title: [{ required: true, message: '请输入挑战名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入挑战描述', trigger: 'blur' }],
  startDate: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  endDate: [{ required: true, message: '请选择结束日期', trigger: 'change' }],
  targetDays: [{ required: true, message: '请输入目标天数', trigger: 'blur' }],
  reward: [{ required: true, message: '请输入奖励积分', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
})

const formatDate = (date: string | Date): string => {
  return new Date(date).toLocaleDateString('zh-CN')
}

const getStatusType = (status: string): string => {
  switch (status) {
    case 'pending':
      return 'info'
    case 'active':
      return 'success'
    case 'completed':
      return 'warning'
    default:
      return 'info'
  }
}

const getStatusText = (status: string): string => {
  switch (status) {
    case 'pending':
      return '未开始'
    case 'active':
      return '进行中'
    case 'completed':
      return '已结束'
    default:
      return '未知'
  }
}

const fetchChallenges = async () => {
  loading.value = true
  try {
    // 模拟API调用，实际项目中应该使用真实API
    // const res = await getChallenges({
    //   page: currentPage.value,
    //   limit: pageSize.value
    // })
    // challenges.value = res.items
    // total.value = res.total
    
    // 模拟数据
    setTimeout(() => {
      challenges.value = [
        {
          id: 1,
          title: '21天健身舞打卡',
          description: '连续21天每天练习健身舞15分钟，养成运动好习惯',
          startDate: '2025-03-01',
          endDate: '2025-03-21',
          targetDays: 21,
          reward: 200,
          status: 'active'
        },
        {
          id: 2,
          title: '民族舞学习月',
          description: '学习4种民族舞基础动作，感受传统文化魅力',
          startDate: '2025-04-01',
          endDate: '2025-04-30',
          targetDays: 30,
          reward: 300,
          status: 'pending'
        }
      ]
      total.value = 2
      loading.value = false
    }, 500)
  } catch (error) {
    ElMessage.error('获取挑战列表失败')
    loading.value = false
  }
}

const handleAdd = () => {
  formMode.value = 'add'
  dialogTitle.value = '添加挑战'
  form.value = {
    id: '',
    title: '',
    description: '',
    startDate: '',
    endDate: '',
    targetDays: 7,
    reward: 100,
    status: 'pending'
  }
  dialogVisible.value = true
}

const handleEdit = (row: Challenge) => {
  formMode.value = 'edit'
  dialogTitle.value = '编辑挑战'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (id: string | number) => {
  ElMessageBox.confirm('确定要删除该挑战吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // await deleteChallenge(id)
      ElMessage.success('删除成功')
      fetchChallenges()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const handleViewRecords = async (row: Challenge) => {
  recordsDialogTitle.value = `${row.title} - 打卡记录`
  try {
    // 模拟API调用，实际项目中应该使用真实API
    // const res = await getRecords(row.id, {
    //   page: 1,
    //   limit: 100
    // })
    // challengeRecords.value = res.items
    
    // 模拟数据
    challengeRecords.value = [
      {
        id: 1,
        userId: 101,
        checkInDate: '2025-03-01',
        duration: 20,
        content: '完成了今天的广场舞练习',
        status: 'valid'
      },
      {
        id: 2,
        userId: 102,
        checkInDate: '2025-03-01',
        duration: 15,
        content: '练习了民族舞基本步伐',
        status: 'valid'
      }
    ]
    recordsDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取打卡记录失败')
  }
}

const handleSubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      try {
        if (formMode.value === 'add') {
          // await createChallenge(form.value)
          ElMessage.success('添加成功')
        } else {
          // await updateChallenge(form.value.id, form.value)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchChallenges()
      } catch (error) {
        ElMessage.error(formMode.value === 'add' ? '添加失败' : '更新失败')
      }
    }
  })
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchChallenges()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchChallenges()
}

onMounted(() => {
  fetchChallenges()
})
</script>

<template>
  <div class="challenges-container">
    <div class="header">
      <h2>打卡挑战管理</h2>
      <ElButton type="primary" @click="handleAdd">添加挑战</ElButton>
    </div>

    <ElTable v-loading="loading" :data="challenges" border style="width: 100%">
      <ElTableColumn prop="title" label="挑战名称" />
      <ElTableColumn prop="description" label="挑战描述" show-overflow-tooltip />
      <ElTableColumn prop="startDate" label="开始日期" width="120">
        <template #default="{ row }">
          {{ formatDate(row.startDate) }}
        </template>
      </ElTableColumn>
      <ElTableColumn prop="endDate" label="结束日期" width="120">
        <template #default="{ row }">
          {{ formatDate(row.endDate) }}
        </template>
      </ElTableColumn>
      <ElTableColumn prop="targetDays" label="目标天数">
        <template #default="{ row }">
          {{ row.targetDays }}天
        </template>
      </ElTableColumn>
      <ElTableColumn prop="reward" label="奖励积分">
        <template #default="{ row }">
          {{ row.reward }}分
        </template>
      </ElTableColumn>
      <ElTableColumn prop="status" label="状态" width="100">
        <template #default="{ row }">
          <ElTag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </ElTag>
        </template>
      </ElTableColumn>
      <ElTableColumn label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <ElButtonGroup>
            <ElButton type="primary" @click="handleEdit(row)">编辑</ElButton>
            <ElButton type="success" @click="handleViewRecords(row)">查看记录</ElButton>
            <ElButton type="danger" @click="handleDelete(row.id)">删除</ElButton>
          </ElButtonGroup>
        </template>
      </ElTableColumn>
    </ElTable>

    <div class="pagination">
      <ElPagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <ElDialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
    >
      <ElForm
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <ElFormItem label="挑战名称" prop="title">
          <ElInput v-model="form.title" />
        </ElFormItem>
        <ElFormItem label="挑战描述" prop="description">
          <ElInput v-model="form.description" type="textarea" :rows="3" />
        </ElFormItem>
        <ElFormItem label="开始日期" prop="startDate">
          <ElDatePicker
            v-model="form.startDate"
            type="date"
            placeholder="选择开始日期"
            style="width: 100%"
          />
        </ElFormItem>
        <ElFormItem label="结束日期" prop="endDate">
          <ElDatePicker
            v-model="form.endDate"
            type="date"
            placeholder="选择结束日期"
            style="width: 100%"
          />
        </ElFormItem>
        <ElFormItem label="目标天数" prop="targetDays">
          <ElInputNumber v-model="form.targetDays" :min="1" :max="365" />
          <span class="unit">天</span>
        </ElFormItem>
        <ElFormItem label="奖励积分" prop="reward">
          <ElInputNumber v-model="form.reward" :min="0" :max="10000" />
          <span class="unit">分</span>
        </ElFormItem>
        <ElFormItem label="状态" prop="status">
          <ElSelect v-model="form.status" style="width: 100%">
            <ElOption label="未开始" value="pending" />
            <ElOption label="进行中" value="active" />
            <ElOption label="已结束" value="completed" />
          </ElSelect>
        </ElFormItem>
      </ElForm>
      <template #footer>
        <span class="dialog-footer">
          <ElButton @click="dialogVisible = false">取消</ElButton>
          <ElButton type="primary" @click="handleSubmit(formRef)">确定</ElButton>
        </span>
      </template>
    </ElDialog>

    <ElDialog
      v-model="recordsDialogVisible"
      :title="recordsDialogTitle"
      width="800px"
    >
      <ElTable :data="challengeRecords" border>
        <ElTableColumn prop="userId" label="用户ID" width="100" />
        <ElTableColumn prop="checkInDate" label="打卡日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.checkInDate) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="duration" label="运动时长">
          <template #default="{ row }">
            {{ row.duration }}分钟
          </template>
        </ElTableColumn>
        <ElTableColumn prop="content" label="打卡内容" show-overflow-tooltip />
        <ElTableColumn prop="status" label="状态" width="100">
          <template #default="{ row }">
            <ElTag :type="row.status === 'valid' ? 'success' : 'danger'">
              {{ row.status === 'valid' ? '有效' : '无效' }}
            </ElTag>
          </template>
        </ElTableColumn>
      </ElTable>
    </ElDialog>
  </div>
</template>

<style scoped>
.challenges-container {
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.unit {
  margin-left: 10px;
  color: var(--el-text-color-regular);
}
</style> 