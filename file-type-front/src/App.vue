<template>

  <div>
    <div class="upload-container">
      <el-upload
          v-model:file-list="fileList"
          class="upload-demo"
          drag
          action="http://localhost:8080/api/file/upload"
          multiple
          :on-preview="handlePreview"
          :on-remove="handleRemove"
          :on-success="handleSuccess"
          :on-error="handleError"
          :on-progress="handleProgress"
          :before-upload="beforeUpload"

      >
        <el-icon class="el-icon--upload"><upload-filled /></el-icon>
        <div class="el-upload__text">
          拖拽文件到此处或 <em>点击上传</em>
        </div>
      </el-upload>

      <el-progress :percentage="uploadProgress" v-if="uploadProgress > 0"></el-progress>

      <el-table :data="fileList" style="width: 100%">
        <el-table-column prop="extension" label="名称" width="180">
          <template #default="scope">
            {{ scope.row.name }}
          </template>
        </el-table-column>
        <el-table-column prop="size" label="大小">
          <template #default="scope">
            {{ (scope.row.size / 1024).toFixed(2) }} KB
          </template>
        </el-table-column>
        <el-table-column prop="status" label="状态">
          <template #default="scope">
            <el-tag :type="scope.row.status === 'success' ? 'success' : 'danger'">
              {{ scope.row.status === 'success' ? '上传成功' : '上传失败' }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </div>

  </div>
  <div id="charts" class="right">
    <Charts />
  </div>
  <div id="fileList">
    <FileList :show-history="showHistoryFiles" />
  </div>

</template>

<script setup>
import {ref} from 'vue'
import {ElMessage} from 'element-plus'
import {UploadFilled} from '@element-plus/icons-vue'
import FileList from './list/fileList.vue'
const fileList = ref([])
const uploadProgress = ref(0)
const showHistoryFiles = ref(false)

const handleRemove = (file, uploadFiles) => {
  console.log(file, uploadFiles)
}

const handlePreview = (uploadFile) => {
  console.log(uploadFile)
}

const handleProgress = (event, file, uploadFiles) => {
  uploadProgress.value = Math.round(event.percent)
  file.constructor
  uploadFiles.constructor
}

const handleSuccess = (response, uploadFile, uploadFiles) => {
  ElMessage.success('文件上传成功')
  uploadFile.status = 'success'
  uploadFile.data
  uploadFiles.valueOf()
  uploadProgress.value = 0
  showHistoryFiles.value = !showHistoryFiles.value;
}

const handleError = (error, uploadFile, uploadFiles) => {
  ElMessage.error('文件上传失败')
  uploadFile.status = 'error'
  uploadProgress.value = 0
  uploadFiles.constructor
}

const beforeUpload = (file) => {

  return file.size / 1024 < 50000
}

</script>
<script>
import Charts from "@/charts/fileChart.vue";

export default {
  name: 'App',
  components: {
    Charts
  }
}
</script>

<style scoped>

.upload-container, .right {
  max-width: 800px;
  margin: 20px auto;
}


ul {
  list-style-type: none;
  padding: 0;
}

button {
  margin-top: 10px;
  padding: 5px 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.el-pagination {
  margin-top: 20px;
  text-align: center;
}

button:hover {
  background-color: #45a049;
}
#app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

h1 {
  margin: 0;
}
</style>