<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'

// 这里应该导入处方相关的API，但目前还没有创建，先注释掉
// import { getPrescriptions, createPrescription, updatePrescription, deletePrescription } from '@/api/prescription'

const loading = ref(false)
const prescriptions = ref<Prescription[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formMode = ref<'add' | 'edit'>('add')
const formRef = ref<FormInstance>()

interface Prescription {
  id?: string | number
  userId: string | number
  title: string
  description: string
  duration: number
  frequency: number
  status: 'active' | 'inactive'
}

const form = ref<Prescription>({
  userId: '',
  title: '',
  description: '',
  duration: 30,
  frequency: 3,
  status: 'active'
})

const rules = reactive<FormRules>({
  userId: [{ required: true, message: '请输入用户ID', trigger: 'blur' }],
  title: [{ required: true, message: '请输入处方名称', trigger: 'blur' }],
  description: [{ required: true, message: '请输入处方描述', trigger: 'blur' }],
  duration: [{ required: true, message: '请输入建议时长', trigger: 'blur' }],
  frequency: [{ required: true, message: '请输入建议频率', trigger: 'blur' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
})

const fetchPrescriptions = async () => {
  loading.value = true
  try {
    // 模拟API调用，实际项目中应该使用真实API
    // const res = await getPrescriptions({
    //   page: currentPage.value,
    //   limit: pageSize.value
    // })
    // prescriptions.value = res.items
    // total.value = res.total
    
    // 模拟数据
    setTimeout(() => {
      prescriptions.value = [
        {
          id: 1,
          userId: 101,
          title: '老年人轻度运动处方',
          description: '适合60-70岁老年人的轻度运动处方，以舒缓的广场舞为主',
          duration: 30,
          frequency: 3,
          status: 'active'
        },
        {
          id: 2,
          userId: 102,
          title: '关节保健运动处方',
          description: '针对关节炎患者的舞蹈处方，以柔和的动作为主',
          duration: 20,
          frequency: 5,
          status: 'active'
        }
      ]
      total.value = 2
      loading.value = false
    }, 500)
  } catch (error) {
    ElMessage.error('获取处方列表失败')
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

const handleEdit = (row: Prescription) => {
  formMode.value = 'edit'
  dialogTitle.value = '编辑处方'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (id: string | number) => {
  ElMessageBox.confirm('确定要删除该处方吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      // await deletePrescription(id)
      ElMessage.success('删除成功')
      fetchPrescriptions()
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
          // await createPrescription(form.value)
          ElMessage.success('添加成功')
        } else {
          // await updatePrescription(form.value.id!, form.value)
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

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchPrescriptions()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchPrescriptions()
}

onMounted(() => {
  fetchPrescriptions()
})
</script>

<template>
  <div class="prescription-container">
    <div class="header">
      <h2>运动处方管理</h2>
      <ElButton type="primary" @click="handleAdd">添加处方</ElButton>
    </div>

    <ElTable v-loading="loading" :data="prescriptions" border style="width: 100%">
      <ElTableColumn prop="userId" label="用户ID" width="100" />
      <ElTableColumn prop="title" label="处方名称" />
      <ElTableColumn prop="description" label="处方描述" show-overflow-tooltip />
      <ElTableColumn prop="duration" label="建议时长">
        <template #default="{ row }">
          {{ row.duration }}分钟/天
        </template>
      </ElTableColumn>
      <ElTableColumn prop="frequency" label="建议频率">
        <template #default="{ row }">
          {{ row.frequency }}次/周
        </template>
      </ElTableColumn>
      <ElTableColumn prop="status" label="状态">
        <template #default="{ row }">
          <ElTag :type="row.status === 'active' ? 'success' : 'info'">
            {{ row.status === 'active' ? '生效中' : '已结束' }}
          </ElTag>
        </template>
      </ElTableColumn>
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
        <ElFormItem label="处方名称" prop="title">
          <ElInput v-model="form.title" />
        </ElFormItem>
        <ElFormItem label="处方描述" prop="description">
          <ElInput v-model="form.description" type="textarea" :rows="3" />
        </ElFormItem>
        <ElFormItem label="建议时长" prop="duration">
          <ElInputNumber v-model="form.duration" :min="1" :max="360" />
          <span class="unit">分钟/天</span>
        </ElFormItem>
        <ElFormItem label="建议频率" prop="frequency">
          <ElInputNumber v-model="form.frequency" :min="1" :max="7" />
          <span class="unit">次/周</span>
        </ElFormItem>
        <ElFormItem label="状态" prop="status">
          <ElSelect v-model="form.status" style="width: 100%">
            <ElOption label="生效中" value="active" />
            <ElOption label="已结束" value="inactive" />
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
  </div>
</template>

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
  color: var(--el-text-color-regular);
}
</style> 