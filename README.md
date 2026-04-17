# OpenHouse Docs

这个仓库单独存放 OpenHouse 的对外使用文档。

目标：

- 单独维护用户说明与 AI 使用说明
- 独立发布静态文档站
- 不和 `termux-app` 主仓库耦合

## 目录结构

- `docs/`：Markdown 源文档
- `docs/assets/`：文档图片等静态资源
- `scripts/build_docs_site.py`：把 Markdown 构建成 HTML 站点
- `site/`：生成后的静态站点目录

## 本地构建

先安装依赖：

```bash
pip install -r requirements.txt
```

再生成站点：

```bash
python3 scripts/build_docs_site.py
```

生成结果在：

```text
site/
```

## 本地预览

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory site
```

然后访问：

```text
http://127.0.0.1:8765/
```

## 发布建议

建议把这个仓库直接发布到 GitHub，再用 GitHub Pages 发布 `site/`。

后续如果需要，我可以继续补：

- 自定义域名配置

## GitHub Pages

仓库已经包含自动发布工作流：

- [pages.yml](/root/openhouse-docs/.github/workflows/pages.yml)

推到 GitHub 之后，建议在仓库设置中启用：

- `Settings -> Pages -> Build and deployment -> Source: GitHub Actions`

之后每次向 `main` 分支推送，都会自动：

- 安装依赖
- 构建 `site/`
- 发布到 GitHub Pages
