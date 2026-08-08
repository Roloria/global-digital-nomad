# 数据字典 / Data Dictionary

本目录是「全球数字游民计划」的核心数据集。

## 文件清单

| 文件 | 用途 | 推荐使用场景 |
|---|---|---|
| `digital-nomad-cities.csv` | 主数据，UTF-8，逗号分隔 | **首选** — 便于 PR diff、版本控制、代码处理 |
| `digital-nomad-cities.xlsx` | Excel 多 sheet 版本 | 人工浏览、对比分析 |
| `digital-nomad-cities-china.csv` | 中国大陆补充数据（16 城，26 列与主表一致） | 中国境内数字游民城市专项分析 |

两份文件内容一致，CSV 是 source of truth，Excel 由脚本生成。

## 字段说明（26 列）

| # | 字段 | 英文 | 类型 | 单位 | 示例 |
|---:|---|---|---|---|---|
| 1 | 排名 | rank | int | — | 1 |
| 2 | 区域 | region | string | — | 亚洲 / 欧洲 / 拉美 / 非洲 / 中东 |
| 3 | 城市 | city | string | — | 里斯本 |
| 4 | 国家 | country | string | — | 葡萄牙 |
| 5 | 国家(英) | country_en | string | — | Portugal |
| 6 | 国旗 | flag | string (emoji) | — | 🇵🇹 |
| 7 | 游民数 | nomads | int | 人 | 2800 |
| 8 | 月成本 (USD) | cost_usd | int | USD/月 | 2300 |
| 9 | 货币类型 | currency | string | — | 美元 / 人民币 |
| 10 | 网络 | internet | float | 0–10 | 7.5 |
| 11 | 社群 | community | float | 0–10 | 8.0 |
| 12 | 生活 | fun | float | 0–10 | 8.0 |
| 13 | 安全 | safety | float | 0–10 | 8.5 |
| 14 | 英语 | english | float | 0–10 | 7.0 |
| 15 | 步行 | walk | float | 0–10 | 7.0 |
| 16 | 空气 | air | float | 0–10 | 7.0 |
| 17 | 女性友好 | female | float | 0–10 | 9.0 |
| 18 | LGBTQ+ | lgbt | float | 0–10 | 9.0 |
| 19 | 夜生活 | nightlife | float | 0–10 | 8.0 |
| 20 | 安静指数 | peace | float | 0–10 | 7.0 |
| 21 | 种族包容 | racial | float | 0–10 | 8.0 |
| 22 | 年均气温 (°C) | temp_c | int | °C | 18 |
| 23 | 最佳季节 | best_season | string | — | 4月-6月, 9月-10月 |
| 24 | 签证 | visa | string | — | D7/D8 数字游民签证 |
| 25 | 综合分 | overall | float | 0–10 | 7.9 |
| 26 | 最后更新 | last_updated | string (date) | YYYY-MM-DD | 2026-08-08 |

> ⚠️ **排名自动派生**:按「**游民数** desc → 综合分 desc → 城市 asc」自动重算,无需手动维护。修改游民数或综合分后刷新网站即生效;CSV 中的排名列由脚本同步重写以保持一致。

## 评分口径

所有评分采用 0–10 分制（10 最佳）：

| 分值 | 含义 |
|---|---|
| 9.0–10 | 世界级 / 全球顶尖 |
| 7.5–8.9 | 优秀 |
| 6.0–7.4 | 良好 |
| 4.5–5.9 | 一般 |
| 3.0–4.4 | 偏差 |
| < 3.0 | 严重不足 |

## 综合分计算公式

```
overall = (
    internet  × 1.0 +
    community × 1.2 +
    fun       × 1.0 +
    safety    × 1.2 +
    english   × 0.9 +
    walk      × 0.7 +
    air       × 0.7 +
    female    × 0.8 +
    lgbt      × 0.6 +
    nightlife × 0.5 +
    peace     × 0.6 +
    racial    × 0.6
) / 9.8
```

权重合计 = 9.8，结果四舍五入保留 1 位小数。

## 最后更新时间字段

- **取值规则**：该城市数据最后被修改的日期
- **自动填充**：通过 `git blame` 自动获取每行数据的最后修改时间
- **手动更新**：如果使用 GitHub 网页编辑器修改 CSV，需手动更新该列
- **新城市**：使用提交当天的日期

## 月成本说明

- 包含：房租（单间公寓市中心）、餐饮、日常通勤、基础娱乐
- 不包含：国际机票、保险、签证申请费
- 中位数：基于过去 12 个月数据
- 误差范围：±30%（取决于个人生活方式）

## 数据更新规范

- 单一字段修改：在 Issue 或 PR 中注明 1–2 个数据来源
- 新增城市：必须填全 26 个字段，至少提供 3 个数据来源
- 重大重构（修改权重、删除/新增维度）：先开 Issue 讨论 ≥ 1 周

## 数据来源

详见 [`docs/data-sources.md`](../docs/data-sources.md)。

游民数逐城来源与调整记录详见 [`reports/nomad-counts-sources.md`](../reports/nomad-counts-sources.md)。

## 同步脚本

将 CSV 转换为 Excel：

```python
import pandas as pd
df = pd.read_csv("digital-nomad-cities.csv")
df.to_excel("digital-nomad-cities.xlsx", index=False)
```

更多脚本见 [`docs/methodology.md`](../docs/methodology.md)。

---

## 数字游民社区数据集 / Digital Nomad Communities

> 📍 第二份核心数据集 · `digital-nomad-communities.csv`
> 全网 60 个热门数字游民社区的结构化资料（位置/介绍/政策/联系方式）+ 匿名体验共建

### 文件清单

| 文件 | 用途 |
|---|---|
| `digital-nomad-communities.csv` | 社区主数据 · UTF-8 · 逗号分隔 · 18 列 · **首选用于 PR diff** |
| `digital-nomad-communities.xlsx` | Excel 多 sheet 版（含分布与 TOP10 透视） |

### 字段说明（18 列）

| # | 字段 | 英文 | 类型 | 示例 |
|---:|---|---|---|---|
| 1 | 排名 | rank | int | 1 |
| 2 | 区域 | region | string | 亚洲 / 欧洲 / 拉美 / 非洲 / 中东 / 全球 |
| 3 | 城市 | city | string | 巴厘岛 (乌布) |
| 4 | 国家 | country | string | 印尼 |
| 5 | 国旗 | flag | emoji | 🇮🇩 |
| 6 | 社区名称 | name | string | Hubud |
| 7 | 社区名称(英) | name_en | string | Hubud Bali |
| 8 | 类型 | type | enum | 联合办公 / 联合生活 / 聚会 / 度假村 / 在线社群 |
| 9 | 简介 | intro | string | 巴厘岛最早的联合办公空间… |
| 10 | 月费(USD) | price | string | $130–220/月 |
| 11 | 容量 | capacity | int | 80 |
| 12 | 政策摘要 | policy | string | 日票可用 / 周月票灵活 |
| 13 | 网址 | url | string | https://hubud.org |
| 14 | 联系邮箱 | email | string | hello@hubud.org |
| 15 | 社群链接 | social | string | https://facebook.com/HubudBali |
| 16 | 综合分 | overall | float | 8.4 |
| 17 | 来源 | source | string | hubud.org/about |
| 18 | 最后更新 | last_updated | YYYY-MM-DD | 2026-08-08 |

### 社区类型

| 类型 | 中文 | 含义 |
|---|---|---|
| Coworking | 联合办公 | 提供工位 / 会议室的共享办公空间 |
| Coliving | 联合生活 | 提供住宿 + 工作 + 餐饮的精品小院 |
| Meetup | 聚会 | 线下定期聚会 / 社团组织 |
| Resort | 度假村 | 酒店型混合住宿 + 工作空间 |
| Online | 在线社群 | 纯在线社群 / 平台 |

### 综合分计算口径

社区综合分（0–10）综合考虑以下因子（无固定权重，由维护者根据社区调研定期评分）：

- 游民友好度（英语通用度 / 24×7 开放 / 接受访客）
- 社群活跃度（周聚会 / 创业者氛围 / 新人欢迎）
- 价格透明度（月费公开 / 无隐藏费用 / 灵活月票）
- 设施完善度（高速 WiFi / 会议室 / 餐饮）
- 安全与包容（女性友好 / LGBTQ+ 友好 / 多元文化）

> 与城市榜单不同，社区没有公式化的自动综合分计算。评分由维护者根据实际走访或社区调研给出，**最后更新日期通过 Git 历史自动追溯**。

### 隐私与匿名提交

- 匿名体验表单保存在**浏览器本地**（localStorage），**不会**自动上传
- 一键导出 JSON 或通过 GitHub Issue 上报到开源仓库
- 提交指南见 [`docs/index.html`](../docs/index.html) 页面顶部的「📤 分享社区体验」按钮

### 添加新社区

新社区建议包含：

- 官方网址（首选 `https://`）
- 当前月费区间
- 至少 1 条政策亮点（如接受访客、24×7 开放等）
- 简介 < 80 字

可在 [`Issues`](https://github.com/Roloria/global-digital-nomad/issues) 中提议或在 PR 中直接编辑 CSV。

---

**最后修订**：2026-08-08
