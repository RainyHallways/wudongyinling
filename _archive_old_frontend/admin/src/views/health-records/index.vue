<template>
  <div class="health-records-container">
    <div class="header">
      <h2>健康记录管理</h2>
      <el-button type="primary" @click="handleAdd">添加记录</el-button>
    </div>

    <el-table v-loading="loading" :data="records" border style="width: 100%">
      <el-table-column prop="userId" label="用户ID" width="100" />
      <el-table-column prop="recordDate" label="记录日期" width="120">
        <template #default="{ row }">
          {{ formatDate(row.recordDate) }}
        </template>
      </el-table-column>
      <el-table-column prop="weight" label="体重">
        <template #default="{ row }">
          {{ row.weight }}kg
        </template>
      </el-table-column>
      <el-table-column prop="height" label="身高">
        <template #default="{ row }">
          {{ row.height }}cm
        </template>
      </el-table-column>
      <el-table-column prop="heartRate" label="心率">
        <template #default="{ row }">
          {{ row.heartRate }}次/分
        </template>
      </el-table-column>
      <el-table-column prop="bloodPressure" label="血压">
        <template #default="{ row }">
          {{ row.bloodPressure.systolic }}/{{ row.bloodPressure.diastolic }}mmHg
        </template>
      </el-table-column>
      <el-table-column prop="notes" label="备注" show-overflow-tooltip />
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
        <el-form-item label="记录日期" prop="recordDate">
          <el-date-picker
            v-model="form.recordDate"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="体重" prop="weight">
          <el-input-number v-model="form.weight" :min="20" :max="200" :precision="1" />
          <span class="unit">kg</span>
        </el-form-item>
        <el-form-item label="身高" prop="height">
          <el-input-number v-model="form.height" :min="100" :max="250" :precision="1" />
          <span class="unit">cm</span>
        </el-form-item>
        <el-form-item label="心率" prop="heartRate">
          <el-input-number v-model="form.heartRate" :min="40" :max="200" />
          <span class="unit">次/分</span>
        </el-form-item>
        <el-form-item label="血压" prop="bloodPressure.systolic">
          <el-input-number v-model="form.bloodPressure.systolic" :min="60" :max="200" class="blood-pressure" />
          <span class="separator">/</span>
          <el-input-number v-model="form.bloodPressure.diastolic" :min="40" :max="130" class="blood-pressure" />
          <span class="unit">mmHg</span>
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input v-model="form.notes" type="textarea" :rows="3" />
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
import { healthApi } from '@/api'

const loading = ref(false)
const records = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formMode = ref('add')
const formRef = ref(null)

const form = ref({
  userId: '',
  recordDate: new Date(),
  weight: 60,
  height: 170,
  heartRate: 75,
  bloodPressure: {
    systolic: 120,
    diastolic: 80
  },
  notes: ''
})

const rules = {
  userId: [{ required: true, message: '请输入用户ID', trigger: 'blur' }],
  recordDate: [{ required: true, message: '请选择记录日期', trigger: 'change' }],
  weight: [{ required: true, message: '请输入体重', trigger: 'blur' }],
  height: [{ required: true, message: '请输入身高', trigger: 'blur' }],
  heartRate: [{ required: true, message: '请输入心率', trigger: 'blur' }],
  'bloodPressure.systolic': [{ required: true, message: '请输入收缩压', trigger: 'blur' }],
  'bloodPressure.diastolic': [{ required: true, message: '请输入舒张压', trigger: 'blur' }]
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('zh-CN')
}

const fetchRecords = async () => {
  loading.value = true
  try {
    const res = await healthApi.getRecords({
      page: currentPage.value,
      pageSize: pageSize.value
    })
    records.value = res.data.items
    total.value = res.data.total
  } catch (error) {
    ElMessage.error('获取健康记录失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  formMode.value = 'add'
  dialogTitle.value = '添加记录'
  form.value = {
    userId: '',
    recordDate: new Date(),
    weight: 60,
    height: 170,
    heartRate: 75,
    bloodPressure: {
      systolic: 120,
      diastolic: 80
    },
    notes: ''
  }
  dialogVisible.value = true
}

const handleEdit = (row) => {
  formMode.value = 'edit'
  dialogTitle.value = '编辑记录'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (id) => {
  ElMessageBox.confirm('确定要删除该记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await healthApi.deleteRecord(id)
      ElMessage.success('删除成功')
      fetchRecords()
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
          await healthApi.createRecord(form.value)
          ElMessage.success('添加成功')
        } else {
          await healthApi.updateRecord(form.value.id, form.value)
          ElMessage.success('更新成功')
        }
        dialogVisible.value = false
        fetchRecords()
      } catch (error) {
        ElMessage.error(formMode.value === 'add' ? '添加失败' : '更新失败')
      }
    }
  })
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchRecords()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchRecords()
}

onMounted(() => {
  fetchRecords()
})
</script>

<style scoped>
.health-records-container {
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

.blood-pressure {
  width: 120px;
}

.separator {
  margin: 0 8px;
  color: #606266;
}
</style> 