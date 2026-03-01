# FileTypeDetector — 文件类型智能识别系统

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-000000?logo=flask)](https://flask.palletsprojects.com/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-2.x-brightgreen?logo=springboot)](https://spring.io/)
[![Vue.js](https://img.shields.io/badge/Vue.js-2.x-4FC08D?logo=vue.js)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

## 项目背景

日常工作中经常遇到 **文件扩展名被篡改、丢失或不可信** 的情况——比如把 `.exe` 改成 `.jpg` 伪装传输，或者收到一个没有扩展名的附件不知道用什么软件打开。仅靠扩展名判断文件类型存在明显的安全隐患和识别盲区。

本项目通过分析文件的 **二进制特征**（字节分布 + 文件大小），结合随机森林机器学习模型和 python-magic、filetype 等工具进行多层级检测，能够识别 50 种常见文件格式。即使扩展名被篡改或删除，也能准确判断文件的真实类型。

## 系统架构

```
┌─────────────────┐      HTTP       ┌─────────────────┐      REST
│   Vue.js 前端    │ ◄─────────────► │ Spring Boot 后端  │ ◄──────────►
│ (file-type-front)│                 │     (demo)       │
│                  │                 │                  │
│  · 文件上传界面   │                 │  · 文件接收与转发  │
│  · ECharts 图表  │                 │  · 数据持久化     │
│  · 识别结果展示   │                 │  · 业务逻辑处理   │
└─────────────────┘                 └────────┬─────────┘
      :3030                                   │ HTTP
                                    ┌─────────▼────────┐
                                    │  Python AI 服务   │
                                    │ (RandomForestModel)│
                                    │                   │
                                    │  · 随机森林模型    │
                                    │  · python-magic   │
                                    │  · filetype 检测  │
                                    │  · Flask API      │
                                    └───────────────────┘
                                          :5000
```

## 核心能力

- **AI 驱动识别：** 训练随机森林分类器，基于 256 维字节分布特征 + 文件大小进行分类
- **多层检测：** python-magic → filetype → 扩展名 → 模型预测，四重验证提高准确率
- **50 类文件支持：** 覆盖文档、图片、音视频、压缩包、代码源文件等常见格式
- **结果对比：** 同时展示 AI 预测结果与实际检测结果，方便评估准确率
- **数据可视化：** 前端 ECharts 图表展示识别统计数据

## 项目结构

```
FileTypeDetector/
├── RandomForestModel/          # AI 模型服务（Python/Flask）
│   ├── app.py                  # Flask API 服务
│   ├── model_training.py       # 模型训练脚本
│   ├── Test_prediction.py      # 模型测试
│   ├── file_type_model.pkl     # 训练好的模型文件
│   └── requirements.txt
├── demo/                       # 后端服务（Spring Boot/Maven）
│   ├── src/main/java/
│   └── pom.xml
└── file-type-front/            # 前端（Vue.js）
    ├── src/
    └── package.json
```

## 快速开始

**环境要求：** Python 3.8+、JDK 8+、Node.js 14+、MySQL

```bash
# 1. 启动 AI 模型服务
cd RandomForestModel
pip install -r requirements.txt
python app.py    # 运行在 :5000

# 2. 启动后端
cd demo
mvn spring-boot:run    # 运行在 :8080

# 3. 启动前端
cd file-type-front
npm install
npm run serve    # 运行在 :3030
```

## 模型训练

如果需要重新训练模型：

```bash
cd RandomForestModel
python model_training.py
# 会扫描 training_files/ 目录下的样本文件
# 提取字节分布特征，训练随机森林分类器
# 输出 file_type_model.pkl
```

## 开源协议

MIT License
