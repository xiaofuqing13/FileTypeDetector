<template>
  <div class="container">
    <div class="filter-controls">
      <el-config-provider :locale="zhCn">
        <el-date-picker
            v-model="dateRange"
            type="monthrange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            :clearable="true"
            @change="handleDateChange"
            value-format="YYYY-MM"
            :default-time="[
            new Date(2000, 1, 1, 0, 0, 0),
            new Date(2000, 1, 1, 23, 59, 59)
          ]"
        />
      </el-config-provider>
    </div>
    <div ref="fullFile" style="width: 100%; height: 400px;"></div>
    <div ref="successFile" style="width: 100%; height: 400px;"></div>
    <div ref="pieChart" style="width: 100%; height: 400px;"></div>

  </div>
</template>

<script>
import {ref, onMounted, onUnmounted, watch} from 'vue';
import * as echarts from 'echarts';
import axios from 'axios';
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { ElDatePicker } from 'element-plus';

export default {
  components: {ElDatePicker},
  setup() {
    const fullFile = ref(null);
    const successFile = ref(null);
    const pieChart = ref(null);
    const dateRange = ref([]);
    let fullFileInstance = null;
    let successFileInstance = null;
    let pieChartInstance = null;

    const initCharts = () => {
      fullFileInstance = echarts.init(fullFile.value);
      successFileInstance = echarts.init(successFile.value);
      pieChartInstance = echarts.init(pieChart.value);
    };
    // 生成随机颜色的函数
    const getRandomColor = () => {
      return '#' + Math.floor(Math.random()*16777215).toString(16);
    };
    const fetchBarData = async () => {
      try {
        const response = await axios.get('http://localhost:8080/api/charts/fullFileBar', {
          params: {
            startDate: dateRange.value?.[0],
            endDate: dateRange.value?.[1]
          }
        });
        const data = response.data;

        const categories = data.map(item => item.month);
        const values = data.map(item => item.fileCount);
        // 为每个类别生成一个随机颜色
        const colors = categories.map(() => getRandomColor());
        fullFileInstance.setOption({
          title: { text: '柱状图' },
          tooltip: {},
          xAxis: {
            data: categories
          },
          yAxis: {},
          series: [{
            name: '数值',
            type: 'bar',
            data:  values.map((value, index) => ({
              value: value,
              itemStyle: {
                color: colors[index]
              }
            }))
          }]
        });
      } catch (error) {
        console.error('获取柱状图数据失败:', error);
      }
    };

    const fetchSuccessBarData = async () => {
      try {
        const response = await axios.get('http://localhost:8080/api/charts/successFileBar', {
          params: {
            startDate: dateRange.value?.[0],
            endDate: dateRange.value?.[1]
          }
        });
        const data = response.data;

        const categories = data.map(item => item.actual_type);
        const values = data.map(item => item.count);
        // 为每个类别生成一个随机颜色
        const colors = categories.map(() => getRandomColor());
        successFileInstance.setOption({
          title: { text: '柱状图' },
          tooltip: {},
          xAxis: {
            data: categories
          },
          yAxis: {},
          series: [{
            name: '数值',
            type: 'bar',
            data:  values.map((value, index) => ({
              value: value,
              itemStyle: {
                color: colors[index]
              }
            }))
          }]
        });
      } catch (error) {
        console.error('获取柱状图数据失败:', error);
      }
    };

    const fetchPieData = async () => {
      try {
        const response = await axios.get('http://localhost:8080/api/charts/pie');
        const data = response.data;

        const pieData = data.map(item => ({
          name: item.actual_type,
          value: item.count
        }));

        pieChartInstance.setOption({
          title: { text: '饼图' },
          tooltip: {
            trigger: 'item',
            formatter: '{a} <br/>{b}: {c} ({d}%)'
          },
          series: [{
            name: '数据分布',
            type: 'pie',
            radius: '50%',
            data: pieData
          }]
        });
      } catch (error) {
        console.error('获取饼图数据失败:', error);
      }
    };

    onMounted(() => {
      initCharts();
      fetchBarData();
      fetchSuccessBarData();
      fetchPieData();
      window.addEventListener('resize', handleResize);
    });

    onUnmounted(() => {
      fullFileInstance && fullFileInstance.dispose();
      pieChartInstance && pieChartInstance.dispose();
      successFileInstance && successFileInstance.dispose();
      window.removeEventListener('resize', handleResize);
    });

    const handleResize = () => {
      fullFileInstance && fullFileInstance.resize();
      pieChartInstance && pieChartInstance.resize();
      successFileInstance && successFileInstance.resize();
    };

    const handleDateChange = (value) => {
      dateRange.value = value;
      fetchBarData();
    };

    watch(dateRange, () => {
      fetchBarData();
      fetchSuccessBarData()
      fetchPieData();
    }, { deep: true });

    return { fullFile, successFile, pieChart, handleDateChange, dateRange, zhCn };
  }
}
</script>
<style scoped>
.filter-controls {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}

.chart {
  height: 400px;
  width: 100%;
}
</style>