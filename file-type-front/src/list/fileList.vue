<template>
  <div class="file-list">
    <h2>{{ '历史文件'}}</h2>
    <el-table :data="files" v-loading="loading" style="width: 100%">
      <el-table-column prop="fileName" label="文件名" width="180" />
      <el-table-column prop="fileSize" label="文件大小" width="120">
        <template #default="scope">
          {{ formatFileSize(scope.row.fileSize) }}
        </template>
      </el-table-column>
      <el-table-column prop="uploadTime" label="上传时间" width="180">
        <template #default="scope">
          {{ formatDate(scope.row.uploadTime) }}
        </template>
      </el-table-column>
      <el-table-column prop="recognitionTime" label="识别时间" width="180">
        <template #default="scope">
          {{ formatTimestamp(scope.row.recognitionTime) }}
        </template>
      </el-table-column>
      <el-table-column prop="predictedType" label="预测类型" width="120" />
      <el-table-column prop="actualType" label="实际类型" width="120" />
      <el-table-column prop="comparisonResult" label="比较结果" width="120">
        <template #default="scope">
          <el-tag :type="scope.row.comparisonResult ? 'success' : 'danger'">
            {{ scope.row.comparisonResult ? '匹配' : '不匹配' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="120">
        <template #default="scope">
          <el-button type="primary" size="small" @click="downloadFile(scope.row)">
            下载
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[10, 20, 50, 100]"
        :total="total"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        layout="total, sizes, prev, pager, next, jumper"
        class="pagination"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, defineProps } from 'vue'
import { ElTable, ElTableColumn, ElPagination, ElTag, ElButton, ElMessage } from 'element-plus'
import axios from 'axios'

const props = defineProps({
  showHistory: {
    type: Boolean,
    default: false
  }
})

const files = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)

const fetchData = async () => {
  loading.value = true
  try {
    const response = await axios.get('http://localhost:8080/api/file/list', {
      params: {
        page: currentPage.value,
        pageSize: pageSize.value
      }
    })
    files.value = response.data.list
    total.value = response.data.total
  } catch (error) {
    console.error('Error fetching files:', error)
    ElMessage.error('获取文件列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)

watch(() => props.showHistory, () => {
  currentPage.value = 1
  fetchData()
})

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchData()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
  fetchData()
}

const formatFileSize = (size) => {
  if (size < 1024) return size + ' B'
  if (size < 1024 * 1024) return (size / 1024).toFixed(2) + ' KB'
  return (size / (1024 * 1024)).toFixed(2) + ' MB'
}

const formatDate = (date) => {
  return new Date(date).toLocaleString()
}
const formatTimestamp = (timestamp) => {
  if (!timestamp) return '';
  const date = new Date(timestamp);
  return date.toLocaleString(); // 或者使用其他你喜欢的日期格式化方法
}


const downloadFile = async (file) => {
  try {
    const response = await axios({
      url: `http://localhost:8080/api/file/download/${file.id}`,
      method: 'GET',
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', file.fileName)
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)

    ElMessage.success(`文件 ${file.fileName} 下载成功`)
  } catch (error) {
    console.error('下载文件时出错:', error)
    ElMessage.error(`下载文件 ${file.fileName} 失败`)
  }
}
</script>

<style scoped>
.file-list {
  max-width: 1200px;
  margin: 0 auto;
}

.pagination {
  margin-top: 20px;
  text-align: right;
}
</style>