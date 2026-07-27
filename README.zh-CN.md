# claude-bell

[English](README.md) | 中文

Claude Code 提示音插件:在需要你的时候轻声提醒,让你放心切走窗口干别的事。

| 时机 | 音效 |
|------|------|
| Claude 请求授权 / 需要你的输入 | "叮—咚?"(上行双音,疑问语气) |
| Claude 完成任务 | "叮咚—DAA!"(同一旋律线收束到主和弦) |

音效短促(约 1 秒)、音量柔和,两者共用同一音色,盲听可区分。支持 Windows / macOS / Linux。

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

安装后重启 Claude Code(或执行 `/reload-plugins`)生效。

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
