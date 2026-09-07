# 🌐 全球数字游民社区 · 匿名提交 API

> 无需登录的「社区体验」匿名提交端点。
> 用户在 [`docs/index.html`](../docs/index.html) 填写表单 → POST 到本服务 → 服务端用 GitHub PAT 创建 Issue → 维护者从 Issue 合到 [`data/digital-nomad-communities.csv`](../data/digital-nomad-communities.csv)。

## 为什么用这个

| 方案 | 是否需要登录 | 是否需要本地存储 | 复杂度 | 成本 |
|---|---|---|---|---|
| **本服务（Cloudflare Worker）** | ❌ | ❌ | 🟢 低 | 🟢 免费 100k 请求/天 |
| GitHub Issue 直链 | ❌（但需手动点） | ❌ | 🟢 低 | 🟢 免费 |
| Google Form | ❌ | ❌ | 🟡 中 | 🟢 免费（但数据锁在 Google） |
| Formspree / Web3Forms | ❌ | ❌ | 🟢 低 | 🟡 免费层有限制 |

我们选 **Cloudflare Worker** 因为：

- 🆓 **完全免费**：Cloudflare Workers 免费层 100k 请求/天，对开源项目绰绰有余
- 🔒 **token 不暴露**：GitHub PAT 存在服务端 secret，用户永远看不到
- 🌍 **边缘网络**：全球 < 50ms 延迟
- 📦 **零运维**：不需要数据库，数据落到 GitHub Issues
- 🔍 **可审计**：所有提交都在 GitHub Issues 里可追溯
- 🛡️ **可限流**：内置每 IP 每小时 10 条上限（防止垃圾）

## 端点

```
POST https://<your-worker>.workers.dev/
Content-Type: application/json

{
  "community": "Hubud (巴厘岛 (乌布), 印尼)",
  "exp_type": "中期 (1-3 月)",
  "season": "2024-09 秋季",
  "pros": "屋顶泳池 + 24h 工位 + 周三免费啤酒社交",
  "cons": "周边餐厅中午关门早",
  "rating": 9.0,
  "extra": "实际花费 $1200/月",
  "timestamp": "2026-08-08T12:00:00.000Z"
}
```

返回成功：

```json
{
  "ok": true,
  "issue_number": 142,
  "issue_url": "https://github.com/Roloria/global-nomad-atlas/issues/142"
}
```

返回失败：

```json
{
  "ok": false,
  "error": "validation",
  "details": ["rating 必须 0–10"]
}
```

Health check：

```
GET https://<your-worker>.workers.dev/health
→ { "ok": true, "service": "community-experience-api", ... }
```

## 部署到 Cloudflare（5 分钟）

### 1. 准备 GitHub PAT

1. 访问 <https://github.com/settings/tokens?type=beta>
2. 创建 **Fine-grained PAT**，Repository access 选 `Roloria/global-nomad-atlas`，Permissions 选 `Issues: Read and Write`
3. 复制 token（只显示一次）

### 2. 部署 Worker

```bash
cd api
npm install
npx wrangler login              # 浏览器会弹出，授权 Cloudflare
npx wrangler secret put GITHUB_TOKEN
# 粘贴你的 PAT，回车
npx wrangler deploy             # 部署到 *.workers.dev
```

部署成功后会得到一个 URL，类似：

```
Published global-nomad-atlas-community-api (1.23 sec)
  https://global-nomad-atlas-community-api.<your-subdomain>.workers.dev
```

### 3. 测试

```bash
curl https://<your-worker>.workers.dev/health
# {"ok":true,"service":"community-experience-api",...}

curl -X POST https://<your-worker>.workers.dev/ \
  -H "Content-Type: application/json" \
  -d '{"community":"Hubud (test)","exp_type":"短期 (1-4 周)","rating":8.5}'
# {"ok":true,"issue_number":1,"issue_url":"..."}
```

### 4. 填到前端

打开 `docs/index.html`，找到：

```html
<!-- TODO: 配置 API -->
const COMMUNITY_API_URL = "";
```

填入你的 Worker URL：

```html
const COMMUNITY_API_URL = "https://global-nomad-atlas-community-api.<your-subdomain>.workers.dev/";
```

提交一个 PR 即可。

## 环境变量 / Secrets

| 名称 | 类型 | 说明 |
|---|---|---|
| `GITHUB_TOKEN` | **Secret** | GitHub Fine-grained PAT，需 `Issues: Write` 到本仓库 |
| `GITHUB_REPO` | Var | 默认 `Roloria/global-nomad-atlas` |
| `GITHUB_LABELS` | Var | 默认 `community-experience,data,anonymous-submission` |
| `ALLOWED_ORIGIN` | Var | CORS 白名单，逗号分隔；`*` 表示全部 |

通过 `wrangler secret put <NAME>` 设置 secret，`wrangler.toml` `[vars]` 设置变量。

## 安全说明

| 关注点 | 我们的做法 |
|---|---|
| **GitHub PAT 泄露** | 存在 Cloudflare encrypted secret，仅 Worker 可读 |
| **滥用 / 垃圾** | 每 IP 每小时 10 条上限（生产可换 KV / Turnstile） |
| **CSRF** | API 只接受 `application/json`，不能用 `<form>` 跨域提交 |
| **CORS** | 仅白名单 origin（默认 `roloria.github.io` + `localhost`） |
| **隐私** | 用户无需登录 GitHub；提交内容透明，可联系维护者删除 |
| **审计** | 所有提交落到 GitHub Issues，公开可追溯 |

## 本地开发

```bash
cd api
npm install
npm run dev
# → wrangler dev 会启动 http://localhost:8787
# 模拟环境变量：在项目根新建 .dev.vars 文件：
#   GITHUB_TOKEN=ghp_xxxxxxxx
#   GITHUB_REPO=Roloria/global-nomad-atlas
# wrangler 会自动读取 .dev.vars
```

## 架构图

```
┌──────────────┐     POST (JSON)      ┌─────────────────────┐     Bearer PAT     ┌──────────────┐
│  网站用户     │ ───────────────────► │ Cloudflare Worker   │ ────────────────► │ GitHub API   │
│  (浏览器)     │                     │ (本服务)             │                    │ /repos/.../  │
│              │ ◄────────────────── │                     │ ◄──────────────── │ issues       │
│              │   {ok:true,         │ - CORS              │   {number,url}    │              │
│              │    issue_url}       │ - 限流               │                    │ 创建 Issue    │
└──────────────┘                     │ - 校验               │                    └──────────────┘
                                     │ - 注入服务端字段      │                            │
                                     └─────────────────────┘                            ▼
                                                                       ┌──────────────────────┐
                                                                       │ GitHub Issue         │
                                                                       │ (Roloria/global-     │
                                                                       │  digital-nomad)      │
                                                                       │ 维护者 review → 合并  │
                                                                       └──────────────────────┘
                                                                                      │
                                                                                      ▼
                                                                       ┌──────────────────────┐
                                                                       │ data/digital-nomad-  │
                                                                       │ communities.csv      │
                                                                       │ (自动校验 + 网站展示)  │
                                                                       └──────────────────────┘
```

## License

MIT © Roloria
