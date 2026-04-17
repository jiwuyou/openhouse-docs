from __future__ import annotations

from html import escape
from pathlib import Path
import re
import shutil

from markdown_it import MarkdownIt


REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"
SITE_DIR = REPO_ROOT / "site"

TITLE_MAP = {
    "README.md": "OpenHouse 文档首页",
    "START_HERE.md": "起始说明",
    "USER_GUIDE.md": "用户使用说明",
    "AGENT_GUIDE.md": "AI 使用说明",
    "PATHS_AND_PORTS.md": "路径与端口",
    "OFFICIAL_RULES.md": "官方规则",
    "FAQ.md": "常见问题",
    "TROUBLESHOOTING.md": "排障说明",
    "AI_BOOTSTRAP_PROMPT.md": "AI 引导提示词",
    "ENV_SKILL.md": "环境技能说明",
}

DOC_ORDER = [
    "README.md",
    "START_HERE.md",
    "USER_GUIDE.md",
    "AGENT_GUIDE.md",
    "PATHS_AND_PORTS.md",
    "OFFICIAL_RULES.md",
    "FAQ.md",
    "TROUBLESHOOTING.md",
    "AI_BOOTSTRAP_PROMPT.md",
    "ENV_SKILL.md",
]

CSS = """
:root {
  --bg: #f4ead1;
  --panel: #fffaf0;
  --line: #d7c9ab;
  --text: #2a2a24;
  --muted: #6d6a5d;
  --link: #355c4a;
  --link-hover: #234033;
  --code-bg: #efe5cc;
}
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: var(--bg); color: var(--text); }
body {
  font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  line-height: 1.7;
}
.layout {
  max-width: 1180px;
  margin: 0 auto;
  padding: 24px;
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  gap: 24px;
}
.sidebar, .content {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 18px;
  box-shadow: 0 12px 32px rgba(97, 82, 42, 0.08);
}
.sidebar {
  padding: 20px 18px;
  position: sticky;
  top: 24px;
  align-self: start;
}
.brand {
  font-size: 28px;
  font-weight: 700;
  margin: 0 0 4px 0;
}
.subtitle {
  margin: 0 0 18px 0;
  color: var(--muted);
  font-size: 14px;
}
.nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.nav a {
  text-decoration: none;
  color: var(--text);
  padding: 10px 12px;
  border-radius: 12px;
  border: 1px solid transparent;
}
.nav a:hover {
  border-color: var(--line);
  background: rgba(215, 201, 171, 0.2);
}
.nav a.active {
  background: #e8ddc1;
  border-color: #ccb98b;
  color: #21352d;
  font-weight: 700;
}
.content {
  padding: 30px 34px;
  min-width: 0;
}
h1, h2, h3, h4 { line-height: 1.25; color: #1f261d; }
h1 { font-size: 2rem; margin-top: 0; }
h2 { margin-top: 2rem; padding-top: 0.2rem; border-top: 1px solid #eadfc3; }
a { color: var(--link); }
a:hover { color: var(--link-hover); }
img {
  max-width: 100%;
  height: auto;
  border-radius: 16px;
  border: 1px solid #decfad;
  background: #fbf5e7;
  display: block;
}
pre, code {
  font-family: "JetBrains Mono", "SFMono-Regular", Consolas, monospace;
}
code {
  background: var(--code-bg);
  padding: 0.15rem 0.4rem;
  border-radius: 6px;
}
pre {
  background: #efe4c7;
  border: 1px solid #dfcfaa;
  border-radius: 12px;
  padding: 14px;
  overflow-x: auto;
}
blockquote {
  margin: 1.2rem 0;
  padding: 0.6rem 1rem;
  border-left: 4px solid #b79d69;
  background: #fbf5e7;
  color: #4f4b40;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 1rem 0;
}
th, td {
  border: 1px solid #decfad;
  padding: 0.7rem;
  text-align: left;
}
th { background: #f2e8ce; }
.footer {
  margin-top: 2rem;
  color: var(--muted);
  font-size: 13px;
}
.code-wrap {
  position: relative;
}
.copy-button {
  position: absolute;
  top: 10px;
  right: 10px;
  border: 1px solid #ccb98b;
  background: #fff8ea;
  color: #2a2a24;
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 12px;
  cursor: pointer;
}
.copy-button:hover {
  background: #f2e5c8;
}
.copy-button.copied {
  background: #dcebdc;
  border-color: #8cab8c;
}
.entry-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  margin: 24px 0 8px 0;
}
.entry-card {
  display: block;
  text-decoration: none;
  color: var(--text);
  background: linear-gradient(180deg, #fff8ea, #f8efd9);
  border: 1px solid #d9c8a2;
  border-radius: 18px;
  padding: 22px 20px;
  box-shadow: 0 10px 24px rgba(97, 82, 42, 0.08);
}
.entry-card:hover {
  transform: translateY(-2px);
  border-color: #b89d67;
}
.entry-title {
  margin: 0 0 10px 0;
  font-size: 1.3rem;
  font-weight: 700;
}
.entry-body {
  margin: 0;
  color: var(--muted);
}
.entry-meta {
  margin-top: 14px;
  color: var(--link);
  font-weight: 700;
}
@media (max-width: 920px) {
  .layout {
    grid-template-columns: 1fr;
    padding: 14px;
  }
  .sidebar {
    position: static;
  }
  .content {
    padding: 20px;
  }
  .entry-grid {
    grid-template-columns: 1fr;
  }
}
"""

SCRIPT = """
<script>
document.addEventListener("DOMContentLoaded", function () {
  var isUserGuide = document.body.dataset.page === "user-guide";
  document.querySelectorAll("pre > code").forEach(function (codeBlock) {
    var pre = codeBlock.parentElement;
    var wrapper = document.createElement("div");
    wrapper.className = "code-wrap";
    pre.parentNode.insertBefore(wrapper, pre);
    wrapper.appendChild(pre);

    var button = document.createElement("button");
    button.className = "copy-button";
    button.type = "button";
    button.textContent = isUserGuide ? "复制给 AI" : "复制";
    button.addEventListener("click", async function () {
      var idleText = isUserGuide ? "复制给 AI" : "复制";
      try {
        await navigator.clipboard.writeText(codeBlock.innerText);
        button.textContent = "已复制";
        button.classList.add("copied");
        window.setTimeout(function () {
          button.textContent = idleText;
          button.classList.remove("copied");
        }, 1800);
      } catch (error) {
        button.textContent = "复制失败";
        window.setTimeout(function () {
          button.textContent = idleText;
        }, 1800);
      }
    });
    wrapper.appendChild(button);
  });
});
</script>
"""


def page_title(path: Path) -> str:
    return TITLE_MAP.get(path.name, path.stem.replace("_", " "))


def sort_docs(paths: list[Path]) -> list[Path]:
    order_index = {name: index for index, name in enumerate(DOC_ORDER)}
    return sorted(paths, key=lambda path: (order_index.get(path.name, 999), path.name))


def rewrite_links(markdown_text: str) -> str:
    markdown_text = re.sub(r"\(([^)]+)\.md(#.*?)?\)", r"(\1.html\2)", markdown_text)
    markdown_text = re.sub(r'href="([^"]+)\.md(#.*?)?"', r'href="\1.html\2"', markdown_text)
    return markdown_text


def build_nav(paths: list[Path], current_name: str) -> str:
    links = []
    for path in paths:
        href = "index.html" if path.name == "README.md" else f"{path.stem}.html"
        active = " active" if path.name == current_name else ""
        links.append(
            f'<a class="{active.strip()}" href="{href}">{escape(page_title(path))}</a>'
            if active
            else f'<a href="{href}">{escape(page_title(path))}</a>'
        )
    return "\n".join(links)


def render_homepage() -> str:
    body_html = """
<h1>OpenHouse 文档首页</h1>
<p>请选择你当前的入口。普通用户直接进入“我是用户”，运行在系统里的 AI 进入“我是 AI”。</p>
<div class="entry-grid">
  <a class="entry-card" href="USER_GUIDE.html">
    <h2 class="entry-title">我是用户</h2>
    <p class="entry-body">你只需要复制一段固定的话，再粘贴给 AI。这里不会要求你理解技术细节。</p>
    <div class="entry-meta">进入复制粘贴说明</div>
  </a>
  <a class="entry-card" href="START_HERE.html">
    <h2 class="entry-title">我是 AI</h2>
    <p class="entry-body">先确认运行环境，再继续读取路径、端口、规则和技能说明。这部分主要给 AI / agent 使用。</p>
    <div class="entry-meta">进入 AI 起始说明</div>
  </a>
</div>
<h2>继续阅读建议</h2>
<ul>
  <li>普通用户：优先看 <code>用户使用说明</code>，照着复制粘贴即可。</li>
  <li>AI：先看 <code>起始说明</code>，再看 <code>AI 使用说明</code> 与 <code>路径与端口</code>。</li>
  <li><code>排障说明</code> 主要给 AI 使用，普通用户不需要先看。</li>
</ul>
"""
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OpenHouse 文档首页</title>
  <style>{CSS}</style>
</head>
<body data-page="home">
  <div class="layout">
    <aside class="sidebar">
      <h1 class="brand">OpenHouse</h1>
      <p class="subtitle">本机产品文档服务，用户说明优先使用中文。</p>
      <nav class="nav">
        <a class="active" href="index.html">文档首页</a>
        <a href="USER_GUIDE.html">用户使用说明</a>
        <a href="START_HERE.html">起始说明</a>
        <a href="AGENT_GUIDE.html">AI 使用说明</a>
        <a href="PATHS_AND_PORTS.html">路径与端口</a>
      </nav>
    </aside>
    <main class="content">
      {body_html}
      <div class="footer">当前页面源文件：<code>README.md</code></div>
    </main>
  </div>
</body>
</html>
"""


def render_page(md: MarkdownIt, all_docs: list[Path], current_doc: Path) -> str:
    body_html = md.render(rewrite_links(current_doc.read_text(encoding="utf-8")))
    nav_html = build_nav(all_docs, current_doc.name)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(page_title(current_doc))}</title>
  <style>{CSS}</style>
</head>
<body data-page="{ 'user-guide' if current_doc.name == 'USER_GUIDE.md' else 'doc' }">
  <div class="layout">
    <aside class="sidebar">
      <h1 class="brand">OpenHouse</h1>
      <p class="subtitle">本机产品文档服务，用户说明优先使用中文。</p>
      <nav class="nav">
        {nav_html}
      </nav>
    </aside>
    <main class="content">
      {body_html}
      <div class="footer">当前页面源文件：<code>{escape(current_doc.name)}</code></div>
    </main>
  </div>
  {SCRIPT}
</body>
</html>
"""


def main() -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    assets_src = DOCS_DIR / "assets"
    assets_dst = SITE_DIR / "assets"
    if assets_dst.exists():
        shutil.rmtree(assets_dst)
    if assets_src.exists():
        shutil.copytree(assets_src, assets_dst)
    md = MarkdownIt("commonmark", {"html": True, "linkify": True, "typographer": True})
    docs = sort_docs(list(DOCS_DIR.glob("*.md")))
    (SITE_DIR / "index.html").write_text(render_homepage(), encoding="utf-8")
    for doc in docs:
        html = render_page(md, docs, doc)
        target = SITE_DIR / f"{doc.stem}.html"
        target.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    main()
