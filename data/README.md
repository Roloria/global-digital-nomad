# 数据字典 / Data Dictionary

本目录是「全球数字游民计划」的核心数据集。

## 文件清单

| 文件 | 用途 | 推荐使用场景 |
|---|---|---|
| `digital-nomad-cities.csv` | 主数据，UTF-8，逗号分隔 | **首选** — 便于 PR diff、版本控制、代码处理 |
| `digital-nomad-cities.xlsx` | Excel 多 sheet 版本 | 人工浏览、对比分析 |

两份文件内容一致，CSV 是 source of truth，Excel 由脚本生成。

## 字段说明（24 列）

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
| 9 | 网络 | internet | float | 0–10 | 7.5 |
| 10 | 社群 | community | float | 0–10 | 8.0 |
| 11 | 生活 | fun | float | 0–10 | 8.0 |
| 12 | 安全 | safety | float | 0–10 | 8.5 |
| 13 | 英语 | english | float | 0–10 | 7.0 |
| 14 | 步行 | walk | float | 0–10 | 7.0 |
| 15 | 空气 | air | float | 0–10 | 7.0 |
| 16 | 女性友好 | female | float | 0–10 | 9.0 |
| 17 | LGBTQ+ | lgbt | float | 0–10 | 9.0 |
| 18 | 夜生活 | nightlife | float | 0–10 | 8.0 |
| 19 | 安静指数 | peace | float | 0–10 | 7.0 |
| 20 | 种族包容 | racial | float | 0–10 | 8.0 |
| 21 | 年均气温 (°C) | temp_c | int | °C | 18 |
| 22 | 最佳季节 | best_season | string | — | 4月-6月, 9月-10月 |
| 23 | 签证 | visa | string | — | D7/D8 数字游民签证 |
| 24 | 综合分 | overall | float | 0–10 | 7.9 |
| 25 | 最后更新 | last_updated | string (date) | YYYY-MM-DD | 2026-08-08 |

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
- 新增城市：必须填全 24 个字段，至少提供 3 个数据来源
- 重大重构（修改权重、删除/新增维度）：先开 Issue 讨论 ≥ 1 周

## 数据来源

详见 [`docs/data-sources.md`](../docs/data-sources.md)。

## 同步脚本

将 CSV 转换为 Excel：

```python
import pandas as pd
df = pd.read_csv("digital-nomad-cities.csv")
df.to_excel("digital-nomad-cities.xlsx", index=False)
```

更多脚本见 [`docs/methodology.md`](../docs/methodology.md)。
