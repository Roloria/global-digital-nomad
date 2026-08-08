# 贡献指南 / Contributing Guide

感谢你考虑为「全球数字游民计划」做出贡献！🎉  
我们欢迎任何形式的参与：数据修正、添加新城市、改进报告、翻译、Issue 讨论等。

---

## 🚀 快速贡献流程

1. **Fork 本仓库**到你的 GitHub 账号
2. **Clone** 你 fork 的仓库到本地：
   ```bash
   git clone https://github.com/<your-username>/global-digital-nomad.git
   cd global-digital-nomad
   ```
3. **创建分支**（不要直接改 main）：
   ```bash
   git checkout -b fix/add-bangkok-internet
   ```
4. **修改数据**（推荐改 `data/digital-nomad-cities.csv`，Excel 可选）
5. **提交**并**推送**：
   ```bash
   git add data/digital-nomad-cities.csv
   git commit -m "fix: 更新曼谷网络评分为 8.5"
   git push origin fix/add-bangkok-internet
   ```
6. 在 GitHub 上发起 **Pull Request**，描述你的修改

---

## 📝 贡献类型

### 🐛 修正数据错误
发现某个城市的某项评分明显不对？  
→ 直接编辑 `data/digital-nomad-cities.csv` 对应字段，发 PR。

### ➕ 添加新城市
新晋数字游民目的地？  
→ 在 CSV 末尾追加一行，填全 24 个字段（参考 [data/README.md](data/README.md)）。

### 🛂 更新签证政策
签证政策变了？  
→ 修改 `reports/digital-nomad-cities-report.md` 的「签证政策地图」段，或修改该城市的 visa 字段。

### 📊 增加新维度
想加上"税收"或"CoWorking 价格"？  
→ 在 [Issues](https://github.com/Roloria/global-digital-nomad/issues) 中先讨论，达成共识后再改。

### 🌐 翻译
想做英文版报告？  
→ 在 `reports/` 下新建 `digital-nomad-cities-report-en.md`。

---

## 📏 数据质量要求

每个评分字段都需要满足：
- **可验证**：附上 1–2 个公开数据来源（Nomad List、官方统计局、Numbeo、Wikipedia 等）
- **基于事实**：评分应反映可观察的指标，而不是个人喜好
- **时效性**：数据不应超过 12 个月
- **中立性**：避免主观偏见，尤其是安全、LGBTQ、女性友好等敏感维度

如果不确定如何评分，**先开 Issue 讨论**，不要直接发 PR。

---

## 🔄 数据更新频率

- **季度审查**：每 3 个月（1/4/7/10 月）由维护者发起一轮社区 review
- **持续更新**：欢迎随时发 PR 修正明显错误
- **重大变更**：如新增/删除维度，需要先在 Issues 讨论 ≥ 1 周

---

## 💻 编辑建议

### 编辑 CSV
CSV 文件是首要数据源，推荐用文本编辑器或 LibreOffice/Numbers 编辑：
- 保留 UTF-8 编码
- 字段含逗号请用双引号包裹
- 评分数值保留 1 位小数（如 `7.5` 而非 `7.50`）

### 编辑 Excel
- 修改后请**同步更新 CSV**（CSV 是 PR 的 source of truth）
- 保留原有的格式（色阶、冻结窗格等）

### 编辑 Markdown
- 中文为主，英文为辅
- 表格对齐使用 `|` + `---:|`

---

## 🧪 PR 检查清单

发 PR 前请确认：

- [ ] 修改字段已附数据来源
- [ ] CSV 与 Excel（如有改动）保持一致
- [ ] 综合分已按权重公式重新计算（见 [data/README.md](data/README.md)）
- [ ] 没有破坏表格/可视化结构
- [ ] Commit message 清晰（建议用 `fix:` / `feat:` / `docs:` / `data:` 前缀）

---

## 📐 综合分计算公式

```
综合分 = (
    网络      × 1.0 +
    社群      × 1.2 +
    生活      × 1.0 +
    安全      × 1.2 +
    英语      × 0.9 +
    步行      × 0.7 +
    空气      × 0.7 +
    女性友好  × 0.8 +
    LGBTQ+    × 0.6 +
    夜生活    × 0.5 +
    安静指数  × 0.6 +
    种族包容  × 0.6
) / 9.8
```

权重反映各因素对数字游民体验的相对重要性：
- 社群与安全权重最高（1.2）
- 网络、生活、英语其次
- 细分维度（夜生活、安静度等）作为补充

---

## 🛡️ 行为准则

参与本项目即表示同意遵守 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

---

## ❓ 有问题？

- 📖 先看 [README.md](README.md)
- 💬 在 [Discussions](https://github.com/Roloria/global-digital-nomad/discussions) 提问
- 🐛 Bug 或数据错误请提 [Issues](https://github.com/Roloria/global-digital-nomad/issues)

> 🌟 任何贡献都很珍贵——哪怕是修正一个错别字！
