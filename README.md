# 🔍 FileTypeDetector — 基于随机森林的文件类型智能识别系统

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.x-000000?logo=flask" alt="Flask">
  <img src="https://img.shields.io/badge/Spring%20Boot-2.x-brightgreen?logo=springboot" alt="Spring Boot">
  <img src="https://img.shields.io/badge/Vue.js-2.x-4FC08D?logo=vue.js" alt="Vue.js">
  <img src="https://img.shields.io/badge/scikit--learn-RandomForest-F7931E?logo=scikitlearn" alt="scikit-learn">
  <img src="https://img.shields.io/badge/License-MIT-blue" alt="License">
</p>

> 基于 **随机森林算法** 的文件类型智能识别系统。通过分析文件二进制特征（字节分布 + 文件大小），结合 python-magic 和 filetype 库进行多层级检测，支持 **50 种文件类型** 的精准识别。采用 **Python AI 模型 + Spring Boot 后端 + Vue.js 前端** 三层微服务架构。

---

## ✨ 核心特性

- 🤖 **AI 驱动** — 随机森林分类器，基于 256 维字节分布特征 + 文件大小进行训练
- 🔬 **多层检测** — python-magic → filetype → 文件扩展名 → 模型预测，四重验证
- 📊 **50 类识别** — 覆盖文档、图片、音视频、压缩包、代码源文件等 50 种常见文件类型
- 🎯 **结果对比** — 同时展示 AI 预测结果与实际检测结果，直观对比准确率
- 📈 **数据可视化** — 前端 ECharts 图表展示识别统计数据

---

## 🏗️ 系统架构

```
┌──────────────────────┐     HTTP      ┌──────────────────────┐     REST     ┌──────────────────────┐
│    Vue.js 前端        │ ◄──────────► │  Spring Boot 后端     │ ◄─────────► │  Flask + AI 模型      │
│  (file-type-front)   │              │     (demo)            │              │ (RandomForestModel)  │
│                      │              │                       │              │                      │
│  · 文件上传界面       │              │  · 文件接收与转发      │              │  · 特征提取           │
│  · ECharts 图表      │              │  · 数据持久化          │              │  · 随机森林预测        │
│  · 识别结果展示       │              │  · 业务逻辑处理        │              │  · python-magic 检测  │
└──────────────────────┘              └──────────────────────┘              └──────────────────────┘
         :3030                                :8080                               :5001
```

---

## 📁 项目结构

```
FileTypeDetector/
├── RandomForestModel/              # 🤖 AI 模型服务 (Python/Flask)
│   ├── app.py                      # Flask API 服务（/process_file 接口）
│   ├── model_training.py           # 模型训练脚本
│   ├── Test_prediction.py          # 模型测试脚本
│   ├── Randomly_generate_data_sets.py  # 训练数据生成
│   └── data/                       # 训练数据目录
├── demo/                           # ⚙️ 后端服务 (Spring Boot)
│   ├── src/main/java/.../
│   │   ├── controller/             # FileController, ChartsController
│   │   ├── service/                # FileService
│   │   ├── mapper/                 # MyBatis Mapper
│   │   └── config/                 # CORS, Multipart 配置
│   └── pom.xml
├── file-type-front/                # 🖥️ 前端 (Vue.js)
│   ├── src/
│   │   ├── list/fileList.vue       # 文件列表组件
│   │   ├── charts/fileChart.vue    # 统计图表组件
│   │   └── plugins/                # Axios, Element UI
│   └── package.json
└── README.md
```

---

## 🔬 支持的文件类型（50 类）

| 类别 | 格式 |
|---|---|
| **文档** | `.txt` `.pdf` `.docx` `.xls` `.xlsx` `.ppt` `.pptx` `.rtf` `.md` `.csv` |
| **图片** | `.png` `.jpg` `.gif` |
| **音频** | `.mp3` `.wav` |
| **视频** | `.mp4` `.avi` `.mov` `.mkv` `.flv` |
| **压缩** | `.zip` `.tar` `.rar` |
| **代码** | `.py` `.java` `.js` `.ts` `.c` `.cpp` `.go` `.rb` `.php` `.swift` `.kt` `.dart` `.h` `.class` |
| **配置** | `.json` `.xml` `.html` `.css` `.scss` `.yml` `.ini` `.log` |
| **其他** | `.exe` `.bat` `.sh` `.iso` `.bin` |

---

## 🚀 快速开始

### 环境要求
- Python 3.8+ · pip
- JDK 8+ · Maven
- Node.js 14+ · npm
- MySQL

### 1️⃣ 启动 AI 模型服务

```bash
cd RandomForestModel
pip install flask scikit-learn numpy python-magic filetype joblib
python app.py
# 运行在 http://localhost:5001
```

### 2️⃣ 启动后端服务

```bash
cd demo
mvn spring-boot:run
# 运行在 http://localhost:8080
```

### 3️⃣ 启动前端

```bash
cd file-type-front
npm install
npm run serve
# 运行在 http://localhost:3030
```

---

## 🧠 模型训练

如需重新训练模型：

```bash
cd RandomForestModel
# 1. 生成训练数据集
python Randomly_generate_data_sets.py
# 2. 训练模型
python model_training.py
# 3. 测试模型
python Test_prediction.py
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
