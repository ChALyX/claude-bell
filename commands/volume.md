---
description: 设置提示音音量 (0-100),立即生效无需重启
argument-hint: <0-100>
---

用户想把 claude-bell 插件的提示音音量设为:$ARGUMENTS

请执行以下步骤:

1. 校验参数是 0-100 的整数。如果为空或无效,读取 `~/.claude/claude-bell/volume.txt` 报告当前音量(文件不存在则为默认值 100),并提示用法 `/claude-bell:volume <0-100>`,然后结束。
2. 确保目录 `~/.claude/claude-bell/` 存在,把该整数写入 `~/.claude/claude-bell/volume.txt`(只写数字,无其他内容)。
3. 用新音量播放试听音效让用户确认效果:`bash "${CLAUDE_PLUGIN_ROOT}/scripts/play-sound.sh" complete`
4. 告知用户:音量已设为 N,立即生效(每次播放时读取,无需重启);设为 0 即静音。
