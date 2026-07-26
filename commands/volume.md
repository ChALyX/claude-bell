---
description: Set notification sound volume (0-100), effective immediately, no restart needed
argument-hint: <0-100>
---

The user wants to set the claude-bell notification sound volume to: $ARGUMENTS

Follow these steps:

1. Validate that the argument is an integer between 0 and 100. If it is empty or invalid, read `~/.claude/claude-bell/volume.txt` and report the current volume (default 100 if the file does not exist), show the usage `/claude-bell:volume <0-100>`, then stop.
2. Ensure the directory `~/.claude/claude-bell/` exists, then write the integer to `~/.claude/claude-bell/volume.txt` (the number only, nothing else).
3. Play a test sound at the new volume so the user can confirm: `bash "${CLAUDE_PLUGIN_ROOT}/scripts/play-sound.sh" complete`
4. Tell the user: volume is set to N, effective immediately (read on every playback, no restart needed); 0 means mute.
