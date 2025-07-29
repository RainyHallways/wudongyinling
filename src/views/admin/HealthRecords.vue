<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

// 这里应该导入健康记录相关的API，但目前还没有创建，先注释掉
// import { getRecords, createRecord, updateRecord, deleteRecord } from '@/api/health'

const loading = ref(false)
const records = ref<HealthRecord[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formMode = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()

interface BloodPressure {
  systolic: number
  diastolic: number
}

interface HealthRecord {
  id?: string | number
  userId: string | number
  recordDate: string | Date
  weight: number
  height: number
  heartRate: number
  bloodPressure: BloodPressure
  notes: string
}

const form = ref<HealthRecord>({
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

const rules = reactive<FormRules>({
  userId: [{ required: true, message: '请输入用户ID', trigger: 'blur' }],
  recordDate: [{ required: true, message: '请选择记录日期', trigger: 'change' }],
  weight: [{ required: true, message: '请输入体重', trigger: 'blur' }],
  height: [{ required: true, message: '请输入身高', trigger: 'blur' }],
  heartRate: [{ required: true, message: '请输入心率', trigger: 'blur' }],
  'bloodPressure.systolic': [{ required: true, message: '请输入收缩压', trigger: 'blur' }],
  'bloodPressure.diastolic': [{ required: true, message: '请输入舒张压', trigger: 'blur' }]
})

const formatDate = (date: string | Date): string => {
  return new Date(date).toLocaleDateString('zh-CN')
}

const fetchRecords = async () => {
  loading.value = true
  try {
    // 模拟API调用，实际项目中应该使用真实API
    // const res = await getRecords({
    //   page: currentPage.value,
    //   limit: pageSize.value
    // })
    // records.value = res.items
    // total.value = res.total
    
    // 模拟数据
    setTimeout(() => {
      records.value = [
        {
          id: 1,
          userId: 101,
          recordDate: '2025-03-01',
          weight: 65.5,
          height: 168,
          heartRate: 72,
          bloodPressure: {
            systolic: 125,
            diastolic: 85
          },
          notes: '运动后测量'
        },
        {
          id: 2,
          userId: 102,
          recordDate: '2025-03-02',
          weight: 70.2,
          height: 175,
          heartRate: 68,
          bloodPressure: {
            systolic: 118,
            diastolic: 78
          },
          notes: '早晨空腹测量'
        }
      ]
      total.value = 2
      loading.value = false
    }, 500)
  } catch (error) {
    ElMessage.error('获取健康记录失败')
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

const handleEdit = (row: HealthRecord) => {
  formMode.value = 'edit'
  dialogTitle.value = '编辑记录'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (id: string | number) => {
  ElMessageBox.confirm('确定要删除该记录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // await deleteRecord(id)
      ElMessage.success('删除成功')
      fetchRecords()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const handleSubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return
  await formEl.validate(async (valid) => {
    if (valid) {
      try {
        if (formMode.value === 'add') {
          // await createRecord(form.value)
          ElMessage.success('添加成功')
        } else {
          // await updateRecord(form.value.id!, form.value)
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

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchRecords()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchRecords()
}

onMounted(() => {
  fetchRecords()
})
</script>

<template>
  <div class="health-records-container">
    <div class="header">
      <h2>健康记录管理</h2>
      <ElButton type="primary" @click="handleAdd">添加记录</ElButton>
    </div>

    <ElTable 
      v-loading="loading" 
      :data="records" 
      border 
      style="width: 100%"
      header-row-class-name="table-header-white"
    >
      <ElTableColumn prop="userId" label="用户ID" width="100" />
      <ElTableColumn prop="recordDate" label="记录日期" width="120">
        <template #default="{ row }">
          {{ formatDate(row.recordDate) }}
        </template>
      </ElTableColumn>
      <ElTableColumn prop="weight" label="体重">
        <template #default="{ row }">
          {{ row.weight }}kg
        </template>
      </ElTableColumn>
      <ElTableColumn prop="height" label="身高">
        <template #default="{ row }">
          {{ row.height }}cm
        </template>
      </ElTableColumn>
      <ElTableColumn prop="heartRate" label="心率">
        <template #default="{ row }">
          {{ row.heartRate }}次/分
        </template>
      </ElTableColumn>
      <ElTableColumn prop="bloodPressure" label="血压">
        <template #default="{ row }">
          {{ row.bloodPressure.systolic }}/{{ row.bloodPressure.diastolic }}mmHg
        </template>
      </ElTableColumn>
      <ElTableColumn prop="notes" label="备注" show-overflow-tooltip />
      <ElTableColumn label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <ElButtonGroup>
            <ElButton type="primary" @click="handleEdit(row)">编辑</ElButton>
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
        <ElFormItem label="用户ID" prop="userId">
          <ElInput v-model="form.userId" />
        </ElFormItem>
        <ElFormItem label="记录日期" prop="recordDate">
          <ElDatePicker
            v-model="form.recordDate"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          />
        </ElFormItem>
        <ElFormItem label="体重" prop="weight">
          <ElInputNumber v-model="form.weight" :min="20" :max="200" :precision="1" />
          <span class="unit">kg</span>
        </ElFormItem>
        <ElFormItem label="身高" prop="height">
          <ElInputNumber v-model="form.height" :min="100" :max="250" :precision="1" />
          <span class="unit">cm</span>
        </ElFormItem>
        <ElFormItem label="心率" prop="heartRate">
          <ElInputNumber v-model="form.heartRate" :min="40" :max="200" />
          <span class="unit">次/分</span>
        </ElFormItem>
        <ElFormItem label="血压" prop="bloodPressure.systolic">
          <ElInputNumber v-model="form.bloodPressure.systolic" :min="60" :max="200" class="blood-pressure" />
          <span class="separator">/</span>
          <ElInputNumber v-model="form.bloodPressure.diastolic" :min="40" :max="130" class="blood-pressure" />
          <span class="unit">mmHg</span>
        </ElFormItem>
        <ElFormItem label="备注" prop="notes">
          <ElInput v-model="form.notes" type="textarea" :rows="3" />
        </ElFormItem>
      </ElForm>
      <template #footer>
        <span class="dialog-footer">
          <ElButton @click="dialogVisible = false">取消</ElButton>
          <ElButton type="primary" @click="handleSubmit(formRef)">确定</ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>

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
  color: var(--el-text-color-regular);
}

.blood-pressure {
  width: 120px;
}

.separator {
  margin: 0 8px;
  color: var(--el-text-color-regular);
}
</style> 