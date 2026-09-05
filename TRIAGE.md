# 🧹 每周 Issue Triage 手册

> 目标节奏：**每周固定一次，30 分钟**。所有网站「匿名提交」与社区 Issue 都在这里汇合。
> 每周一 09:00（北京时间），CI 会自动开出/更新「🧹 本周 Issue triage 清单」Issue（见
> `.github/workflows/weekly-triage.yml`），照单处理即可。

## 每周流程（照做即可）

1. **打开清单**：搜标题「🧹 本周 Issue triage」，CI 已列出全部开放 Issue + 年龄。
2. **逐条定级**，给每个 Issue 打标签并决定去向：
   | 情况 | 标签 | 去向 |
   |---|---|---|
   | 数据可信、字段明确 | `data` | 改 CSV 开 PR（或确认腾讯文档侧同步），merge 后关 |
   | 城市提名 | `feature` | 搬到 Discussions「🗳️ 求新城」收集 👍，按月汇总 |
   | 评分争议 | `question` | 搬到 Discussions 讨论；守护者意见优先；共识后统一改 |
   | 信息不足 | `needs-info` | 用模板补问一次；**2 周无回复关闭**（关时留一句话原因） |
   | 垃圾/灌水 | 关闭 | 必要时拉黑；git + PR 闸门兜底，不慌 |
3. **致谢**：对有效贡献者评论「感谢共建 🙏 你的贡献已进入本月贡献者荣誉榜统计」。
4. **更新清单**：处理完把结论回写到 triage Issue，作为当周存档。

## Issue → 数据 PR 的标准动作

```bash
gh issue view <N>                        # 读全上下文
# 1. 改 data/digital-nomad-cities.csv 对应行（保持「最后更新」= 当日）
# 2. 本地校验
python3 .github/scripts/validate_data.py
# 3. 开 PR，正文引用 issue（merge 自动关闭）
gh pr create --title "data: 应用 Issue #N（城市/字段）" --body "Closes #N"
```

注意：main 有分支保护且必需检查不在 PR 上跑，数据 PR 由 owner `--admin` 合并（与现有汇率 PR 同流程）。

## 指标

- Triage 周报停留时长：理想 < 7 天（即当周清零）。
- 有效贡献响应率：每周 triage 中 @ 致谢的比例应接近 100%。
