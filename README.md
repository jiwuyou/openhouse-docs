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

- GitHub Actions 自动构建
- GitHub Pages 自动发布
- 自定义域名配置
