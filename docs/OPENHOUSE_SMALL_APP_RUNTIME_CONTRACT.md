# OpenHouse 小 App 运行时契约

小 App 的“桌面入口”和“长期服务”是两条独立链路。入口写入 OpenHouse registry；运行进程由 Termux native service-manager 管理。不要用 WebView、tmux 或 Android Activity 代替服务管理。

## 启动链路

```text
components.d/*.json 或 registry API
→ Android 读取并合并 DesktopCatalog
→ 用户从侧边栏或桌面打开小 App
→ 解析 serviceNames / serviceRefs
→ 查询 service-manager endpoint/status
→ 服务不可用时请求 start
→ 等待 endpoint 发布
→ WebView 打开实际 URL
```

组件中的 `serviceNames` 和 `service-manager://services/<id>` 必须指向稳定 service-manager 服务 ID。服务 ID 与组件 ID 可以不同，但 WuxianPi 的桌面组件和服务都统一使用 `yuanshengwuxianpi`。

## Android 使用的 service-manager API

所有管理接口都在本机 `http://127.0.0.1:20087`，除 health 外均使用 canonical config 中的 bearer token。

| 用途 | 方法 | 路径 |
| --- | --- | --- |
| 控制面健康 | `GET` | `/api/v1/health` |
| 服务列表 | `GET` | `/api/v1/services` |
| 批量服务状态 | `GET` | `/api/v1/services/statuses` |
| 单服务状态 | `GET` | `/api/v1/services/:id/status` |
| 生命周期操作 | `POST` | `/api/v1/services/:id/{start,stop,restart,repair}` |
| 服务日志 | `GET` | `/api/v1/services/:id/logs?limit=N` |
| 组件 registry | `GET` | `/api/v1/registry/components` |
| registry 状态 | `GET` | `/api/v1/registry/state` |

组件注册使用：

```text
PUT  /api/v1/registry/components/:componentId
POST /api/v1/registry/sync
```

registry 成功只表示后端已经接受组件。已运行 Android 进程中的桌面仍须执行“刷新桌面组件”或回到前台触发刷新；旧 APK 可能需要完整关闭并重新打开宿主 App。

## 服务状态和错误处理

- `running`：可直接读取 endpoint 并打开 WebView。
- `stopped`：请求 `start` 后使用退避轮询 endpoint；WuxianPi 的 stopped 是正常按需状态。
- `starting` 或 `stopping`：显示进行中，不重复提交生命周期操作。
- `failed`：展示服务日志、重试和维护入口。
- service-manager 不可达：先排查控制面，参见 [Android 与 Termux 控制面](ANDROID_TERMUX_CONTROL_PLANE.md)。

小 App 代码不应持有 service-manager token。Android Host 负责 token 读取和本地 API 调用；组件清单只表达入口和服务引用。
