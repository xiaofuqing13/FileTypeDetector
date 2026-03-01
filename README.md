# FileTypeDetector — 文件类型智能识别系统

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org/)
[![Flask](https://img.shields.io/badge/Flask-后端-000000?logo=flask)](https://flask.palletsprojects.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-前端-4FC08D?logo=vue.js)](https://vuejs.org/)
[![License](https://img.shields.io/badge/License-MIT-blue)](LICENSE)

## 项目背景

文件扩展名可以被随意修改，依赖扩展名判断文件类型既不可靠也不安全。在网络安全、数字取证、文件管理等场景中，需要通过分析文件的二进制结构（魔数、文件头）来准确识别真实文件类型。市面上虽有命令行工具（如 `file` 命令），但缺乏友好的图形界面和批量处理能力。

本系统通过解析文件的 Magic Bytes（文件头魔数），结合自建的文件特征库，实现不依赖扩展名的精准文件类型识别。前后端分离架构，支持单文件和批量检测。

## 效果展示

![系统主界面](docs/main-interface.png)

支持拖拽上传文件，自动识别文件真实类型，展示文件魔数、置信度等详细信息。

## 核心功能

| 功能 | 说明 |
|------|------|
| 魔数识别 | 解析文件头部字节，匹配已知文件类型特征 |
| 批量检测 | 支持同时上传多个文件进行批量识别 |
| 伪装检测 | 检测文件扩展名与实际类型是否一致 |
| 类型分类 | 自动归类为文档、图片、音视频、压缩包等 |
| 详情展示 | 显示 Magic Bytes 十六进制值和匹配规则 |

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue.js + Element Plus |
| 后端 | Flask + Python |
| 识别引擎 | python-magic + 自定义规则库 |
| 部署 | Nginx + Gunicorn |

## 项目结构

```
FileTypeDetector/
├── file-type-back/             # Flask 后端
│   ├── app.py                  # 主入口
│   ├── detector/               # 识别引擎
│   ├── rules/                  # 文件特征规则库
│   └── requirements.txt
├── file-type-front/            # Vue.js 前端
│   ├── src/
│   │   ├── views/
│   │   └── components/
│   └── package.json
└── README.md
```

## 快速开始

```bash
# 后端
cd file-type-back
pip install -r requirements.txt
python app.py

# 前端
cd file-type-front
npm install
npm run dev
```

## 开源协议

MIT License
