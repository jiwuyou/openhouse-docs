# OpenHouse Docs

这个仓库是 OpenHouseAI 的公开版用户与 AI 文档源。

目标：

- 单独维护用户说明与 AI 使用说明
- 独立发布静态文档站
- 给 APK 提供 `openhouse/docs-public` 内置文档快照
- 允许用户不等待新 APK，直接更新公开文档并同步到本机运行期路径

## 目录结构

- `docs/`：公开文档源，包括 Markdown、示例工程和静态资源
- `docs/assets/`：文档图片等静态资源
- `scripts/sync-runtime-docs.sh`：把当前仓库文档同步到本机 OpenHouse 运行期路径
- `scripts/sync-to-apk-assets.sh`：把当前仓库文档同步到 APK `docs-public` 快照目录
- `scripts/build_docs_site.py`：把 Markdown 构建成 HTML 站点
- `site/`：生成后的静态站点目录

## 与 APK 的关系

APK 内置文档快照路径：

```text
/root/projects/smallphoneai/openhouseai-app/app/src/main/assets/openhouse/docs-public
```

发布 APK 前，从本仓库同步快照：

```bash
scripts/sync-to-apk-assets.sh
```

APK 中的 `openhouse/docs-public` 是本仓库 `docs/` 的发布快照，不是长期编辑源。
只改文档时，先改本仓库，再同步 APK 快照。

用户安装 APK 后，文档会被同步到：

```text
/root/openhouse/docs
/root/openhouseai-docs/official
```

如果只是文档更新，用户可以不等新 APK：

```bash
git clone https://github.com/jiwuyou/openhouse-docs.git /root/openhouse-docs
cd /root/openhouse-docs
git pull --ff-only
scripts/sync-runtime-docs.sh
```

这条路径只刷新文档，不要求重新安装 APK，也不修改用户项目、模型配置或运行时数据。

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
