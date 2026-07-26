# claude-bell

English | [中文](README.zh-CN.md)

Notification sounds for Claude Code: a gentle chime when Claude needs you, so you can safely switch away and do something else.

| When | Sound |
|------|-------|
| Claude asks for confirmation / waits for input | "ding-dong?" (rising two-note, question intonation) |
| Claude finishes a task | "ding-dong-DAA!" (same melodic line resolving into a chord) |

Sounds are short (~1s) and soft, share one timbre, and are distinguishable at a glance. Works on Windows / macOS / Linux.

## Install

```
/plugin marketplace add ChALyX/claude-bell
/plugin install claude-bell@claude-bell
```

Or clone and install from a local path:

```
/plugin marketplace add /path/to/claude-bell
/plugin install claude-bell@claude-bell
```

Restart Claude Code (or run `/reload-plugins`) to activate.

## Adjust volume

Takes effect immediately, no restart needed:

```
/claude-bell:volume 50
```

- Range 0–100, `0` mutes, no argument shows the current volume
- Alternatively, write an integer to `~/.claude/claude-bell/volume.txt`

## Replace the sounds

Put your own sound files in `~/.claude/claude-bell/` (on Windows: `C:\Users\<you>\.claude\claude-bell\`):

- `notify.wav` — played when Claude asks for confirmation
- `complete.wav` — played when a task completes

If present, they take priority over the built-in sounds; delete them to restore the defaults.

**Supported format: WAV only** (a Windows player limitation), recommended length under 1.5s.

## Slash commands

| Command | Description |
|---------|-------------|
| `/claude-bell:volume <0-100>` | Set volume, effective immediately; `0` mutes; no argument shows current volume |

## License

MIT
