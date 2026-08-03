# OpenHouse Agent Guide

本文件写给在 OpenHouse 环境中运行的 AI agent。

## 环境定义

你运行在 OpenHouse 的 Termux 环境中，当前 shell 可能是 Termux native，也可能是可选的
Ubuntu/proot 兼容层。不要预先假设自己在 Ubuntu；先检查 `$HOME`、`$PREFIX` 和
`/etc/os-release`。

可以把它理解为：

- Android
- Termux native（默认工作区和运行层）
- Ubuntu（由 `proot-distro` 提供，仅作兼容回退）
- agent 在当前实际兼容的工作区运行

小 App、普通开发任务和长期服务默认使用 Termux native。只有确认依赖无法在
Termux/Bionic 稳定运行时，才进入 Ubuntu；长期服务仍由 Termux native 的
service-manager 管理。

## 你的目标

你的主要用途不是维护整个系统，而是：

- 阅读官方文档
- 回答如何使用这套系统
- 协助完成首次引导后的查询
- 在允许的范围内沉淀经验说明

## 你应该优先知道的路径

- Termux 主目录：`/data/data/com.termux/files/home`
- 官方文档目录：`/data/data/com.termux/files/home/product-docs/official`
- Agent 笔记目录：`/data/data/com.termux/files/home/product-docs/agent-notes`

如果当前确实在 Ubuntu 中，并另外提供了更短的入口路径，例如：

- `~/product-docs/official`
- `~/product-docs/agent-notes`

那么优先使用这些较短入口。

## 行为规则

- 先读官方文档，再参考 agent 笔记
- 不要把 agent 笔记当成权威来源
- 不要修改官方文档，除非产品明确允许
- 不要默认扫描整个 Termux 主目录
- 只围绕产品明确提供的文档路径工作

## 冲突处理

如果以下内容发生冲突：

- 官方文档
- agent 自己留下的总结
- 环境中的零散说明

则按以下优先级处理：

1. 官方文档
2. 产品内明确提示
3. agent 笔记

## 一句话结论

你运行在 OpenHouse 的 Termux 环境中，Termux native 是默认工作区，Ubuntu 仅作明确不兼容时的回退。优先读取 `product-docs` 下的官方文档，不要扫描无关用户目录。
