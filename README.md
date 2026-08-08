# 🌍 全球数字游民计划 / Global Digital Nomad Project

> 一个由全球数字游民社区共同维护的开源数据集与调研项目。  
> An open-source, community-maintained dataset and research project for the global digital nomad community.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub stars](https://img.shields.io/github/stars/Roloria/global-digital-nomad)](https://github.com/Roloria/global-digital-nomad/stargazers)
[![Data: 2026](https://img.shields.io/badge/Data-2026--07-blue)](data/)
[![🌐 Website](https://img.shields.io/badge/🌐_Website-Live-success?style=flat-square)](https://roloria.github.io/global-digital-nomad/)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Deployed-blueviolet?logo=github)](https://roloria.github.io/global-digital-nomad/)

---

## 📌 项目简介

**全球数字游民计划** 致力于以**开放协作**的方式，整理并持续更新全球适合数字游民居住/工作的城市数据，包括成本、网络、生活品质、安全、签证等关键维度。

数据综合自：
- Nomad List（nomadlist.com）
- 各国数字游民签证政策与官方旅游局数据
- Airbnb / Numbeo / CoWorker 等公开统计
- 实地调研与社区贡献

**覆盖范围**：5 大区域 · 39 国/地区 · 64 个主流数字游民城市

---

## 🌐 在线网站

<div align="center">

### 👉 https://roloria.github.io/global-digital-nomad/

</div>

> 一个完全可交互的网页应用，无需登录、移动端友好。

**核心功能**：

| 功能 | 说明 |
|---|---|
| 🔍 **多维筛选** | 按区域（5 大区）/ 国家（39 国）/ 排名（TOP 10/20/30/50/全部）/ 关键词搜索 |
| 📊 **可视化榜单** | 表格 + 评分条形图，点击行展开 12 维度完整详情 |
| 📤 **匿名提交** | 浏览器本地保存评分，附 GitHub Issue 模板一键上报 |
| 📐 **评分标准内置** | 页面底部完整展示 12 项评分口径与综合分计算公式 |
| 📱 **响应式** | 适配桌面 / 平板 / 手机（375px 起） |
| 🌙 **暗色模式** | 自动跟随系统主题 |

**快速体验**：[打开网站](https://roloria.github.io/global-digital-nomad/) · [数据 CSV](data/digital-nomad-cities.csv) · [可视化报告](reports/digital-nomad-cities-report.md)



## 📸 网站截图

| 桌面端 | 移动端 |
|---|---|
| ![桌面端](assets/screenshot-desktop.png) | ![移动端](assets/screenshot-mobile.png) |

> 截图说明：左侧为桌面端完整布局；右侧为 iPhone 14 尺寸下的自适应布局。

## 📂 仓库结构

```
global-digital-nomad/
├── README.md                        ← 本文件（项目说明）
├── CONTRIBUTING.md                  ← 如何贡献
├── CODE_OF_CONDUCT.md               ← 社区守则
├── LICENSE                          ← MIT 协议
│
├── data/                            ← 原始数据集
│   ├── digital-nomad-cities.xlsx    ← 主数据集（Excel）
│   ├── digital-nomad-cities.csv     ← 主数据集（CSV · 推荐用于 PR）
│   └── README.md                    ← 数据字典与字段说明
│
├── reports/                         ← 调研报告
│   └── digital-nomad-cities-report.md
│
├── visualizations/                  ← 可视化页面
│   ├── digital-nomad-cities.html              ← 内嵌片段
│   └── digital-nomad-cities-standalone.html   ← 独立页面（可直接打开）
│
├── docs/                            ← 方法论与数据来源
│   ├── methodology.md
│   └── data-sources.md
│
└── assets/                          ← 图片、Logo 等
```

---

## 🚀 快速开始

### 在线查看调研报告
👉 [`reports/digital-nomad-cities-report.md`](reports/digital-nomad-cities-report.md)

### 在线查看交互式可视化
下载 [`visualizations/digital-nomad-cities-standalone.html`](visualizations/digital-nomad-cities-standalone.html) 后在浏览器中打开。

### 使用数据
直接下载：
- `data/digital-nomad-cities.xlsx`（Excel 多 sheet 版）
- `data/digital-nomad-cities.csv`（纯数据，便于代码处理）

---

## 📊 核心数据维度

每个城市包含以下字段（详见 [data/README.md](data/README.md)）：

| 维度 | 说明 | 单位 |
|---|---|---|
| 排名 / 区域 / 城市 / 国家 | 基础信息 | — |
| 游民数 | 常驻/旅居的估算人数 | 人 |
| 月成本 | 单人月支出中位数 | USD |
| 网络 / 社群 / 生活 / 安全 | 0–10 分（10 最佳）| 分 |
| 英语 / 步行 / 空气 / 女性友好 / LGBTQ+ / 夜生活 / 安静度 / 种族包容 | 0–10 分 | 分 |
| 年均气温 / 最佳季节 / 签证 | 补充信息 | — |
| 综合分 | 加权平均 | 分 |

---

## 🤝 参与共建

**我们欢迎任何形式的贡献**：
- 🐛 修正数据错误
- ➕ 添加新城市
- 📊 更新评分（基于最新调研）
- 🛂 更新签证政策
- 🌍 添加新维度（税收、医疗、CoWorking 价格…）
- 📝 改进报告与可视化
- 🌐 多语言翻译

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。

---

## 📅 更新日志

- **2026-07**：首版发布，覆盖 64 个城市 / 39 个国家（亚洲 21 / 欧洲 18 / 拉美 15 / 非洲 7 / 中东 3）

---

## ⚖️ 许可证

本项目采用 [MIT 许可证](LICENSE)。你可以自由使用、修改和分发数据，但请保留原始来源声明。

数据本身来自多个公开来源，使用时请遵守各来源的使用条款。

---

## 🙏 致谢

- [Nomad List](https://nomadlist.com) — Pieter Levels 的开源数字游民数据
- [Flatio](https://flatio.com) — 数字游民住宿数据
- 所有参与贡献的 [贡献者们](https://github.com/Roloria/global-digital-nomad/graphs/contributors) ❤️

---

## 📬 联系方式

- 提交 Issue：[Issues](https://github.com/Roloria/global-digital-nomad/issues)
- 发起讨论：[Discussions](https://github.com/Roloria/global-digital-nomad/discussions)
- 维护者：[@Roloria](https://github.com/Roloria)

> 🌟 **如果这个项目对你有帮助，欢迎 Star、Fork、Watch，也欢迎推荐给身边正在考虑数字游民生活方式的朋友！**
