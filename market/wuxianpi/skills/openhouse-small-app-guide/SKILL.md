---
name: openhouse-small-app-guide
description: 当用户要求创建、接入、运行、更新或排障 OpenHouse 小 App 时，读取并执行官方指南。
---

# OpenHouse 小 App

开始实现前，完整读取 Package 根目录下的
`docs/OPENHOUSE_SMALL_APP_GUIDE.md`。相对本 Skill 的路径是
`../../../../docs/OPENHOUSE_SMALL_APP_GUIDE.md`。

执行时遵守以下顺序：

1. 识别当前位于 Termux native 还是 Ubuntu/proot。
2. 默认选择 Termux native；只有确认 Termux 不兼容时才使用 Ubuntu/proot。
3. 用 WuxianPi Composite Package 描述可安装内容。
4. 长期进程交给 Termux native 的 service-manager。
5. 用 `openhouse.app` 注册桌面入口，不在桌面 manifest 中放启动命令。
6. 完成状态、健康检查、日志、桌面入口、更新和卸载验证。

如果指南与当前 checkout 的 WuxianPi 或 service-manager 契约冲突，以当前组件仓库的
版本化契约为准，并向用户说明差异。
