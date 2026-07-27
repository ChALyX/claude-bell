# claude-bell

[English](README.md) | 中文

Claude Code 提示音插件:在需要你的时候轻声提醒,让你放心切走窗口干别的事。

| 时机 | 音效 |
|------|------|
| Claude 请求授权 / 需要你的输入 | "叮—咚?"(上行双音,疑问语气) |
| Claude 完成任务 | "叮咚—DAA!"(同一旋律线收束到主和弦) |

音效短促(约 1 秒)、音量柔和,两者共用同一音色,盲听可区分。支持 Windows / macOS / Linux。

## 什么时候响,什么时候故意不响

`notify` 依赖 Claude Code 的 `Notification` 事件,而这个事件**不是**在授权框弹出的瞬间发出的。Claude Code 会先等几秒,看你在不在:

| 你的响应 | 结果 |
|----------|------|
| 立刻点确认 | 通知被取消,**完全没有声音**。你人就在键盘前,它不打扰你。 |
| 一直没点 | 事件派发,提示音响起,距离框弹出约 6.5 秒。 |

所以"我秒点了确认却没听到声音"是预期行为,不是漏响。这个等待是 Claude Code 自身的行为:没有任何设置项能调整它,插件也无法缩短。

`complete` 依赖 `Stop` 事件,没有这个等待——每轮回复结束即触发,延迟约 1.3 秒。这 1.3 秒是启动脚本宿主、打开音频设备的固有开销(Windows 上是 PowerShell + WPF MediaPlayer),也是整条链路上唯一属于本插件的部分。

60 秒空闲提醒(`idle_prompt`)被刻意过滤,不会响。

*以上耗时实测于 Windows 11,其他平台会有差异。*

## 安装

```
/plugin marketplace add ChALyX/claude-bell
/plugin install claude-bell@claude-bell
```

也可以克隆到本地后用本地路径安装:

```
/plugin marketplace add /path/to/claude-bell
/plugin install claude-bell@claude-bell
```

安装后**重启 Claude Code** 生效。`/reload-plugins` 不够——hooks 配置只在启动时读取,重载插件不会重新加载它。

## 调整音量

改动立即生效,无需重启:

```
/claude-bell:volume 50
```

- 取值 0–100,`0` 为静音,不带参数显示当前音量

## 替换音效

把你自己的音效文件放到 `~/.claude/claude-bell/`(Windows 即 `C:\Users\<你>\.claude\claude-bell\`):

- `notify.wav` — 请求确认提示音
- `complete.wav` — 任务完成提示音

文件存在即优先于插件自带音效,删除即恢复默认。

**支持格式:仅 WAV**(受 Windows 播放器限制),建议时长 1.5 秒以内。

## 斜杠命令

| 命令 | 说明 |
|------|------|
| `/claude-bell:volume <0-100>` | 设置提示音音量,立即生效;`0` 静音;不带参数显示当前音量 |

## License

MIT
