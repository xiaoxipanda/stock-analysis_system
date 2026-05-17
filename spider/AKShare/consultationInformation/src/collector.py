"""
文章采集模块
从新闻链接抓取完整正文，保存为本地 HTML 富文本文件
"""
import os
import re
import textwrap
from datetime import datetime

import requests
from bs4 import BeautifulSoup

ARTICLE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "articles")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def _fetch_article(url, timeout=15):
    """抓取网页并尝试提取正文内容"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        r.encoding = r.apparent_encoding or "utf-8"
    except Exception as e:
        return None, f"请求失败: {e}"

    soup = BeautifulSoup(r.text, "html.parser")

    # 按优先级尝试选择器
    selectors = [
        "#ContentBody",
        ".article-body",
        ".article_content",
        "article",
        ".newsContent",
        ".news-txt",
        ".content",
        ".body",
    ]
    content_el = None
    for sel in selectors:
        content_el = soup.select_one(sel)
        if content_el and len(content_el.get_text(strip=True)) > 100:
            break

    if content_el is None:
        # 退而求其次，取 body 内纯文本
        body = soup.find("body")
        raw = body.get_text(separator="\n") if body else r.text
        raw = raw.strip()
        return raw, None

    raw_html = str(content_el)
    return raw_html, None


def _make_html(title, source, date_str, url, body_html):
    """生成带样式的富文本 HTML 文件"""
    css = textwrap.dedent("""\
        body {
            font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
            max-width: 780px; margin: 40px auto; padding: 0 20px;
            color: #333; line-height: 1.85;
        }
        .meta { color: #888; font-size: 14px; margin-bottom: 24px; border-bottom: 1px solid #eee; padding-bottom: 16px; }
        .meta .source { background: #f0f0f0; padding: 2px 8px; border-radius: 4px; }
        .meta a { color: #2563eb; }
        img { max-width: 100%; height: auto; }
        p { margin: 14px 0; }
        blockquote {
            border-left: 3px solid #ddd; padding: 8px 16px; margin: 16px 0;
            color: #666; background: #fafafa;
        }
    """)

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<h1>{title}</h1>
<div class="meta">
    <span class="source">{source}</span> &nbsp;
    <span>{date_str}</span> &nbsp;
    <a href="{url}" target="_blank">原文链接</a>
</div>
<div class="content">
{body_html}
</div>
</body>
</html>"""


def collect_news_articles(max_articles=20):
    """从 stock_news_em 抓取完整新闻文章，保存为 HTML"""
    import akshare as ak

    try:
        df = ak.stock_news_em()
    except Exception as e:
        print(f"获取新闻列表失败: {e}")
        return 0

    os.makedirs(ARTICLE_DIR, exist_ok=True)
    saved = 0

    for i, row in df.head(max_articles).iterrows():
        title = str(row.get("新闻标题", "")).strip()
        url = str(row.get("新闻链接", "")).strip()
        source = str(row.get("文章来源", "")).strip()
        date_str = str(row.get("发布时间", "")).strip()

        if not url or not url.startswith("http"):
            continue

        # 安全文件名
        safe_title = re.sub(r'[\\/*?:"<>|]', "", title)[:60]
        tag = datetime.now().strftime("%Y%m%d")
        filename = f"{tag}_{safe_title}.html"
        filepath = os.path.join(ARTICLE_DIR, filename)

        # 跳过已存在的文件
        if os.path.exists(filepath):
            continue

        print(f"[{saved+1}/{max_articles}] 抓取: {title[:40]}...")
        body, err = _fetch_article(url)
        if err:
            print(f"  ⚠ {err}")
            continue

        html = _make_html(title, source, date_str, url, body)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        saved += 1
        print(f"  ✓ {filepath}")

    print(f"\n共保存 {saved} 篇文章到 {ARTICLE_DIR}")
    return saved


def collect_notice_articles(symbol="000002", max_articles=20):
    """从 stock_notice_report 抓取公告内容"""
    import akshare as ak

    try:
        df = ak.stock_notice_report(symbol=symbol)
    except Exception as e:
        print(f"获取公告列表失败: {e}")
        return 0

    os.makedirs(ARTICLE_DIR, exist_ok=True)
    saved = 0

    for i, row in df.head(max_articles).iterrows():
        title = str(row.get("公告标题", "")).strip()
        url = ""
        for col in df.columns:
            if "链接" in col or "url" in col.lower() or "href" in col.lower():
                url = str(row.get(col, "")).strip()
                break

        source = str(row.get("公告标题", "")).strip()[:30]
        date_str = str(row.get("公告时间", "")).strip()

        if not url or not url.startswith("http"):
            continue

        safe_title = re.sub(r'[\\/*?:"<>|]', "", title)[:60]
        tag = datetime.now().strftime("%Y%m%d")
        filename = f"notice_{tag}_{safe_title}.html"
        filepath = os.path.join(ARTICLE_DIR, filename)

        if os.path.exists(filepath):
            continue

        print(f"[{saved+1}/{max_articles}] 抓取: {title[:40]}...")
        body, err = _fetch_article(url)
        if err:
            print(f"  ⚠ {err}")
            continue

        html = _make_html(title, "公告", date_str, url, body)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        saved += 1
        print(f"  ✓ {filepath}")

    print(f"\n共保存 {saved} 条公告到 {ARTICLE_DIR}")
    return saved


def collect_report_articles(max_articles=10):
    """从 stock_research_report_em 获取研报"""
    import akshare as ak

    try:
        df = ak.stock_research_report_em(symbol="000858")
    except Exception as e:
        print(f"获取研报列表失败: {e}")
        return 0

    os.makedirs(ARTICLE_DIR, exist_ok=True)
    saved = 0

    for i, row in df.head(max_articles).iterrows():
        title = str(row.get("股票简称", "")).strip() + " 研报"
        source = str(row.get("机构名称", "")).strip()
        date_str = str(row.get("评级日期", "")).strip()
        rating = str(row.get("最新评级", "")).strip()
        target = str(row.get("目标价", "")).strip()

        # 研报一般没有直接链接，生成摘要 HTML
        body_html = f"""<p><strong>评级:</strong> {rating}</p>
<p><strong>目标价:</strong> {target}</p>
<p><strong>机构:</strong> {source}</p>
<p><strong>日期:</strong> {date_str}</p>
<p>（研报正文需从东方财富等平台查看）</p>"""

        safe_title = re.sub(r'[\\/*?:"<>|]', "", title)[:60]
        tag = datetime.now().strftime("%Y%m%d")
        filename = f"report_{tag}_{safe_title}.html"
        filepath = os.path.join(ARTICLE_DIR, filename)

        if os.path.exists(filepath):
            continue

        html = _make_html(title, source, date_str, "", body_html)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
        saved += 1
        print(f"  ✓ {filepath}")

    print(f"\n共保存 {saved} 份研报到 {ARTICLE_DIR}")
    return saved
