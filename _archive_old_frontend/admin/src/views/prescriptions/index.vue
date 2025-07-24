<template>
  <div class="prescription-container">
    <div class="header">
      <h2>运动处方管理</h2>
      <el-button type="primary" @click="handleAdd">添加处方</el-button>
    </div>

    <el-table v-loading="loading" :data="prescriptions" border style="width: 100%">
      <el-table-column prop="userId" label="用户ID" width="100" />
      <el-table-column prop="title" label="处方名称" />
      <el-table-column prop="description" label="处方描述" show-overflow-tooltip />
      <el-table-column prop="duration" label="建议时长">
        <template #default="{ row }">
          {{ row.duration }}分钟/天
        </template>
      </el-table-column>
      <el-table-column prop="frequency" label="建议频率">
        <template #default="{ row }">
          {{ row.frequency }}次/周
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'info'">
            {{ row.status === 'active' ? '生效中' : '已结束' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button-group>
            <el-button type="primary" @click="handleEdit(row)">编辑</el-button>
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
        <el-form-item label="用户ID" prop="userId">
          <el-input v-model="form.userId" />
        </el-form-item>
        <el-form-item label="处方名称" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="处方描述" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="建议时长" prop="duration">
          <el-input-number v-model="form.duration" :min="1" :max="360" />
          <span class="unit">分钟/天</span>
        </el-form-item>
        <el-form-item label="建议频率" prop="frequency">
          <el-input-number v-model="form.frequency" :min="1" :max="7" />
          <span class="unit">次/周</span>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="form.status" style="width: 100%">
            <el-option label="生效中" value="active" />
            <el-option label="已结束" value="inactive" />
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { prescriptionApi } from '@/api'

const loading = ref(false)
const prescriptions = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formMode = ref('add')
const formRef = ref(null)

const form = ref({
  userId: '',
  title: '',
  description: '',
  duration: 30,
  frequency: 3,
  status: 'active'
})

const rules = {
  userId: [{ required: true, message: '请输入用户ID', trigger: 'blur' }],
  title: [{ required: true, message: '请输入处方名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入处方描述', trigger: 'blur' }],
  duration: [{ required: true, message: '请输入建议时长', trigger: 'blur' }],
  frequency: [{ required: true, message: '请输入建议频率', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

const fetchPrescriptions = async () => {
  loading.value = true
  try {
    const res = await prescriptionApi.getPrescriptions({
      page: currentPage.value,
      pageSize: pageSize.value
    })
    prescriptions.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    ElMessage.error('获取处方列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  formMode.value = 'add'
  dialogTitle.value = '添加处方'
  form.value = {
    userId: '',
    title: '',
    description: '',
    duration: 30,
    frequency: 3,
    status: 'active'
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  formMode.value = 'edit'
  dialogTitle.value = '编辑处方'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除该处方吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await prescriptionApi.deletePrescription(id)
      ElMessage.success('删除成功')
      fetchPrescriptions()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const handleSubmit = async (formEl) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      try {
        if (formMode.value === 'add') {
          await prescriptionApi.createPrescription(form.value)
          ElMessage.success('添加成功')
        } else {
          await prescriptionApi.updatePrescription(form.value.id, form.value)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchPrescriptions()
      } catch (error) {
        ElMessage.error(formMode.value === 'add' ? '添加失败' : '更新失败')
      }
    }
  })
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchPrescriptions()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchPrescriptions()
}

onMounted(() => {
  fetchPrescriptions()
})
</script>

<style scoped>
.prescription-container {
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