 <template>
  <div class="challenges-container">
    <div class="header">
      <h2>打卡挑战管理</h2>
      <el-button type="primary" @click="handleAdd">添加挑战</el-button>
    </div>

    <el-table v-loading="loading" :data="challenges" border style="width: 100%">
      <el-table-column prop="title" label="挑战名称" />
      <el-table-column prop="description" label="挑战描述" show-overflow-tooltip />
      <el-table-column prop="startDate" label="开始日期" width="120">
        <template #default="{ row }">
          {{ formatDate(row.startDate) }}
        </template>
      </el-table-column>
      <el-table-column prop="endDate" label="结束日期" width="120">
        <template #default="{ row }">
          {{ formatDate(row.endDate) }}
        </template>
      </el-table-column>
      <el-table-column prop="targetDays" label="目标天数">
        <template #default="{ row }">
          {{ row.targetDays }}天
        </template>
      </el-table-column>
      <el-table-column prop="reward" label="奖励积分">
        <template #default="{ row }">
          {{ row.reward }}分
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">
            {{ getStatusText(row.status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button type="success" @click="handleViewRecords(row)">查看记录</el-button>
            <el-button type="danger" @click="handleDelete(row.id)">删除</el-button>
          </el-button-group>
        </template>
      </el-table-column>
    </el-table>

    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="100px"
      >
        <el-form-item label="挑战名称" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="挑战描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="开始日期" prop="startDate">
          <el-date-picker
            v-model="form.startDate"
            type="date"
            placeholder="选择开始日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束日期" prop="endDate">
          <el-date-picker
            v-model="form.endDate"
            type="date"
            placeholder="选择结束日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="目标天数" prop="targetDays">
          <el-input-number v-model="form.targetDays" :min="1" :max="365" />
          <span class="unit">天</span>
        </el-form-item>
        <el-form-item label="奖励积分" prop="reward">
          <el-input-number v-model="form.reward" :min="0" :max="10000" />
          <span class="unit">分</span>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="未开始" value="pending" />
            <el-option label="进行中" value="active" />
            <el-option label="已结束" value="completed" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit(formRef)">确定</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog
      v-model="recordsDialogVisible"
      :title="recordsDialogTitle"
      width="800px"
    >
      <el-table :data="challengeRecords" border>
        <el-table-column prop="userId" label="用户ID" width="100" />
        <el-table-column prop="checkInDate" label="打卡日期" width="120">
          <template #default="{ row }">
            {{ formatDate(row.checkInDate) }}
          </template>
        </el-table-column>
        <el-table-column prop="duration" label="运动时长">
          <template #default="{ row }">
            {{ row.duration }}分钟
          </template>
        </el-table-column>
        <el-table-column prop="content" label="打卡内容" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'valid' ? 'success' : 'danger'">
              {{ row.status === 'valid' ? '有效' : '无效' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { challengeApi } from '@/api'

const loading = ref(false)
const challenges = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formMode = ref('add')
const formRef = ref(null)

const recordsDialogVisible = ref(false)
const recordsDialogTitle = ref('')
const challengeRecords = ref([])

const form = ref({
  title: '',
  description: '',
  startDate: '',
  endDate: '',
  targetDays: 7,
  reward: 100,
  status: 'pending'
})

const rules = {
  title: [{ required: true, message: '请输入挑战名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入挑战描述', trigger: 'blur' }],
  startDate: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  endDate: [{ required: true, message: '请选择结束日期', trigger: 'change' }],
  targetDays: [{ required: true, message: '请输入目标天数', trigger: 'blur' }],
  reward: [{ required: true, message: '请输入奖励积分', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('zh-CN')
}

const getStatusType = (status) => {
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

const getStatusText = (status) => {
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
    const res = await challengeApi.getChallenges({
      page: currentPage.value,
      pageSize: pageSize.value
    })
    challenges.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    ElMessage.error('获取挑战列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  formMode.value = 'add'
  dialogTitle.value = '添加挑战'
  form.value = {
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

const handleEdit = (row) => {
  formMode.value = 'edit'
  dialogTitle.value = '编辑挑战'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除该挑战吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await challengeApi.deleteChallenge(id)
      ElMessage.success('删除成功')
      fetchChallenges()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const handleViewRecords = async (row) => {
  recordsDialogTitle.value = `${row.title} - 打卡记录`
  try {
    const res = await challengeApi.getRecords(row.id, {
      page: 1,
      pageSize: 100
    })
    challengeRecords.value = res.data.items
    recordsDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取打卡记录失败')
  }
}

const handleSubmit = async (formEl) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      try {
        if (formMode.value === 'add') {
          await challengeApi.createChallenge(form.value)
          ElMessage.success('添加成功')
        } else {
          await challengeApi.updateChallenge(form.value.id, form.value)
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

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchChallenges()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchChallenges()
}

onMounted(() => {
  fetchChallenges()
})
</script>

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
  color: #606266;
}
</style>