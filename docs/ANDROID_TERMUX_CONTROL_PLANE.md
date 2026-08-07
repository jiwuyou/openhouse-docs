# Android 与 Termux 控制面

本文定义 OpenHouse Android 宿主如何启动和检查 Termux native 的 service-manager。它适用于 Native（外部 `com.termux`）和 All-in-One；两种宿主的 service-manager 都只能在 Termux native 层长期运行。

## 固定调用链

```text
OpenHouse Android 服务控制页
→ com.termux.RUN_COMMAND
→ openhouse-host/start-control-plane.sh
→ $HOME/.local/share/openhouseai/control-plane/current/
  start-control-plane-termux-native.sh
→ service-daemon start / runsvdir
→ service-manager install-service / sv up
→ 127.0.0.1:20087 health 与认证验证
```

Android 只提交固定入口，不直接执行 `service-manager serve`，也不使用 `nohup`、tmux 或 Ubuntu/proot 承载控制面。入口会优先调用版本化控制包；All-in-One 兼容旧 APK 资源目录作为后备。

Native 首次配对、APK 更新和点击“启动运行中枢”前，都会通过用户已授权的 Termux Home SAF 投放下列文件：

```text
$HOME/.local/share/openhouseai/control-plane/current/
  control-plane-manifest.json
  start-control-plane-termux-native.sh
  repair-control-plane-termux-native.sh
  inspect-control-plane-termux-native.sh
```

`control-plane-manifest.json` 包含版本和 SHA-256。脚本文件先写入，manifest 最后写入，manifest 存在才代表包完整。该目录由 OpenHouse 管理；不要把自己的脚本放在这里。

## 启动约束

完整启动脚本依次检查：

1. Termux native 环境、canonical config、token、curl 和 service-manager 二进制。
2. `service-daemon`、`sv` 与 `runsvdir`。
3. 使用 `service-manager install-service` 写入 runit 服务，再执行 `sv up service-manager`。
4. `GET /api/v1/health`，随后使用 bearer token 请求 `GET /api/v1/services`。

它不会创建新 token、不会替换已存在的未知 service-manager 进程，也不会退回为临时后台进程。`runsvdir` 首次拉起有短暂时序窗口，应等待 readiness，而不是立即重装。

## 诊断与修复

在 Termux native 中运行：

```bash
"$PREFIX/bin/bash" \
  "$HOME/.local/share/openhouseai/control-plane/current/inspect-control-plane-termux-native.sh" inspect
```

输出使用 `control_plane_*` 键，例如：

```text
control_plane_bundle_start-control-plane-termux-native=present
control_plane_runsvdir=running
control_plane_sv_status=run: service-manager: (...)
control_plane_health=ok
control_plane_status=ready
```

`repair_required` 表示先检查推荐动作。只在 config 已存在且确认需要修复时运行：

```bash
"$PREFIX/bin/bash" \
  "$HOME/.local/share/openhouseai/control-plane/current/inspect-control-plane-termux-native.sh" repair
```

诊断不会输出 token。若控制包本身缺失，更新 `wuxianpi.first-install` 至 `1.0.4` 后重新运行其控制面投放步骤；不要反复安装 WuxianPi Runtime。

## 安全边界

- service-manager 只监听 `127.0.0.1`。
- token 只保留在 `$HOME/.config/openhouseai/service-manager/config.json`，不得写入组件清单、日志、市场插件反馈或公开文档。
- Android 使用 `com.termux.RUN_COMMAND` 前，外部 Termux 必须已授权，且 `~/.termux/termux.properties` 启用 `allow-external-apps = true`。
- Ubuntu/proot 中的服务可由 Termux native service-manager 启动，但 Ubuntu 内不得另起一个长期 service-manager。
