# 🌐 全球数字游民社区地图 / Global Digital Nomad Communities

> **TL;DR**：60 个全球热门数字游民社区的结构化资料库 · 5 大类型 · 6 大区域 · 匿名体验共建

| 数据集 | 入口 |
|---|---|
| 主数据 CSV | [`data/digital-nomad-communities.csv`](../data/digital-nomad-communities.csv) |
| Excel 多 sheet | [`data/digital-nomad-communities.xlsx`](../data/digital-nomad-communities.xlsx) |
| 在线浏览 | [roloria.github.io/global-digital-nomad/#communities](https://roloria.github.io/global-digital-nomad/#communities) |
| 数据字典 | [`data/README.md`](../data/README.md) |
| 匿名提交 | 站内「📤 分享社区体验」按钮 |

---

## 一、为什么做这个数据集

[主榜单](digital-nomad-cities-report.md) 回答的是"哪些城市适合数字游民居住"。但当一个 nomad 抵达一座新城市，**第一个问题不是"住哪"，而是"找谁"**。

- 在曼谷，没有人带你进 Co-working，你可能两个月都见不到同类；
- 在清迈，找不到合适的 Meetup，可能误入「保险+房产」的局；
- 在迪拜，错过 Astrolabs 这种科技孵化器，等于白来一趟。

社区（Community）才是数字游民真正的入口。本数据集把全网能找到的**主流数字游民社区**结构化整理出来，让你：

1. **提前调研**：出发前看社区位置 / 政策 / 价格 / 联系方式，决定要不要去；
2. **到点就入伙**：所有联系方式都已列清，到了就发邮件 / 申请；
3. **共建知识库**：自己住过 / 待过，可以匿名提交体验，补充社区真实情况。

---

## 二、数据集结构

| 字段 | 类型 | 示例 |
|---|---|---|
| 排名 / 区域 / 城市 / 国家 / 国旗 | 基础信息 | 巴厘岛 (乌布), 印尼, 🇮🇩 |
| 社区名称 / 社区名称(英) | 名称 | Hubud / Hubud Bali |
| 类型 | 枚举 | 联合办公 / 联合生活 / 聚会 / 度假村 / 在线社群 |
| 简介 | 文本 | 巴厘岛数字游民运动起点 |
| 月费 (USD) | 区间 | $130–220/月 |
| 容量 | 整数 | 80 |
| 政策摘要 | 文本 | 日票可用 / 24×7 开放 / 接受访客 |
| 网址 / 联系邮箱 / 社群链接 | 联系方式 | hubud.org / hello@hubud.org |
| 综合分 | 0–10 | 8.4 |
| 来源 / 最后更新 | 元信息 | hubud.org/about / 2026-08-08 |

完整字段说明见 [`data/README.md`](../data/README.md)。

---

## 三、5 类社区地图

### 1. 联合办公 (Coworking) — 45 个

**最常见的形态**。月票通常 $70–$350，提供工位 / 会议室 / 高速 WiFi / 咖啡。

| 推荐 | 城市 | 月费 | 综合分 |
|---|---|---|---|
| **CAMP @ Maya** | 清迈 | $70–110 | ⭐ 8.7 |
| **Dojo Bali** | 长谷 | $165 | ⭐ 8.5 |
| **Second Home Lisboa** | 里斯本 | $250–400 | ⭐ 8.5 |
| **Hubud** | 乌布 | $130–220 | ⭐ 8.4 |
| **St. Oberholz** | 柏林 | $130–220 | ⭐ 8.4 |
| **Lift99** | 塔林 | $140–220 | ⭐ 8.1 |
| **The Coworking Hub** | 拉斯帕尔马斯 | $150–250 | ⭐ 8.3 |
| **Casa Coworking Roma** | 墨西哥城 | $140–220 | ⭐ 8.2 |
| **OneCoWork Marina** | 巴塞罗那 | $180–280 | ⭐ 8.0 |

**特点**：
- 适合 1 周-3 个月的中短期游民
- 通常接受访客日票（Day Pass），随时体验
- 多数有周度固定 Social Hour / 创业者晚餐

### 2. 联合生活 (Coliving) — 9 个

**生活+工作一体的精品小院**。月费 $1,200–$4,000，含住宿+工作空间，部分含三餐。

| 推荐 | 城市 | 月费 | 综合分 |
|---|---|---|---|
| **Outpost Ubud** | 乌布 | $1,850–2,800 | ⭐ 8.7 |
| **Outsite Canggu** | 长谷 | $1,400–2,500 | ⭐ 8.6 |
| **WiFi Tribe** | 全球轮换 | $2,000–3,500 | ⭐ 8.4 |
| **Roam** | 多国 | $2,500–4,000 | ⭐ 8.0 |
| **Nomad House** | 全球 | $1,200–2,200 | ⭐ 7.8 |
| **Casa Con Vista** | 卡塔赫纳 | $1,200–1,800 | ⭐ 8.1 |
| **Outpost Sanur** | 沙努尔 | $1,800–2,600 | ⭐ 8.2 |

**特点**：
- 适合 1-3 个月深度融入
- 申请审核 / 入住最少天数限制
- 强烈社交导向，每天与 5-30 人共处
- 比 Airbnb 酒店更适合找长期合作伙伴

### 3. 聚会 (Meetup) — 1 个

**Chiang Mai Digital Nomads**（meetup.com）— 全球最大游民线下聚会群，周日晚固定晚宴，3,000+ 成员。

### 4. 度假村 (Resort) — 3 个

**Selina Tulum / Marrakech / Nomad Cruise** — 酒店型混合住宿+工作空间，月费 $800–$12,000（含船上）。

### 5. 在线社群 (Online) — 2 个

| 名称 | URL | 综合分 | 规模 |
|---|---|---|---|
| **Nomad List** | nomadlist.com | ⭐ 8.9 | 50,000+ |
| **Coworker.com** | coworker.com | ⭐ 7.7 | 26,000+ 空间 |

---

## 四、6 大区域分布

| 区域 | 社区数 | 代表 |
|---|---|---|
| 🌏 **亚洲** | 20 | Hubud / CAMP @ Maya / Dojo Bali / Punspace / 大理数字游民社区 / Naked Hub |
| 🌍 **欧洲** | 18 | Second Home / St. Oberholz / Heden / Lift99 / KAPTÁR / OneCoWork |
| 🌎 **拉美** | 9 | Casa Coworking / Plataforma / Casa Con Vista / Selina Tulum |
| 🌐 **全球** | 6 | Nomad List / WiFi Tribe / Roam / Nomad House / Coworker.com |
| 🌍 **非洲** | 4 | The Workspace Cape Town / iHub Nairobi / Selina Marrakech |
| 🕌 **中东** | 3 | WeWork Dubai / Astrolabs / Mindspace Tel Aviv |

---

## 五、综合分 TOP 10

| # | 社区 | 城市 | 类型 | 综合分 |
|---:|---|---|---|---:|
| 1 | Nomad List | 线上 | 在线社群 | 8.9 |
| 2 | Outpost Ubud | 巴厘岛 (乌布) | 联合生活 | 8.7 |
| 3 | CAMP @ Maya | 清迈 | 联合办公 | 8.7 |
| 4 | Outsite Canggu | 巴厘岛 (长谷) | 联合生活 | 8.6 |
| 5 | Dojo Bali | 巴厘岛 (长谷) | 联合办公 | 8.5 |
| 6 | Second Home Lisboa | 里斯本 | 联合办公 | 8.5 |
| 7 | Hubud | 巴厘岛 (乌布) | 联合办公 | 8.4 |
| 8 | St. Oberholz | 柏林 | 联合办公 | 8.4 |
| 9 | WiFi Tribe | 全球轮换 | 联合生活 | 8.4 |
| 10 | The Coworking Hub | 拉斯帕尔马斯 | 联合办公 | 8.3 |

---

## 六、价格分布

| 月费区间 | 社区数 | 类型 |
|---|---:|---|
| 免费 / Meetup AA 制 | 1 | 聚会 |
| $70–$200 (纯 Co-working 月票) | 24 | 联合办公 |
| $200–$400 (高端 Co-working) | 19 | 联合办公 |
| $800–$2,000 (Coliving + 工作) | 11 | 联合生活 / 度假村 |
| $2,000–$4,000 (高端 Coliving) | 4 | 联合生活 |
| $5,000+ (Nomad Cruise 等) | 1 | 度假村 |

> 注：纯在线社群（Nomad List, Coworker.com）单独列出，无月费但有"高级会员"选项。

---

## 七、如何使用本数据集

### 7.1 出行前调研

```bash
# 查看清迈附近的数字游民社区
grep "清迈" data/digital-nomad-communities.csv
```

### 7.2 添加新社区

参考 [`data/README.md`](../data/README.md) 中的字段说明，发起 PR：

```bash
git checkout -b feat/add-medellin-community
# 编辑 data/digital-nomad-communities.csv
git add data/digital-nomad-communities.csv
git commit -m "feat(data): 添加麦德林新社区 XXX"
git push origin feat/add-medellin-community
# 在 GitHub 发起 PR
```

### 7.3 匿名分享体验

在网站 https://roloria.github.io/global-digital-nomad/#communities 顶部点击「📤 分享社区体验（匿名）」：

1. 选择社区 + 居住时长 + 季节
2. 描述你的真实体验（无需注册账号）
3. 一键导出 JSON 或跳转 GitHub Issue 上报

提交后数据保存在**你的浏览器本地**（localStorage），可以选择不上传，也可以一键上报贡献给开源项目。

---

## 八、隐私与匿名

- ✅ 体验表单**只在你浏览器**保存，不自动上传
- ✅ 你可以选择不上传（仅本地），也可以一键上报
- ✅ 上报走 GitHub Issue，**GitHub Issue 默认公开**，请勿包含姓名、邮箱、电话
- ✅ 维护者定期合并 PR 到主 CSV，PR 标题与正文不包含个人信息

如果你的体验包含敏感内容（如社区负面新闻、欺诈投诉），请用 GitHub Issue 的私人方式联系维护者。

---

## 九、数据来源与采集方法

每个社区字段都附 **来源 (source)** 字段，指向社区官方页面或第三方评测页面。采集方法：

1. **官方页面**：每个社区首先访问其官方网址，提取简介 / 价格 / 政策 / 联系信息
2. **第三方评测**：Nomad List / Coworker.com / 维基百科等交叉验证
3. **实地走访**：维护者或社区贡献者的实地考察记录

任何字段都可以通过 PR 修改，欢迎补充来源链接。

---

## 十、更新日志

- **2026-08-08**：v1 首版发布 · 60 个社区 · 5 类 · 6 区 · 全字段填齐
  - 亚洲 20 / 欧洲 18 / 拉美 9 / 全球 6 / 非洲 4 / 中东 3
  - 联合办公 45 / 联合生活 9 / 度假村 3 / 在线 2 / 聚会 1
  - 18 字段：排名 / 区域 / 城市 / 国家 / 国旗 / 名称 / 英文名 / 类型 / 简介 / 月费 / 容量 / 政策 / 网址 / 邮箱 / 社群 / 综合分 / 来源 / 最后更新
  - 配套 Excel 多 sheet（综合数据 + 类型分布 + 区域分布 + TOP10 透视）

---

## 十一、相关数据集

- [城市榜单报告](digital-nomad-cities-report.md) — 80 个城市 12 维评分
- [中国大陆数字游民城市专项](digital-nomad-cities-china-report.md) — 16 个中国城市
- [游民数逐城来源](nomad-counts-sources.md) — 城市数据来源与调整记录

---

**维护者**：[@Roloria](https://github.com/Roloria) · 任何 PR / Issue / Discussion 都被欢迎。
