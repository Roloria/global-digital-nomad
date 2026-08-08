/**
 * 🌐 全球数字游民社区 · 匿名体验提交 API
 *
 * 这是一个 Cloudflare Worker（兼容任何 Workers 运行时 / Vercel Edge / Deno Deploy）。
 * 用户在网站填写「社区体验」表单 → POST 到本 API → API 用服务端持有的 GitHub PAT
 * 调用 GitHub Issues API 创建 Issue。**用户永远不需要 GitHub 账号**。
 *
 * 部署说明见 ../README.md 与本目录下 wrangler.toml。
 */

const DEFAULT_REPO = "Roloria/global-digital-nomad";
const DEFAULT_LABELS = ["community-experience", "data", "anonymous-submission"];

// 简易内存限流（per worker instance），生产可换 KV / Durable Objects
const rateMap = new Map();
const RATE_LIMIT_PER_HOUR = 10;
const RATE_WINDOW_MS = 60 * 60 * 1000;

function getClientIp(request) {
  return (
    request.headers.get("CF-Connecting-IP") ||
    request.headers.get("X-Forwarded-For")?.split(",")[0]?.trim() ||
    "unknown"
  );
}

function isRateLimited(ip) {
  const now = Date.now();
  const arr = (rateMap.get(ip) || []).filter((t) => now - t < RATE_WINDOW_MS);
  if (arr.length >= RATE_LIMIT_PER_HOUR) {
    rateMap.set(ip, arr);
    return true;
  }
  arr.push(now);
  rateMap.set(ip, arr);
  return false;
}

function json(data, init = {}) {
  const headers = new Headers(init.headers || {});
  headers.set("Content-Type", "application/json; charset=utf-8");
  return new Response(JSON.stringify(data), { ...init, headers });
}

function corsHeaders(env, request) {
  const allowed = (env.ALLOWED_ORIGIN || "https://roloria.github.io")
    .split(",")
    .map((s) => s.trim());
  const origin = request.headers.get("Origin") || "";
  const allowOrigin = allowed.includes("*")
    ? "*"
    : allowed.includes(origin)
      ? origin
      : allowed[0];

  return {
    "Access-Control-Allow-Origin": allowOrigin,
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function formatIssueBody(d) {
  const lines = [
    "## 🌐 匿名社区体验提交",
    "",
    "由社区用户在网站上填写并直接提交，无需登录。",
    "",
    "| 字段 | 值 |",
    "|---|---|",
    `| **社区** | ${d.community || "(未填)"} |`,
    `| **体验类型** | ${d.exp_type || "(未填)"} |`,
    `| **时间 / 季节** | ${d.season || "(未填)"} |`,
    `| **整体推荐度** | **${Number(d.rating || 0).toFixed(1)} / 10** |`,
    "",
    "### 👍 推荐理由",
    d.pros || "_(无)_",
    "",
    "### 👎 需要注意",
    d.cons || "_(无)_",
    "",
    "### 📝 补充信息",
    d.extra || "_(无)_",
    "",
    "---",
    "",
    `- **提交时间**: ${d.timestamp || new Date().toISOString()}`,
    `- **提交方式**: 网页表单 → Cloudflare Worker → GitHub Issues API`,
    `- **提交 IP（已脱敏到 /24）**: ${(d._clientIp || "").replace(/\.\d+$/, ".0/24") || "(未记录)"}`,
    `- **User-Agent**: ${(d._ua || "").slice(0, 200) || "(未记录)"}`,
    "",
    "> 🛡️ **匿名性**：提交者未登录 GitHub 账号。本 Issue 由本仓库维护者持有",
    "> 的 GitHub PAT（Personal Access Token）代为创建，token 不会暴露给用户。",
    "> 维护者合并 PR 到 `data/digital-nomad-communities.csv` 后即可让该体验生效。",
  ];
  return lines.join("\n");
}

function validate(d) {
  const errs = [];
  if (!d.community || typeof d.community !== "string" || d.community.length > 200) {
    errs.push("community 必填且 ≤ 200 字");
  }
  if (!d.exp_type || typeof d.exp_type !== "string") {
    errs.push("exp_type 必填");
  }
  const rating = Number(d.rating);
  if (!Number.isFinite(rating) || rating < 0 || rating > 10) {
    errs.push("rating 必须 0–10");
  }
  if (d.pros && d.pros.length > 2000) errs.push("pros ≤ 2000 字");
  if (d.cons && d.cons.length > 2000) errs.push("cons ≤ 2000 字");
  if (d.extra && d.extra.length > 2000) errs.push("extra ≤ 2000 字");
  if (d.season && d.season.length > 100) errs.push("season ≤ 100 字");
  return errs;
}

async function createGitHubIssue(data, env) {
  const repo = env.GITHUB_REPO || DEFAULT_REPO;
  const token = env.GITHUB_TOKEN;
  const labels = (env.GITHUB_LABELS || DEFAULT_LABELS.join(","))
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);

  if (!token) {
    throw new Error("server-misconfigured: GITHUB_TOKEN secret missing");
  }

  const body = formatIssueBody(data);
  const title = `[社区体验] ${(data.community || "").slice(0, 80)} — ${data.exp_type || ""}`.slice(0, 200);

  const res = await fetch(`https://api.github.com/repos/${repo}/issues`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      Accept: "application/vnd.github+json",
      "User-Agent": "global-digital-nomad-api",
      "X-GitHub-Api-Version": "2022-11-28",
    },
    body: JSON.stringify({ title, body, labels }),
  });

  if (!res.ok) {
    const txt = await res.text();
    throw new Error(`github-api-${res.status}: ${txt.slice(0, 300)}`);
  }
  const issue = await res.json();
  return { number: issue.number, url: issue.html_url, id: issue.id };
}

export default {
  async fetch(request, env) {
    const cors = corsHeaders(env, request);

    // CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { status: 204, headers: cors });
    }

    // Health check
    if (request.method === "GET" && new URL(request.url).pathname === "/health") {
      return json(
        {
          ok: true,
          service: "community-experience-api",
          github_repo: env.GITHUB_REPO || DEFAULT_REPO,
          rate_limit_per_hour: RATE_LIMIT_PER_HOUR,
        },
        { headers: cors },
      );
    }

    if (request.method !== "POST") {
      return json({ ok: false, error: "method not allowed" }, { status: 405, headers: cors });
    }

    const ip = getClientIp(request);
    if (isRateLimited(ip)) {
      return json(
        { ok: false, error: "rate_limited", retry_after_seconds: 3600 },
        { status: 429, headers: { ...cors, "Retry-After": "3600" } },
      );
    }

    let payload;
    try {
      payload = await request.json();
    } catch {
      return json({ ok: false, error: "invalid_json" }, { status: 400, headers: cors });
    }

    // 注入服务端可观测字段（仅用于 Issue 调试 / 防滥用审计，不用于追踪个人）
    payload._clientIp = ip;
    payload._ua = request.headers.get("User-Agent") || "";

    const errs = validate(payload);
    if (errs.length) {
      return json({ ok: false, error: "validation", details: errs }, { status: 400, headers: cors });
    }

    try {
      const issue = await createGitHubIssue(payload, env);
      return json(
        {
          ok: true,
          issue_number: issue.number,
          issue_url: issue.url,
        },
        { headers: cors },
      );
    } catch (e) {
      console.error("submit failed:", e.message);
      return json(
        { ok: false, error: "submit_failed", message: e.message },
        { status: 502, headers: cors },
      );
    }
  },
};
