#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
城市详情页 & 英文版站点生成器
================================
从 data/digital-nomad-cities.csv 生成（纯 stdlib，无第三方依赖）：
  1. docs/city/<slug>/index.html     × N   中文城市详情页（SEO：title/desc/canonical/hreflang/JSON-LD）
  2. docs/en/city/<slug>/index.html  × N   英文城市详情页
  3. docs/en/index.html                    英文版榜单首页（静态可爬表格）
  4. docs/index.html                       刷新 const CITY_SLUGS（主站行内「详情」链接用）
  5. docs/sitemap.xml                      重建：保留既有条目 + 城市/英文版条目（含 hreflang 互链）

幂等：重复运行输出一致（除 lastmod 用数据内「最后更新」）。CI 由 build-city-pages.yml 在 data/** 变更后自动跑。
"""
import csv
import html
import json
import os
import re
import unicodedata
from datetime import date
from pathlib import Path

REPO = os.environ.get("REPO", "Roloria/global-digital-nomad")
BASE = os.environ.get("SITE_BASE", "https://roloria.github.io/global-digital-nomad")
CSV_PATH = os.environ.get("CSV_PATH", "data/digital-nomad-cities.csv")
DOCS = Path(os.environ.get("DOCS_DIR", "docs"))

BRAND_ZH = "牛马迁移指南"
BRAND_EN = "Global Digital Nomad Cities"

DIMENSIONS = ["网络", "社群", "生活", "安全", "英语", "步行", "空气", "女性友好", "LGBTQ+", "夜生活", "安静指数", "种族包容"]
DIM_EN = {"网络": "Internet", "社群": "Community", "生活": "Cost of Living", "安全": "Safety", "英语": "English-friendly",
          "步行": "Walkability", "空气": "Air Quality", "女性友好": "Female-friendly", "LGBTQ+": "LGBTQ+",
          "夜生活": "Nightlife", "安静指数": "Quietness", "种族包容": "Inclusivity", "综合分": "Overall Score"}
REGION_EN = {"亚洲": "Asia", "欧洲": "Europe", "拉美": "LatAm", "非洲": "Africa", "中东": "Middle East"}
WEIGHTS = {"网络": 1.0, "社群": 1.2, "生活": 1.0, "安全": 1.2, "英语": 0.9, "步行": 0.7, "空气": 0.7,
           "女性友好": 0.8, "LGBTQ+": 0.6, "夜生活": 0.5, "安静指数": 0.6, "种族包容": 0.6}

CITY_EN = {
    "墨西哥城": "Mexico City", "巴厘岛 (长谷)": "Bali (Canggu)", "里斯本": "Lisbon", "巴塞罗那": "Barcelona",
    "上海": "Shanghai", "大理": "Dali", "清迈": "Chiang Mai", "北京": "Beijing", "麦德林": "Medellín",
    "杭州": "Hangzhou", "深圳": "Shenzhen", "胡志明市": "Ho Chi Minh City", "成都": "Chengdu", "曼谷": "Bangkok",
    "布宜诺斯艾利斯": "Buenos Aires", "河内": "Hanoi", "班加罗尔": "Bangalore", "第比利斯": "Tbilisi",
    "图卢姆": "Tulum", "柏林": "Berlin", "拉斯帕尔马斯": "Las Palmas", "吉隆坡": "Kuala Lumpur",
    "伊斯坦布尔": "Istanbul", "普拉亚德尔卡曼": "Playa del Carmen", "迪拜": "Dubai", "普吉": "Phuket",
    "东京": "Tokyo", "南京": "Nanjing", "西安": "Xi'an", "开普敦": "Cape Town", "里约": "Rio de Janeiro",
    "果阿": "Goa", "卡塔赫纳": "Cartagena", "布达佩斯": "Budapest", "新加坡": "Singapore", "布拉格": "Prague",
    "巴拿马城": "Panama City", "三亚": "Sanya", "昆明": "Kunming", "苏州": "Suzhou", "班斯科": "Bansko",
    "岘港": "Da Nang", "雅加达": "Jakarta", "台北": "Taipei", "克拉科夫": "Kraków", "利马": "Lima",
    "波尔图": "Porto", "首尔": "Seoul", "特内里费": "Tenerife", "雅典": "Athens", "槟城": "Penang",
    "金边": "Phnom Penh", "塔林": "Tallinn", "厦门": "Xiamen", "青岛": "Qingdao", "丽江": "Lijiang",
    "圣米格尔": "San Miguel de Allende", "内罗毕": "Nairobi", "马尼拉": "Manila", "马德拉": "Madeira",
    "斯普利特": "Split", "弗洛里亚诺波利斯": "Florianópolis", "瓦哈卡": "Oaxaca", "宿务": "Cebu",
    "约翰内斯堡": "Johannesburg", "阳朔": "Yangshuo", "蒙得维的亚": "Montevideo", "贝尔格莱德": "Belgrade",
    "卡波圣卢卡斯": "Cabo San Lucas", "暹粒": "Siem Reap", "苏梅岛": "Koh Samui", "索菲亚": "Sofia",
    "安提瓜": "Antigua Guatemala", "马拉喀什": "Marrakech", "阿布扎比": "Abu Dhabi", "塔加祖特": "Taghazout",
    "开罗": "Cairo", "基加利": "Kigali", "安吉": "Anji", "多哈": "Doha",
}

MONTH_EN = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
            7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

VISA_PHRASES = [
    ("数字游民签证", "Digital Nomad Visa"), ("自由职业者签证", "Freelancer Visa"),
    ("工作假期签证", "Working Holiday Visa"), ("退休签证", "Retirement Visa"),
    ("教育签证", "Education Visa"), ("学生签", "Student Visa"), ("旅游签", "Tourist Visa"),
    ("商务签", "Business Visa"), ("工作签证", "Work Visa"), ("工作签", "Work Visa"),
    ("长期居留", "Long-term Residence"), ("落地签", "Visa on Arrival"), ("电子签", "eVisa"),
    ("过境签", "Transit Visa"), ("长期旅游", "Long-term Tourist"), ("游民签", "Nomad Visa"),
    ("免签", "Visa-free"), ("申根", "Schengen"), ("落地", "VOA"), ("长期", "Long-term"),
    ("商务", "Business"), ("旅游", "Tourist"), ("签证", "Visa"), ("签", "Visa"),
]

CSS = """*{margin:0;padding:0;box-sizing:border-box}
:root{--bg:#faf9f5;--bg2:#f0eee6;--card:#ffffff;--text:#23272d;--text2:#5c6470;--text3:#8a929e;--border:#e5e1d8;--accent:#c96442;--good:#3d8b5f}
html{-webkit-text-size-adjust:100%}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;background:var(--bg);color:var(--text);line-height:1.6}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:880px;margin:0 auto;padding:24px 20px 60px}
.crumbs{font-size:12px;color:var(--text3);margin-bottom:18px}
.crumbs a{color:var(--text2)}
h1{font-family:Georgia,"Noto Serif SC","Songti SC",serif;font-size:32px;line-height:1.25;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.sub{color:var(--text2);font-size:14px;margin-top:6px}
.pill{display:inline-block;font-size:11px;padding:2px 9px;border:1px solid var(--border);border-radius:999px;background:var(--bg2);color:var(--text2);vertical-align:middle}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(120px,1fr));gap:10px;margin:22px 0}
.stat{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:12px 14px}
.stat .l{font-size:11px;color:var(--text3);letter-spacing:.04em;text-transform:uppercase}
.stat .v{font-size:20px;font-weight:700;margin-top:2px;font-variant-numeric:tabular-nums}
.stat .v.big{font-size:30px;color:var(--accent)}
.stat .s{font-size:11px;color:var(--text3)}
.sec{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:16px 18px;margin:14px 0}
.sec h2{font-size:15px;margin-bottom:12px}
.bar-row{display:grid;grid-template-columns:110px 1fr 44px;align-items:center;gap:10px;margin:7px 0;font-size:13px}
.bar-row .lb{color:var(--text2)}
.bar{height:8px;background:var(--bg2);border-radius:999px;overflow:hidden}
.bar i{display:block;height:100%;background:var(--accent);border-radius:999px}
.bar-row .num{text-align:right;font-variant-numeric:tabular-nums;font-weight:600}
.note{font-size:12px;color:var(--text3);line-height:1.7}
.cta{display:flex;gap:10px;flex-wrap:wrap;margin:18px 0}
.btn{display:inline-block;padding:9px 16px;border-radius:10px;font-size:13px;font-weight:600;border:1px solid var(--border);background:var(--card);color:var(--text)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:#fff}
footer{margin-top:26px;padding-top:16px;border-top:1px solid var(--border);font-size:12px;color:var(--text3);display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap}
table{width:100%;border-collapse:collapse;font-size:13px}
th{font-size:11px;color:var(--text3);text-align:left;padding:8px 10px;border-bottom:2px solid var(--border);white-space:nowrap}
td{padding:9px 10px;border-bottom:1px solid var(--border);font-variant-numeric:tabular-nums}
tr:hover td{background:var(--bg2)}
tr.top td{background:rgba(201,100,66,.06)}
td.r,th.r{text-align:right}
.pagenav{display:flex;justify-content:space-between;gap:10px;margin-top:20px;font-size:13px}
@media(max-width:600px){h1{font-size:26px}.bar-row{grid-template-columns:92px 1fr 40px}}
"""


def slugify(en_name: str) -> str:
    s = unicodedata.normalize("NFKD", en_name).encode("ascii", "ignore").decode()
    s = s.replace("'", "").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def en_season(zh: str) -> str:
    if "全年" in zh:
        return "Year-round"
    def rep(m):
        return MONTH_EN.get(int(m.group(1)), m.group(1))
    return re.sub(r"(\d{1,2})月", rep, zh).replace("-", "–")


def en_visa(zh: str) -> str:
    s = zh
    for zh_p, en_p in VISA_PHRASES:
        s = s.replace(zh_p, en_p)
    s = re.sub(r"(\d+)\s*月", r"\1-month", s)
    s = re.sub(r"(\d+)\s*年", r"\1-year", s)
    s = re.sub(r"(\d+)\s*天", r"\1-day", s)
    return s


def fmt_int(v) -> str:
    return f"{int(v):,}"


def jsonld(*objects) -> str:
    return json.dumps(list(objects), ensure_ascii=False, separators=(",", ":"))


def load_rows():
    with open(CSV_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["综合分_f"] = float(r["综合分"])
        r["_en"] = CITY_EN.get(r["城市"])
        if not r["_en"]:
            raise SystemExit(f"❌ CITY_EN 缺少城市: {r['城市']} —— 请在 CITY_EN 字典补齐后重跑")
        r["_slug"] = slugify(r["_en"])
    slugs = [r["_slug"] for r in rows]
    assert len(slugs) == len(set(slugs)), "slug 冲突：" + str([s for s in slugs if slugs.count(s) > 1])
    rows.sort(key=lambda r: int(r["排名"]))
    return rows


def head_block(lang, title, desc, url_path, updated, extra_links=""):
    url = f"{BASE}{url_path}"
    zh_url = f"{BASE}{url_path}" if lang == "zh" else f"{BASE}{url_path.replace('/en', '', 1)}"
    en_url = f"{BASE}/en{url_path}" if lang == "zh" else f"{BASE}{url_path}"
    return f"""<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="zh-CN" href="{zh_url}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="x-default" href="{zh_url}">
<link rel="icon" href="{BASE}/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta name="robots" content="index,follow">
{extra_links}<style>{CSS}</style>
<script type="application/ld+json">{jsonld(
    {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "牛马迁移指南" if lang == "zh" else BRAND_EN, "item": BASE + ("/" if lang == "zh" else "/en/")},
        {"@type": "ListItem", "position": 2, "name": "城市榜单" if lang == "zh" else "City Index",
         "item": BASE + ("/#cities" if lang == "zh" else "/en/")},
        {"@type": "ListItem", "position": 3, "name": url_path.split("/")[-2].title() if lang == "en" else title.split("数字游民")[0]}]},
    {"@type": "WebPage", "name": title, "description": desc, "url": url,
     "inLanguage": "zh-CN" if lang == "zh" else "en",
     "isPartOf": {"@type": "WebSite", "name": BRAND_ZH if lang == "zh" else BRAND_EN, "url": BASE + "/"},
     "dateModified": updated})}</script>
</head>"""


def bars_block(row, lang):
    out = []
    for dim in DIMENSIONS:
        v = float(row[dim])
        label = DIM_EN[dim] if lang == "en" else dim
        out.append(
            f'<div class="bar-row"><span class="lb">{html.escape(label)}</span>'
            f'<span class="bar"><i style="width:{v * 10:.0f}%"></i></span><span class="num">{v:.1f}</span></div>')
    return "\n".join(out)


def city_page(row, prev_row, next_row, lang) -> str:
    zh = lang == "zh"
    city, country = row["城市"], row["国家"]
    en_name, slug = row["_en"], row["_slug"]
    name = en_name if zh is False else city
    cost, nomads, score, rank = int(row["月成本 (USD)"]), int(row["游民数"]), row["综合分"], row["排名"]
    region = REGION_EN[row["区域"]] if not zh else row["区域"]
    updated = row["最后更新"]
    season = en_season(row["最佳季节"]) if not zh else row["最佳季节"]
    visa = en_visa(row["签证"]) if not zh else row["签证"]

    if zh:
        title = f"{city}数字游民指南 · 月成本 ${cost:,} · 综合分 {score}/10 | {BRAND_ZH}"
        desc = (f"{city}（{country}）数字游民真实画像：月成本约 ${cost:,}，{fmt_int(nomads)} 名游民聚集，"
                f"综合分 {score}/10（总榜第 {rank} 名）。网络、安全、生活成本等 12 维评分、签证速览与最佳季节 —— 数据开源、可复算。")
        url_path = f"/city/{slug}/"
        h1_extra = f'<span class="pill">{country} · {region}</span>'
        stat_labels = ("综合分", "总榜排名", "月成本 (USD)", "游民数", "年均气温", "最佳季节", "最后更新")
        dim_h = "12 维评分明细"
        visa_h = "🛂 签证速览"
        visa_note = "签证政策几乎每月都在变，以下仅为起点，正式申请请以当地移民局官网为准。"
        data_note = (f"综合分 = 12 维评分按公开权重加权（社群/安全 1.2 权重最高），公式见评分标准。"
                     f"本页由开源数据集自动生成，城市数据最后更新于 <b>{updated}</b>。发现过期？欢迎直接改进。")
        cta = ('<a class="btn primary" href="../../#cities">← 返回总榜对比</a>'
               f'<a class="btn" href="https://docs.qq.com/sheet/DREppWERNRWdwcXRR">✏️ 改进{city}的数据</a>'
               f'<a class="btn" href="https://github.com/{REPO}">GitHub 数据集</a>')
        foot = f'<span>{BRAND_ZH} · 开源数字游民城市数据库</span><a href="{BASE}/en/city/{slug}/">English →</a>'
        crumbs = f'<div class="crumbs"><a href="../../">首页</a> / <a href="../../#cities">城市榜单</a> / {city}</div>'
    else:
        title = f"{en_name} Digital Nomad Guide · ${cost:,}/mo · Score {score}/10 | {BRAND_EN}"
        desc = (f"{en_name}, {row['国家(英)']}: monthly cost ≈ ${cost:,}, {fmt_int(nomads)} nomads, "
                f"overall score {score}/10 (rank #{rank} of 80). 12-dimension ratings — internet, safety, cost of living and more — "
                f"plus visa snapshot and best season. Open data, verifiable formula.")
        url_path = f"/en/city/{slug}/"
        h1_extra = f'<span class="pill">{row["国家(英)"]} · {region}</span>'
        stat_labels = ("Overall", "Rank", "Monthly Cost", "Nomads", "Avg Temp", "Best Season", "Last Update")
        dim_h = "12-Dimension Ratings"
        visa_h = "🛂 Visa Snapshot"
        visa_note = "Visa rules change almost monthly — treat this as a starting point and confirm with the official immigration authority."
        data_note = (f"Overall score = weighted average of 12 dimensions (community & safety weigh 1.2, formula public). "
                     f"This page is generated from the open dataset; city data last updated <b>{updated}</b>. Found something stale? Improvements welcome.")
        cta = ('<a class="btn primary" href="../../#ranking">← Back to full ranking</a>'
               f'<a class="btn" href="https://docs.qq.com/sheet/DREppWERNRWdwcXRR">✏️ Improve {en_name} data</a>'
               f'<a class="btn" href="https://github.com/{REPO}">GitHub Dataset</a>')
        foot = f'<span>{BRAND_EN} · Open digital-nomad city database</span><a href="{BASE}/city/{slug}/">中文版 →</a>'
        crumbs = f'<div class="crumbs"><a href="../../">Home</a> / <a href="../../#ranking">City Index</a> / {en_name}</div>'

    nav = []
    if prev_row:
        p = f"../{prev_row['_slug']}/"
        nav.append(f'<a href="{p}">← {prev_row["_en"] if not zh else prev_row["城市"]}</a>')
    if next_row:
        n = f"../{next_row['_slug']}/"
        nav.append(f'<a href="{n}">{next_row["_en"] if not zh else next_row["城市"]} →</a>')
    pagenav = f'<div class="pagenav">{"".join(nav)}</div>' if nav else ""

    stat = lambda l, v, s="", big=False: (f'<div class="stat"><div class="l">{l}</div>'
                                          f'<div class="v{" big" if big else ""}">{v}</div>' + (f'<div class="s">{s}</div>' if s else "") + "</div>")
    stats_html = (
        stat(stat_labels[0], f"{score}/10", ("加权综合分" if zh else "Weighted score"), big=True)
        + stat(stat_labels[1], f"#{rank}", "共 80 城" if zh else "of 80 cities")
        + stat(stat_labels[2], f"${cost:,}", "≈ ¥" + f"{cost * 6.74:,.0f}")
        + stat(stat_labels[3], fmt_int(nomads))
        + stat(stat_labels[4], f'{row["年均气温 (°C)"]}°C')
        + stat(stat_labels[5], season)
        + stat(stat_labels[6], updated)
    )

    h2 = dim_h if zh else dim_h
    body = f"""<!DOCTYPE html>
<html lang="{'zh-CN' if zh else 'en'}">
{head_block(lang, title, desc, url_path, updated)}
<body><div class="wrap">
{crumbs}
<h1><span>{row["国旗"]}</span> {name} {h1_extra}</h1>
<div class="sub">{'数字游民城市真实画像 · 开源数据，公式可复算' if zh else 'A data-driven snapshot for remote workers · Open data, verifiable formula'}</div>
<div class="stats">{stats_html}</div>
<div class="sec"><h2>{dim_h}</h2>
{bars_block(row, lang)}
</div>
<div class="sec"><h2>{visa_h}</h2>
<p style="font-size:14px">{html.escape(visa)}</p>
<p class="note" style="margin-top:8px">{visa_note}</p>
</div>
<div class="sec"><p class="note">{data_note}</p></div>
<div class="cta">{cta}</div>
{pagenav}
<footer>{foot}</footer>
</div></body></html>"""
    return body


def en_index(rows) -> str:
    now = max(r["最后更新"] for r in rows)
    t = f"Global Digital Nomad Cities Index · 80 Cities × 12 Dimensions · Open Data | {BRAND_EN}"
    d = ("Open, community-maintained ranking of 80 digital-nomad cities across 40 countries: monthly cost, "
         "internet, safety, community and more, scored 0–10 with a public formula. English edition of 牛马迁移指南.")
    head = head_block("en", t, d, "/en/", now)

    trs = []
    for i, r in enumerate(rows):
        cls = ' class="top"' if i < 5 else ""
        trs.append(
            f'<tr{cls}><td class="r">{r["排名"]}</td>'
            f'<td><a href="city/{r["_slug"]}/">{r["_en"]}</a> {r["国旗"]}</td>'
            f'<td>{html.escape(r["国家(英)"])}</td><td>{REGION_EN[r["区域"]]}</td>'
            f'<td class="r">{fmt_int(r["游民数"])}</td><td class="r">${int(r["月成本 (USD)"]):,}</td>'
            f'<td class="r"><b style="color:var(--accent)">{r["综合分"]}</b></td><td>{r["最后更新"]}</td></tr>')
    table = "\n".join(trs)

    weights = " · ".join(f"{DIM_EN[k]} ×{v}" for k, v in WEIGHTS.items())
    body = f"""<!DOCTYPE html>
<html lang="en">
{head}
<body><div class="wrap">
<div class="crumbs"><a href="../">牛马迁移指南</a> / English</div>
<h1>🌍 Global Digital Nomad Cities Index</h1>
<div class="sub">{len(rows)} cities · 40 countries · 12 dimensions · community-maintained open data. <a href="../">中文交互版 →</a></div>
<div class="stats">
  <div class="stat"><div class="l">Cities</div><div class="v big">{len(rows)}</div></div>
  <div class="stat"><div class="l">Countries</div><div class="v">40</div></div>
  <div class="stat"><div class="l">Dimensions</div><div class="v">12</div></div>
  <div class="stat"><div class="l">Data License</div><div class="v" style="font-size:14px">Open (GitHub)</div></div>
</div>
<div class="sec"><h2>About this ranking</h2>
<p class="note">Every city is scored 0–10 on {len(DIMENSIONS)} dimensions by community consensus; the overall score is a public weighted
average — <b>{html.escape(weights)}</b>. Anyone can propose changes: edit the shared spreadsheet, open a GitHub PR, or file an issue.
Every change is recorded in git history and reflected on these pages. Cost figures are monthly budget estimates in USD.</p>
</div>
<div class="sec" id="ranking"><h2>Full Ranking ({len(rows)} cities)</h2>
<table>
<thead><tr><th class="r">#</th><th>City</th><th>Country</th><th>Region</th><th class="r">Nomads</th><th class="r">Cost / mo</th><th class="r">Score</th><th>Updated</th></tr></thead>
<tbody>
{table}
</tbody></table>
</div>
<div class="sec"><h2>FAQ</h2>
<p class="note"><b>How is the score computed?</b> Weighted mean of 12 sub-scores (community &amp; safety weigh 1.2); the formula is public and re-computable from the CSV.<br>
<b>How fresh is the data?</b> Every row carries a 📅 last-updated date, auto-derived from git history and refreshed via daily community syncs.<br>
<b>Can I contribute?</b> Yes — the dataset is fully open: <a href="https://github.com/{REPO}">GitHub</a> ·
<a href="https://docs.qq.com/sheet/DREppWERNRWdwcXRR">shared spreadsheet</a> · or <a href="../">browse the Chinese interactive edition</a>.</p>
</div>
<footer><span>{BRAND_EN} · part of <a href="../">牛马迁移指南</a></span><span>Data as of {now} · <a href="https://github.com/{REPO}">open source</a></span></footer>
</div></body></html>"""
    return body


SITEMAP_MARKER_KEEP = "/city/"  # generated entries carry these path fragments


def rebuild_sitemap(rows):
    sitemap_path = DOCS / "sitemap.xml"
    kept = []
    if sitemap_path.exists():
        text = sitemap_path.read_text(encoding="utf-8")
        for block in re.findall(r"<url>.*?</url>", text, re.S):
            m = re.search(r"<loc>(.*?)</loc>", block)
            if not m:
                continue
            loc = m.group(1)
            if "/city/" in loc or loc.rstrip("/").endswith("/en"):
                continue  # generated entries are rebuilt below
            kept.append(block.rstrip())

    today = max(r["最后更新"] for r in rows)
    gen = []
    for r in rows:
        slug, lm = r["_slug"], r["最后更新"]
        zh_url, en_url = f"{BASE}/city/{slug}/", f"{BASE}/en/city/{slug}/"
        gen.append(f"""  <url>
    <loc>{zh_url}</loc>
    <lastmod>{lm}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <xhtml:link rel="alternate" hreflang="zh-CN" href="{zh_url}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{zh_url}"/>
  </url>""")
        gen.append(f"""  <url>
    <loc>{en_url}</loc>
    <lastmod>{lm}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
    <xhtml:link rel="alternate" hreflang="zh-CN" href="{zh_url}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{zh_url}"/>
  </url>""")
    en_home = f"""  <url>
    <loc>{BASE}/en/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
    <xhtml:link rel="alternate" hreflang="zh-CN" href="{BASE}/"/>
    <xhtml:link rel="alternate" hreflang="en" href="{BASE}/en/"/>
    <xhtml:link rel="alternate" hreflang="x-default" href="{BASE}/"/>
  </url>"""
    sitemap_path.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml"\n'
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n\n'
        + "\n\n".join(kept + [en_home] + gen) + "\n\n</urlset>\n", encoding="utf-8")
    return len(kept) + 1 + len(gen)


def refresh_index_slugs(rows):
    """刷新主站 docs/index.html 的 const CITY_SLUGS = {...};（无则插入到 CITIES_DATA 前）。"""
    p = DOCS / "index.html"
    html_text = p.read_text(encoding="utf-8")
    mapping = "{%s}" % ",".join(f'"{r["城市"]}": "{r["_slug"]}"' for r in rows)
    new_const = f"const CITY_SLUGS = {mapping};"
    if re.search(r"const CITY_SLUGS\s*=\s*\{[^}]*\};", html_text):
        html_text = re.sub(r"const CITY_SLUGS\s*=\s*\{[^}]*\};", new_const, html_text)
    else:
        html_text = html_text.replace("const CITIES_DATA", new_const + "\nconst CITIES_DATA", 1)
    p.write_text(html_text, encoding="utf-8")


def prune_stale_city_pages(rows):
    """删除已不在数据集中的城市目录，防残留。"""
    valid_zh = {(DOCS / "city" / r["_slug"]) for r in rows}
    valid_en = {(DOCS / "en" / "city" / r["_slug"]) for r in rows}
    for base, valid in ((DOCS / "city", valid_zh), (DOCS / "en" / "city", valid_en)):
        if not base.exists():
            continue
        for d in base.iterdir():
            if d.is_dir() and d not in valid:
                import shutil
                shutil.rmtree(d)
                print(f"  🗑 移除过期城市页: {d}")


def main():
    rows = load_rows()
    print(f"📥 {len(rows)} 城 · 基准 URL {BASE}")

    zh_dir, en_dir = DOCS / "city", DOCS / "en" / "city"
    zh_dir.mkdir(parents=True, exist_ok=True)
    en_dir.mkdir(parents=True, exist_ok=True)
    (DOCS / "en").mkdir(exist_ok=True)

    for i, r in enumerate(rows):
        prev_r = rows[i - 1] if i > 0 else None
        next_r = rows[i + 1] if i < len(rows) - 1 else None
        (zh_dir / r["_slug"]).mkdir(exist_ok=True)
        (zh_dir / r["_slug"] / "index.html").write_text(city_page(r, prev_r, next_r, "zh"), encoding="utf-8")
        (en_dir / r["_slug"]).mkdir(exist_ok=True)
        (en_dir / r["_slug"] / "index.html").write_text(city_page(r, prev_r, next_r, "en"), encoding="utf-8")
    print(f"✅ 城市详情页 × {len(rows) * 2}（中/英）")

    (DOCS / "en" / "index.html").write_text(en_index(rows), encoding="utf-8")
    print("✅ 英文版首页 docs/en/index.html")

    refresh_index_slugs(rows)
    print("✅ 主站 CITY_SLUGS 已刷新")
    prune_stale_city_pages(rows)

    n = rebuild_sitemap(rows)
    print(f"✅ sitemap.xml 重建：{n} 条 URL")

    # 自检：hreflang 指向的文件必须存在
    for r in rows[:0]:
        pass
    missing = [r["城市"] for r in rows
               if not (zh_dir / r["_slug"] / "index.html").exists() or not (en_dir / r["_slug"] / "index.html").exists()]
    if missing:
        raise SystemExit(f"❌ 生成缺失: {missing}")
    print("✅ 自检通过：全部 hreflang 目标存在")


if __name__ == "__main__":
    main()
